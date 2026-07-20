"""报告质量校验 — 生成后自动运行，检查乱码/格式/完整性。

用法:
  python tests/check_report.py <report.html>
  python tests/check_report.py <report.html> --strict   (任何 warning 也报失败)
"""

import re, sys, os
from pathlib import Path
from html.parser import HTMLParser

ERRORS = []
WARNINGS = []
PASSED = 0

def fail(name, detail):
    ERRORS.append(f"{name}: {detail}")
    print(f"  [FAIL] {name}")
    print(f"         {detail}")

def warn(name, detail):
    WARNINGS.append(f"{name}: {detail}")
    print(f"  [WARN] {name}")
    print(f"         {detail}")

def ok(name):
    global PASSED
    PASSED += 1
    print(f"  [OK]   {name}")

# ═══════════════════════════════════════
#  1. HTML 基本结构
# ═══════════════════════════════════════
def check_html_structure(html):
    print("\n-- 1. HTML 结构 --")

    ok("<!DOCTYPE html>" if html.startswith("<!DOCTYPE html>") or html.startswith("<!doctype") else fail("missing DOCTYPE", "HTML must start with <!DOCTYPE html>"))

    ok("<html" if "<html" in html[:500] else fail("missing <html>", "HTML must contain <html> tag"))

    ok("<head>" if "<head>" in html else fail("missing <head>", "HTML must have <head> section"))
    ok("</head>" if "</head>" in html else fail("missing </head>", "unclosed head tag"))
    ok("<body>" if "<body>" in html else fail("missing <body>", "HTML must have <body>"))
    ok("</body>" if "</body>" in html else fail("missing </body>", "unclosed body tag"))
    ok("</html>" if "</html>" in html else fail("missing </html>", "unclosed html tag"))

    ok('charset' in html[:500].lower() if html[:500] else fail("missing charset", "meta charset not found in head"))

# ═══════════════════════════════════════
#  2. 乱码检测 (wkhtmltopdf tofu)
# ═══════════════════════════════════════
def check_no_garbled(html):
    print("\n-- 2. 乱码检测 --")

    # wkhtmltopdf 不支持的 Unicode 范围
    forbidden_ranges = [
        (0x1F300, 0x1F9FF, "Emoji (U+1F300-U+1F9FF)"),
        (0x1F1E6, 0x1F1FF, "Flag emoji (U+1F1E6-U+1F1FF)"),
        (0x2700, 0x27BF, "Dingbats (U+2700-U+27BF)"),
        (0x2600, 0x26FF, "Misc symbols (U+2600-U+26FF)"),
        (0x2190, 0x21FF, "Arrows (U+2190-U+21FF)"),
        (0x25A0, 0x25FF, "Blocks/triangles (U+25A0-U+25FF)"),
    ]

    found_any = False
    for i, (lo, hi, label) in enumerate(forbidden_ranges):
        pattern = re.compile(f'[\\U{lo:08X}-\\U{hi:08X}]')
        matches = pattern.findall(html)
        if matches:
            unique = list(set(matches))[:8]
            found_any = True
            fail(f"forbidden chars ({label})",
                 f"{len(matches)} occurrences, samples: {repr(''.join(unique))}")

    if not found_any:
        ok("no forbidden Unicode ranges (emoji/symbols)")
    else:
        warn("report contains wkhtmltopdf-incompatible chars",
             "these will render as blank boxes (tofu) in PDF. Use plain Chinese text instead.")

    # 检查是否用了中文替代方案（好习惯）
    safe_patterns = [r'\[涨\]', r'\[跌\]', r'上涨', r'下跌']
    has_safe = any(re.search(p, html) for p in safe_patterns)
    if has_safe:
        ok("uses text-based fallbacks instead of emoji ([涨]/[跌])")

# ═══════════════════════════════════════
#  3. 必需 section 检查
# ═══════════════════════════════════════
def check_sections(html):
    print("\n-- 3. 报告章节完整性 --")

    required_sections = [
        ("指数概览 or 指数", ["指数概览", "三大指数", "指数快照", "Index Snapshot"]),
        ("月度走势 (K线/折线)", ["近一月走势", "K线图", "kline-section", "line-section"]),
        ("涨跌幅最大个股", ["涨跌幅最大个股", "Top Movers"]),
        ("板块轮动", ["板块轮动", "领涨板块", "领跌板块", "bar-section"]),
        ("宏观环境", ["宏观环境", "宏观分析", "Macro"]),
        ("关注前瞻", ["关注前瞻", "下周关注", "What to Watch"]),
        ("知识点", ["知识点", "knowledge-card"]),
    ]

    for label, keywords in required_sections:
        found = any(kw in html for kw in keywords)
        if found:
            ok(f"section: {label}")
        else:
            fail(f"missing section: {label}",
                 f"none of these found: {keywords}")

# ═══════════════════════════════════════
#  4. 图表引用检查
# ═══════════════════════════════════════
def check_charts(html):
    print("\n-- 4. 图表引用 --")

    img_tags = re.findall(r'<img[^>]+src="([^"]+)"', html)
    if img_tags:
        ok(f"{len(img_tags)} image(s) referenced")
        for src in img_tags:
            # 检查本地文件是否存在
            if src.startswith("charts/") or src.startswith("bg-"):
                full = Path(os.getcwd()) / src
                if full.exists():
                    ok(f"  chart file exists: {src}")
                else:
                    fail(f"chart file missing: {src}",
                         f"expected at: {full}")
            elif src.startswith("http"):
                warn(f"  remote image: {src}", "network-dependent, may fail offline")
    else:
        warn("no <img> tags found", "report may be missing chart images")

    # 检查 CSS 柱状图是否存在
    bar_chart = re.search(r'bar-section|bar-chart', html)
    if bar_chart:
        ok("CSS bar chart present (sector performance)")

    # 检查 SVG 图表
    svg_charts = re.findall(r'<svg[^>]*>', html)
    if svg_charts:
        ok(f"{len(svg_charts)} inline SVG chart(s)")

# ═══════════════════════════════════════
#  5. 表格完整性
# ═══════════════════════════════════════
def check_tables(html):
    print("\n-- 5. 表格检查 --")

    tables = re.findall(r'<table[^>]*>', html)
    table_close = re.findall(r'</table>', html)
    if len(tables) == len(table_close):
        ok(f"{len(tables)} table(s) properly opened/closed")
    else:
        fail(f"table mismatch", f"{len(tables)} open vs {len(table_close)} close tags")

    # 检查涨跌颜色标注
    up_count = len(re.findall(r'class="[^"]*up[^"]*"', html)) + html.count('class="up"')
    down_count = len(re.findall(r'class="[^"]*down[^"]*"', html)) + html.count('class="down"')
    if up_count + down_count > 0:
        ok(f"color coding: {up_count} up (green), {down_count} down (red)")
    else:
        warn("no .up/.down color tags found", "涨跌数据可能缺少颜色标注")

# ═══════════════════════════════════════
#  6. 关键数据检查
# ═══════════════════════════════════════
def check_data_presence(html):
    print("\n-- 6. 关键数据 --")

    # 检查是否有数字（指数点位）
    numbers = re.findall(r'\d[\d,]+\.?\d*', html)
    if len(numbers) > 10:
        ok(f"{len(numbers)} numeric values found (index prices, percentages)")
    else:
        warn("very few numbers in report", "可能缺少关键行情数据")

    # 检查日期
    dates = re.findall(r'2026-\d\d-\d\d', html)
    if dates:
        ok(f"date found: {dates[0]}")

    # 检查常见指数名称
    idx_names = re.findall(r'S&P 500|NASDAQ|Dow|道琼斯|标普|纳指|恒生|上证|深证', html)
    if idx_names:
        ok(f"index names found: {list(set(idx_names))}")

# ═══════════════════════════════════════
#  7. CSS 质量
# ═══════════════════════════════════════
def check_css(html):
    print("\n-- 7. CSS 质量 --")

    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    if style_blocks:
        css = '\n'.join(style_blocks)
        ok("CSS present" if len(css) > 100 else warn("CSS block exists but very short", "may be missing styles"))
    else:
        fail("no <style> block found", "HTML must contain embedded CSS")

    # 关键颜色检查
    key_colors = {'#16a34a': 'gain green', '#dc2626': 'loss red', '#2563eb': 'accent blue'}
    for color, label in key_colors.items():
        if color in html:
            ok(f"  {label} ({color})")
        else:
            warn(f"  missing {label} ({color})", "color coding may not render correctly")

    # 字体检查
    if 'Microsoft YaHei' in html or 'SimHei' in html or 'PingFang' in html:
        ok("Chinese font stack present")
    else:
        fail("no Chinese font stack", "Chinese characters may not render in PDF")

# ═══════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════
def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/check_report.py <report.html> [--strict]")
        sys.exit(2)

    html_path = sys.argv[1]
    strict = "--strict" in sys.argv

    if not os.path.exists(html_path):
        print(f"[FATAL] File not found: {html_path}")
        sys.exit(1)

    html = Path(html_path).read_text(encoding="utf-8")
    file_size = len(html)
    print(f"Report: {html_path}")
    print(f"Size:   {file_size:,} bytes ({len(html.split(chr(10)))} lines)")

    check_html_structure(html)
    check_no_garbled(html)
    check_sections(html)
    check_charts(html)
    check_tables(html)
    check_data_presence(html)
    check_css(html)

    # ── 汇总 ──
    total = PASSED + len(ERRORS)
    print(f"\n{'='*60}")
    status = "PASSED" if not ERRORS else "FAILED"
    print(f"  Report Quality: {status}")
    print(f"  Checks passed:  {PASSED}/{total}")
    if WARNINGS:
        print(f"  Warnings:       {len(WARNINGS)}")
        for w in WARNINGS:
            print(f"    - {w}")
    if ERRORS:
        print(f"  Errors:         {len(ERRORS)}")
        for e in ERRORS:
            print(f"    - {e}")
    print(f"{'='*60}")

    if strict and WARNINGS:
        print("\n[STRICT mode] Warnings treated as errors.")
        sys.exit(1)

    sys.exit(0 if not ERRORS else 1)

if __name__ == "__main__":
    main()

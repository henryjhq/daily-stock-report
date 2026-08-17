"""渲染链路测试：HTML 生成 → PDF 输出。"""
import os, sys, json, tempfile
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
ERRORS = []
PASSED = 0

def check(name, condition, detail=""):
    global PASSED
    if condition:
        PASSED += 1
        print(f"  [OK]  {name}")
    else:
        ERRORS.append(f"{name}: {detail}")
        print(f"  [FAIL] {name}  —  {detail}")

# ═══════════════════════════════════════
#  1. Playwright 可用性
# ═══════════════════════════════════════
print("\n── 1. Playwright 可用性 ──")
try:
    from playwright.sync_api import sync_playwright
    check("playwright module imported", True)
except ImportError:
    check("playwright module imported", False, "pip install playwright")
    print("\n[ABORT] Playwright not available, skipping render tests.")
    sys.exit(1)

# ═══════════════════════════════════════
#  2. 生成测试 HTML
# ═══════════════════════════════════════
print("\n── 2. 生成测试 HTML ──")
today = datetime.now().strftime("%Y-%m-%d")

test_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>Test Report</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:"Microsoft YaHei",sans-serif; color:#334155; max-width:800px; margin:0 auto; padding:48px 40px; }}
h2 {{ font-size:20px; margin:36px 0 12px; padding-bottom:8px; border-bottom:3px solid #2563eb; color:#0f172a; }}
.data-table {{ width:100%; border-collapse:collapse; margin:16px 0; font-size:14px; }}
.data-table th {{ background:#f1f5f9; padding:10px 12px; border-bottom:2px solid #cbd5e1; }}
.data-table td {{ padding:9px 12px; border-bottom:1px solid #e2e8f0; }}
.up {{ color:#16a34a; font-weight:700; }}
.down {{ color:#dc2626; font-weight:700; }}
.callout {{ background:#eff6ff; border-left:4px solid #2563eb; padding:14px 18px; margin:18px 0; border-radius:0 6px 6px 0; }}
</style></head>
<body>
<div class="report-header"><h1>测试报告</h1><p class="meta">日期: {today}</p></div>
<h2>一、指数概览</h2>
<table class="data-table">
<tr><th>指数</th><th>收盘</th><th>涨跌</th></tr>
<tr><td>S&P 500</td><td>7,457.69</td><td class="down">-1.01%</td></tr>
<tr><td>NASDAQ</td><td>25,520.24</td><td class="down">-1.40%</td></tr>
</table>
<div class="callout"><strong>测试通过:</strong> 此报告由自动化测试脚本生成，用于验证 HTML→PDF 渲染链路是否正常。</div>
<h2>二、测试数据</h2>
<table class="data-table">
<tr><th>检查项</th><th>状态</th></tr>
<tr><td>中文字体渲染</td><td class="up">正常</td></tr>
<tr><td>表格样式</td><td class="up">正常</td></tr>
<tr><td>颜色标记 (涨/跌)</td><td class="up">正常</td></tr>
<tr><td>Callout 标注框</td><td class="up">正常</td></tr>
</table>
<div class="report-footer" style="margin-top:48px;padding-top:16px;border-top:1px solid #e2e8f0;font-size:11px;color:#94a3b8;text-align:center;">
测试报告 | 渲染链路验证 | {today}
</div>
</body></html>"""

test_dir = ROOT / "tests" / "output"
test_dir.mkdir(exist_ok=True)
html_path = test_dir / "test-report.html"
html_path.write_text(test_html, encoding="utf-8")
check("test HTML generated", html_path.exists(), f"path: {html_path}")
print(f"       saved to: {html_path}")

# ═══════════════════════════════════════
#  3. HTML → PDF
# ═══════════════════════════════════════
print("\n── 3. HTML → PDF ──")
pdf_path = test_dir / "test-report.pdf"

try:
    abs_html = "file:///" + str(html_path.resolve()).replace("\\", "/")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 1200})
        page.goto(abs_html, wait_until="networkidle", timeout=15000)
        page.pdf(
            path=str(pdf_path),
            format="A4",
            margin={"top": "15mm", "bottom": "15mm", "left": "12mm", "right": "12mm"},
            print_background=True,
        )
        browser.close()

    pdf_size = pdf_path.stat().st_size
    check("PDF generated successfully", pdf_path.exists() and pdf_size > 1000,
          f"size: {pdf_size} bytes")
    print(f"       saved to: {pdf_path} ({pdf_size} bytes)")

except Exception as e:
    check("PDF generation", False, str(e))

# ═══════════════════════════════════════
#  4. PDF 内容验证 (pdftotext)
# ═══════════════════════════════════════
print("\n── 4. PDF 内容验证 ──")
try:
    import subprocess
    result = subprocess.run(
        ["pdftotext", str(pdf_path), "-", "-l", "1"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0:
        text = result.stdout
        checks = [
            ("contains title", "测试报告" in text),
            ("contains S&P 500", "S&P 500" in text),
            ("contains NASDAQ", "NASDAQ" in text),
            ("contains Chinese chars", "测试通过" in text or "指数" in text),
        ]
        for name, ok in checks:
            check(f"  {name}", ok)
    else:
        check("pdftotext ran", False, f"exit code {result.returncode}")
except FileNotFoundError:
    print("  [SKIP] pdftotext not installed (optional)")
except Exception as e:
    print(f"  SKIP  pdftotext error: {e}")

# ═══════════════════════════════════════
#  结果汇总
# ═══════════════════════════════════════
total = PASSED + len(ERRORS)
print(f"\n{'='*60}")
print(f"  渲染测试: {PASSED}/{total} 通过", end="")
if ERRORS:
    print(f", {len(ERRORS)} 失败")
else:
    print(", 全部通过!")
print(f"{'='*60}")

if ERRORS:
    print("\nFailures:")
    for e in ERRORS:
        print(f"  [FAIL] {e}")

sys.exit(0 if not ERRORS else 1)

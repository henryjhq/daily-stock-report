"""配置和模板完整性校验。"""
import json, os, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS = []
WARNINGS = []
PASSED = 0
TOTAL = 0

def check(name, condition, detail=""):
    global PASSED, TOTAL
    TOTAL += 1
    if condition:
        PASSED += 1
        print(f"  [OK]  {name}")
    else:
        ERRORS.append(name)
        print(f"  [FAIL] {name}  —  {detail}")

def warn(name, msg):
    WARNINGS.append(f"{name}: {msg}")
    print(f"  [WARN] {name}  —  {msg}")

# ═══════════════════════════════════════
#  1. theme.json
# ═══════════════════════════════════════
print("\n── 1. theme.json ──")
try:
    theme = json.load(open(ROOT / "theme.json"))
    required_keys = ["name", "background", "accent", "gain", "loss", "fontSize",
                     "aiDecorations", "imageApi"]
    for k in required_keys:
        check(f"theme.json has key '{k}'", k in theme, f"missing key: {k}")

    valid_presets = ["default-light", "warm-cream", "cool-slate", "ink-blue", "dark"]
    check("name is a known preset", theme.get("name") in valid_presets,
          f"unknown preset: {theme.get('name')}")

    check("background is valid hex", re.match(r'^#[0-9a-fA-F]{6}$', theme.get("background", "")),
          f"bad hex: {theme.get('background')}")

    check("aiDecorations is bool", isinstance(theme.get("aiDecorations"), bool))

    img = theme.get("imageApi", {})
    check("imageApi.endpoint exists", bool(img.get("endpoint")), "missing endpoint")
    check("imageApi.model exists", bool(img.get("model")), "missing model")
    key = img.get("apiKey", "")
    if key == "YOUR_API_KEY_HERE":
        warn("imageApi.apiKey", "使用占位符 — 公开发布安全, 但需要填入真实 Key 才能生成纹理")
    else:
        check("imageApi.apiKey is set", len(key) > 10, f"key length: {len(key)}")
    check("imageApi.apiKey is string", isinstance(img.get("apiKey"), str))
except Exception as e:
    ERRORS.append(f"theme.json parse: {e}")
    print(f"  FAIL  theme.json parse  —  {e}")

# ═══════════════════════════════════════
#  2. 模板文件
# ═══════════════════════════════════════
print("\n── 2. 模板 (templates/) ──")
TEMPLATES = ["us-stock.md", "hk-stock.md", "a-stock.md", "generic.md"]
VALID_CHARTS = {"table", "bar", "flow", "line", "kline", "none"}
SECTION_RE = re.compile(r'^###\s+(\d+)\.\s+')

for fname in TEMPLATES:
    path = ROOT / "templates" / fname
    check(f"template '{fname}' exists", path.exists(), "file not found")
    if not path.exists():
        continue

    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # 检查 chart 标签
    chart_tags = re.findall(r'\*\*chart:\s+(\w+)\*\*', content)
    for tag in chart_tags:
        check(f"  '{fname}' chart:{tag} is valid", tag in VALID_CHARTS,
              f"unknown chart type: {tag}")

    if not chart_tags:
        warn(f"'{fname}'", "no chart tags found")

    # 检查 section 编号是否连续
    sections = SECTION_RE.findall(content)
    nums = [int(n) for n in sections]
    if nums:
        expected = list(range(1, len(nums) + 1))
        if nums != expected:
            warn(f"'{fname}' section numbers", f"got {nums}, expected {expected}")
        else:
            check(f"  '{fname}' section numbering is sequential ({len(nums)} sections)", True)

    # 检查是否有 "指数近一月走势" section (v3 新增)
    check(f"  '{fname}' has monthly trend section",
          "近一月走势" in content,
          "missing v3 monthly trend section")

# ═══════════════════════════════════════
#  3. SKILL.md 结构
# ═══════════════════════════════════════
print("\n── 3. SKILL.md ──")
skill = ROOT / "SKILL.md"
check("SKILL.md exists", skill.exists())
if skill.exists():
    content = skill.read_text(encoding="utf-8")
    lines = content.split("\n")
    line_count = len(lines)

    check("SKILL.md > 500 lines (v3 should be ~1070)", line_count > 500,
          f"only {line_count} lines")
    check("has Phase 0 (market resolution)", "Phase 0" in content)
    check("has Phase 1 (data collection)", "Phase 1" in content)
    check("has Phase 2 (HTML generation)", "Phase 2" in content)
    check("has Phase 3 (PDF output)", "Phase 3" in content)
    check("mentions chart: kline", "chart: kline" in content)
    check("mentions chart: line", "chart: line" in content)
    check("mentions theme.json", "theme.json" in content)
    check("mentions imageApi", "imageApi" in content)
    check("mentions Playwright", "Playwright" in content.lower() or "playwright" in content)
    check("has frontmatter name", content.startswith("---"))

# ═══════════════════════════════════════
#  4. VERSION
# ═══════════════════════════════════════
print("\n── 4. VERSION ──")
ver = ROOT / "VERSION"
check("VERSION exists", ver.exists())
if ver.exists():
    v = ver.read_text().strip()
    check("VERSION matches 3.0.0", v == "3.0.0", f"got '{v}'")

# ═══════════════════════════════════════
#  5. 其他文件
# ═══════════════════════════════════════
print("\n── 5. 其他文件 ──")
for f in ["README.md", "watchlist.md", "setup.sh"]:
    check(f"'{f}' exists", (ROOT / f).exists())

trackers = list((ROOT / "trackers").glob("*.md"))
check("trackers/ has 5 files", len(trackers) == 5, f"found {len(trackers)}")

# ═══════════════════════════════════════
#  结果汇总
# ═══════════════════════════════════════
print(f"\n{'='*60}")
print(f"  结果: {PASSED}/{TOTAL} 通过", end="")
if ERRORS:
    print(f", {len(ERRORS)} 失败")
else:
    print(", 全部通过!")
if WARNINGS:
    print(f"  警告: {len(WARNINGS)}")
    for w in WARNINGS:
        print(f"    - {w}")
print(f"{'='*60}")

if ERRORS:
    print("\nFailures:")
    for e in ERRORS:
        # Use ASCII-safe output for Windows console compatibility
        print(f"  [FAIL] {e}")

sys.exit(0 if not ERRORS else 1)

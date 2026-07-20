#!/usr/bin/env bash
# ============================================================
#  daily-stock-report — 完整测试流程
#  运行: bash tests/run_all.sh
#  选项: --skip-render  跳过 HTML→PDF 渲染测试
#        --skip-config  跳过配置文件测试
# ============================================================
set -euo pipefail
cd "$(dirname "$0")/.."

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

PYTHON=""
for p in python3 python "E:/Python/python.exe"; do
  if $p --version >/dev/null 2>&1; then PYTHON="$p"; break; fi
done
if [ -z "$PYTHON" ]; then
  echo -e "${RED}[FATAL] Python not found${NC}"
  exit 1
fi

SKIP_RENDER=false
SKIP_CONFIG=false
SKIP_REPORT=false
for arg in "$@"; do
  case "$arg" in
    --skip-render) SKIP_RENDER=true ;;
    --skip-config) SKIP_CONFIG=true ;;
    --skip-report) SKIP_REPORT=true ;;
  esac
done

PASS=0
FAIL=0

run_test() {
  local name="$1"
  local cmd="$2"
  echo ""
  echo -e "${CYAN}══════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  $name${NC}"
  echo -e "${CYAN}══════════════════════════════════════════════${NC}"
  if eval "$cmd"; then
    ((PASS++)) || true
    echo ""
    echo -e "${GREEN}  >>> $name: PASSED${NC}"
  else
    ((FAIL++)) || true
    echo ""
    echo -e "${RED}  >>> $name: FAILED (exit code $?)${NC}"
  fi
}

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  daily-stock-report — Test Suite            ║"
echo "║  $(date '+%Y-%m-%d %H:%M:%S')                       ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "  Python: $PYTHON ($($PYTHON --version 2>&1))"
echo "  CWD:    $(pwd)"

# ── 1. 配置文件检查 ──
if [ "$SKIP_CONFIG" = false ]; then
  run_test "1/4  配置 & 模板校验" "$PYTHON tests/check_config.py"
else
  echo -e "${CYAN}  [SKIP] 配置检查${NC}"
fi

# ── 2. Git 状态检查 ──
run_test "2/4  Git 状态检查" "
  echo '  Branch:' && git branch --show-current &&
  echo '  Last commit:' && git log --oneline -1 &&
  echo '  Uncommitted:' && git status --short | wc -l | xargs -I{} echo '  {} files' &&
  echo '  Tag v3.0.0:' && git tag -l 'v3.0.0'
"

# ── 3. 渲染链路测试 ──
if [ "$SKIP_RENDER" = false ]; then
  run_test "3/4  HTML→PDF 渲染链路" "$PYTHON tests/check_render.py"
else
  echo -e "${CYAN}  [SKIP] 渲染测试${NC}"
fi

# ── 4. 文件完整性 ──
run_test "4/5  文件完整性" "
  echo '  Required files:' &&
  for f in SKILL.md theme.json VERSION README.md watchlist.md setup.sh \
           templates/us-stock.md templates/hk-stock.md templates/a-stock.md templates/generic.md \
           trackers/us-stock-tracker.md trackers/hk-stock-tracker.md trackers/a-stock-tracker.md \
           trackers/generic-tracker.md trackers/knowledge-tracker.md; do
    if [ -f \"\$f\" ]; then
      echo \"    [OK] \$f\"
    else
      echo \"    [MISSING] \$f\"
    fi
  done
"

# ── 5. 报告质量检查 (如果有上次生成的报告) ──
if [ "$SKIP_REPORT" = false ]; then
  LATEST_REPORT=$(find ../reports/daily-stock -name "us-report-*.html" -type f 2>/dev/null | sort -r | head -1)
  if [ -n "$LATEST_REPORT" ] && [ -f "$LATEST_REPORT" ]; then
    run_test "5/5  报告质量检查 ($(basename "$LATEST_REPORT"))" "$PYTHON tests/check_report.py \"$LATEST_REPORT\""
  else
    echo -e "${CYAN}  [SKIP] No existing report to check${NC}"
  fi
else
  echo -e "${CYAN}  [SKIP] 报告质量检查${NC}"
fi

# ── 结果汇总 ──
TOTAL=$((PASS + FAIL))
echo ""
echo "╔══════════════════════════════════════════════╗"
if [ "$FAIL" -eq 0 ]; then
  echo -e "║  ${GREEN}ALL TESTS PASSED: $PASS/$TOTAL${NC}                           ║"
else
  echo -e "║  ${RED}$FAIL/$TOTAL FAILED${NC}                                  ║"
fi
echo "╚══════════════════════════════════════════════╝"

# 清理测试输出
if [ -d tests/output ]; then
  echo ""
  echo "  Test artifacts kept in tests/output/"
fi

exit $FAIL

#!/usr/bin/env bash
set -euo pipefail

# ── daily-stock-report setup ──────────────────────────────────────────────
# One-command install. Supports Claude Code, Codex, and Codebuddy.
# Usage:
#   ./setup.sh              auto-detect agent, install
#   ./setup.sh --all        install to all detected agents
#   ./setup.sh --check      check for updates
#   ./setup.sh --update     pull latest + reinstall
# ──────────────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

banner() {
  echo ""
  echo -e "${CYAN}╔══════════════════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║   📊 daily-stock-report — install & configure        ║${NC}"
  echo -e "${CYAN}╚══════════════════════════════════════════════════════╝${NC}"
  echo ""
}

success() { echo -e "${GREEN}✓${NC} $1"; }
warn()   { echo -e "${YELLOW}⚠${NC} $1"; }
fail()   { echo -e "${RED}✗${NC} $1"; exit 1; }
info()   { echo -e "${CYAN}→${NC} $1"; }

# ── Parse arguments ──────────────────────────────────────────────────────

MODE="auto"
while [ $# -gt 0 ]; do
  case "$1" in
    --all) MODE="all" ;;
    --check) MODE="check" ;;
    --update) MODE="update" ;;
    --help|-h)
      echo "Usage: ./setup.sh [--all|--check|--update]"
      echo "  (none)    Auto-detect agent and install"
      echo "  --all     Install to all detected agents"
      echo "  --check   Check for updates"
      echo "  --update  Pull latest version and reinstall"
      exit 0
      ;;
    *) fail "Unknown option: $1 (use --help)" ;;
  esac
  shift
done

# ── --check mode ──────────────────────────────────────────────────────────

if [ "$MODE" = "check" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  cd "$SCRIPT_DIR"
  if [ -d .git ]; then
    git fetch origin 2>/dev/null || { echo "Cannot reach remote — skipping check"; exit 0; }
    BEHIND=$(git rev-list HEAD..origin/main --count 2>/dev/null || echo "0")
    if [ "$BEHIND" = "0" ]; then
      echo "✓ Up to date ($(cat VERSION 2>/dev/null || echo unknown))"
    else
      echo "$BEHIND commit(s) behind. Run: ./setup.sh --update"
    fi
  else
    echo "Not a git repo — cannot check for updates"
    echo "Re-clone from: https://github.com/<user>/daily-stock-report.git"
  fi
  exit 0
fi

# ── --update mode ─────────────────────────────────────────────────────────

if [ "$MODE" = "update" ]; then
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  cd "$SCRIPT_DIR"
  if [ -d .git ]; then
    info "Pulling latest..."
    git pull origin main || fail "git pull failed — check your network"
    success "Updated to $(cat VERSION 2>/dev/null || echo unknown)"
  else
    fail "Not a git repo — re-clone to update"
  fi
  # Fall through to install after pull
  MODE="auto"
fi

banner

# ── 1. Detect installed agents ────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
declare -a TARGETS=()

# Claude Code
if [ -d "$HOME/.claude" ] || command -v claude &>/dev/null; then
  TARGETS+=("claude")
fi

# Codex
if [ -d "$HOME/.codex" ] || command -v codex &>/dev/null; then
  TARGETS+=("codex")
fi

# Codebuddy
if [ -d "$HOME/.codebuddy" ]; then
  TARGETS+=("codebuddy")
fi

# Default to Claude Code if nothing detected
if [ ${#TARGETS[@]} -eq 0 ]; then
  warn "No AI agent detected — defaulting to Claude Code"
  TARGETS+=("claude")
fi

echo "Detected agents: ${TARGETS[*]}"
echo ""

# ── Install function ──────────────────────────────────────────────────────

install_for() {
  local agent="$1"
  local dest

  case "$agent" in
    claude)
      dest="$HOME/.claude/skills/daily-stock-report"
      ;;
    codex)
      dest="$HOME/.codex/skills/daily-stock-report"
      ;;
    codebuddy)
      dest="$HOME/.codebuddy/skills-marketplace/skills/daily-stock-report"
      ;;
  esac

  info "Installing for $agent → $dest"

  if [ "$SCRIPT_DIR" != "$dest" ]; then
    mkdir -p "$(dirname "$dest")"
    if [ -d "$dest" ]; then
      rm -rf "${dest}.bak" 2>/dev/null || true
      mv "$dest" "${dest}.bak"
      warn "Backed up existing install to ${dest}.bak"
    fi
    cp -R "$SCRIPT_DIR" "$dest"
  fi

  # For Codebuddy, replace root SKILL.md with codebuddy variant
  if [ "$agent" = "codebuddy" ] && [ -f "$dest/codebuddy/SKILL.md" ]; then
    cp "$dest/codebuddy/SKILL.md" "$dest/SKILL.md"
    info "  → Used Codebuddy-specific SKILL.md"
  fi

  success "$agent: installed"
}

# ── 2. Run installs ──────────────────────────────────────────────────────

if [ "$MODE" = "all" ]; then
  for agent in "${TARGETS[@]}"; do
    install_for "$agent"
  done
else
  # Auto mode: install only to first detected agent
  install_for "${TARGETS[0]}"
  if [ ${#TARGETS[@]} -gt 1 ]; then
    info "Also detected: ${TARGETS[*]:1}"
    info "Run './setup.sh --all' to install everywhere"
  fi
fi

# ── 3. Create output directory ────────────────────────────────────────────

REPORT_DIR="$HOME/.claude/daily-stock-reports"
mkdir -p "$REPORT_DIR"
success "Report output: $REPORT_DIR"

# ── 4. Check wkhtmltopdf ──────────────────────────────────────────────────

if command -v wkhtmltopdf &>/dev/null || where wkhtmltopdf &>/dev/null 2>&1; then
  success "wkhtmltopdf: ready"
else
  warn "wkhtmltopdf not found — PDF conversion will auto-install on first run"
  echo "  The skill will run one of:"
  echo "    winget install wkhtmltopdf    (Windows)"
  echo "    brew install wkhtmltopdf      (Mac)"
  echo "    sudo apt install wkhtmltopdf  (Linux)"
fi

# ── 5. Add routing entry to CLAUDE.md ─────────────────────────────────────

CLAUDE_MD="$HOME/.claude/CLAUDE.md"
SKILL_ENTRY="
## daily-stock-report

When the user asks for a market update, daily stock report, or mentions
\"美股\"/\"港股\"/\"A股\"/\"股票报告\"/\"market report\", invoke /daily-stock-report.

Trigger examples:
- \"给我一份今天的美股报告\" → /daily-stock-report 美股
- \"How did HK markets do today?\" → /daily-stock-report 港股
- \"每日股评 A股\" → /daily-stock-report A股
- \"今天的市场报告\" → /daily-stock-report (asks user which market)"

if [ -f "$CLAUDE_MD" ]; then
  if grep -q "daily-stock-report" "$CLAUDE_MD" 2>/dev/null; then
    success "Routing entry already in $CLAUDE_MD"
  else
    echo "$SKILL_ENTRY" >> "$CLAUDE_MD"
    success "Added routing entry to $CLAUDE_MD"
  fi
else
  echo "$SKILL_ENTRY" > "$CLAUDE_MD"
  success "Created $CLAUDE_MD"
fi

# ── 6. Cron hint ──────────────────────────────────────────────────────────

echo ""
echo -e "${CYAN}── Optional: daily cron ──────────────────────────────${NC}"
echo ""
echo "  US stocks (6 PM ET, weekdays):"
echo '    /cron "0 18 * * 1-5" /daily-stock-report 美股'
echo ""
echo "  HK stocks (after 4 PM HKT, weekdays):"
echo '    /cron "30 8 * * 1-5" /daily-stock-report 港股'
echo ""
echo "  A-shares (after 3 PM CST, weekdays):"
echo '    /cron "30 7 * * 1-5" /daily-stock-report A股'
echo ""

echo -e "${GREEN}── Setup complete ───────────────────────────────────${NC}"
echo ""
echo "  Run: /daily-stock-report"
echo "  Or:  /daily-stock-report 美股"
echo ""

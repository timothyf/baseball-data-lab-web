#!/usr/bin/env bash
set -euo pipefail

PKG_NAME="baseball-data-lab"
LOCAL_PATH="../baseball-data-lab"

usage() {
  echo "Usage: $0 {install|dev|revert|where|auto}"
  echo
  echo "  install   Install from requirements.txt (Codex-compatible)"
  echo "  dev       Override with local editable package at $LOCAL_PATH"
  echo "  revert    Revert to Git-installed package (from requirements.txt)"
  echo "  where     Show where Python is loading $PKG_NAME from"
  echo "  auto      Auto-detect: use local if available, else fallback to requirements"
  exit 1
}

if [ $# -eq 0 ]; then
  CMD="auto"
else
  CMD=$1
fi

case "$CMD" in
  install)
    echo "📦 Installing from requirements.txt..."
    python -m pip install -r requirements.txt
    ;;
  dev)
    echo "🔧 Installing in editable mode from $LOCAL_PATH..."
    python -m pip uninstall -y "$PKG_NAME" || true
    python -m pip install -e "$LOCAL_PATH"
    ;;
  revert)
    echo "♻️ Reverting to Git-installed package from requirements.txt..."
    python -m pip uninstall -y "$PKG_NAME" || true
    python -m pip install -r requirements.txt
    ;;
  where)
    python - <<'EOF'
import importlib.util
name = "baseball_data_lab"
spec = importlib.util.find_spec(name)
print(f"{name} loaded from: {spec.origin}" if spec else f"{name} not found")
EOF
    ;;
  auto)
    if [ -d "$LOCAL_PATH" ]; then
      echo "✅ Local package detected at $LOCAL_PATH. Using dev mode..."
      "$0" dev
    else
      echo "⚠️ No local package found. Falling back to requirements.txt..."
      "$0" install
    fi
    ;;
  *)
    usage
    ;;
esac

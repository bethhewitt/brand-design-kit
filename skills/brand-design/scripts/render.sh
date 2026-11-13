#!/usr/bin/env bash
# Render HTML to PNG/PDF. First run installs Playwright into a per-user cache
# (~/.cache/brand-design) and Chromium into Playwright's own browser cache, so
# no repo needs either as a dependency.
#
#   bash render.sh <in.html> <out.png|out.pdf> [options]   (options: see render.cjs)
set -euo pipefail

PLAYWRIGHT_VERSION="${PLAYWRIGHT_VERSION:-1.49.1}"
RUNTIME="${BD_RUNTIME:-${XDG_CACHE_HOME:-$HOME/.cache}/brand-design/runtime-$PLAYWRIGHT_VERSION}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v node >/dev/null 2>&1; then
  echo "error: Node.js is required for PNG/PDF export (https://nodejs.org)" >&2
  exit 1
fi

if [[ ! -d "$RUNTIME/node_modules/playwright" ]]; then
  echo "brand-design: installing Playwright $PLAYWRIGHT_VERSION into $RUNTIME (one-time)…" >&2
  mkdir -p "$RUNTIME"
  npm install --silent --no-audit --no-fund --prefix "$RUNTIME" "playwright@$PLAYWRIGHT_VERSION" >&2
fi
if [[ ! -f "$RUNTIME/.chromium-ok" ]]; then
  "$RUNTIME/node_modules/.bin/playwright" install chromium >&2
  touch "$RUNTIME/.chromium-ok"
fi

BD_RUNTIME="$RUNTIME" exec node "$SCRIPT_DIR/render.cjs" "$@"

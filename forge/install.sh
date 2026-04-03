#!/bin/bash
set -e

FORGE_DIR="$HOME/crucible/forge"
echo "🔥 Installing forge into Crucible..."

mkdir -p "$FORGE_DIR"/{core,ui}
cd "$FORGE_DIR"

touch core/__init__.py ui/__init__.py

pip install rich textual httpx --break-system-packages --quiet

echo "✅ forge ready at $FORGE_DIR"

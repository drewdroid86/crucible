#!/bin/zsh

# Crucible Forge: Layer 0 Bootstrapper
# Optimized for Pixel 9 Pro (Tensor G4) + Termux
# Built: April 1, 2026 @ 05:00 AM

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "${BLUE}⚒️  Initializing Crucible Forge...${NC}"

# --- 1. Audit System Packages ---
echo "${YELLOW}🔍 Auditing System Packages...${NC}"
REQUIRED_PKG=("nodejs-lts" "python" "git" "zsh" "termux-api" "rust")
for pkg in "${REQUIRED_PKG[@]}"; do
    if ! pkg list-installed "$pkg" > /dev/null 2>&1; then
        echo "${RED}❌ Missing $pkg. Installing...${NC}"
        pkg install "$pkg" -y
    else
        echo "${GREEN}✅ $pkg is installed.${NC}"
    fi
done

# --- 2. Verify Runtimes ---
NODE_VER=$(node -v)
PYTHON_VER=$(python --version)
echo "${GREEN}✅ Node: $NODE_VER${NC}"
echo "${GREEN}✅ Python: $PYTHON_VER${NC}"

# --- 3. Setup Project Structure ---
echo "${YELLOW}📁 Verifying Project Structure...${NC}"
DIRS=("agents" "docs" "mcp" "forge" "src")
for dir in "${DIRS[@]}"; do
    mkdir -p "$dir"
    echo "  - $dir/"
done

# --- 4. Setup Agentic Aliases ---
echo "${YELLOW}⚙️  Configuring Agentic Aliases...${NC}"
FORGE_DIR=$(pwd)
ALIAS_FILE="$FORGE_DIR/forge/aliases.zsh"

if ! grep -q "source $ALIAS_FILE" ~/.zshrc; then
    echo "\n# Crucible Forge Aliases\nsource $ALIAS_FILE" >> ~/.zshrc
    echo "${GREEN}✅ Aliases linked to ~/.zshrc${NC}"
else
    echo "${GREEN}✅ Aliases already linked.${NC}"
fi

# --- 5. Verify MCP Configuration ---
echo "${YELLOW}🔌 Verifying MCP Servers...${NC}"
if ! command -v gemini > /dev/null 2>&1; then
    echo "${YELLOW}⚠️  Gemini CLI not found. To install: npm install -g @google/gemini-cli${NC}"
else
    echo "${GREEN}✅ Gemini CLI detected.${NC}"
fi

# --- 6. Hardware Check (Pixel 9 Pro / Tensor G4) ---
echo "${YELLOW}📱 Hardware Check: Pixel 9 Pro (Tensor G4)${NC}"
if [ -d "/data/data/com.termux/files/home/llama.cpp" ]; then
    echo "${GREEN}✅ llama.cpp detected.${NC}"
else
    echo "${YELLOW}⚠️  llama.cpp not found. Local inference layer missing.${NC}"
fi

echo "${GREEN}✨ Crucible Forge initialized successfully. Restart zsh or 'source ~/.zshrc' to apply aliases.${NC}"

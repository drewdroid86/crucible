#!/bin/zsh

# Crucible Forge: Mobile-First Deployment Pipeline
# A one-touch deploy script for phone-only developers.

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "${BLUE}🚀 Initiating Crucible Mobile Deploy...${NC}"

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "${YELLOW}⚠️ Uncommitted changes detected. Committing...${NC}"
    git add .
    git commit -m "chore: mobile auto-commit via forge deploy"
fi

# Fetch and bump version (semantic)
echo "${YELLOW}📦 Select version bump:${NC}"
echo "1) patch (bug fixes)"
echo "2) minor (new features)"
echo "3) major (breaking changes)"
read "BUMP_CHOICE?Enter choice (1/2/3): "

BUMP_TYPE="patch"
if [ "$BUMP_CHOICE" = "2" ]; then BUMP_TYPE="minor"; fi
if [ "$BUMP_CHOICE" = "3" ]; then BUMP_TYPE="major"; fi

npm version $BUMP_TYPE --no-git-tag-version || echo "${YELLOW}No package.json found. Skipping npm version bump.${NC}"
NEW_VERSION="v$(date +'%Y.%m.%d-%H%M')"

echo "${YELLOW}🔖 Tagging release ${NEW_VERSION}...${NC}"
git add .
git commit -m "release: ${NEW_VERSION}" || true
git tag -a "${NEW_VERSION}" -m "Release ${NEW_VERSION} from Crucible Forge"

echo "${YELLOW}☁️ Pushing to GitHub...${NC}"
git push origin main
git push origin "${NEW_VERSION}"

# Trigger a notification
termux-notification --title "Crucible Deploy Complete" --content "Version ${NEW_VERSION} is live."

echo "${GREEN}✅ Deployment successful! Check your GitHub Actions tab if configured.${NC}"

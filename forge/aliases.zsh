# Crucible Forge: Agentic Aliases
# Optimized for phone-only development speed.

# -- Forge Management --
alias forge-init="/data/data/com.termux/files/home/crucible/forge/init.sh"
alias forge-status="git -C /data/data/com.termux/files/home/crucible status"
alias forge-sync="git -C /data/data/com.termux/files/home/crucible pull origin main"

# -- Agent Shortcuts --
alias g="gemini"
alias gm="gemini mcp"
alias gr="gemini run"

# -- Hardware / Termux Shortcuts --
alias bat="termux-battery-status"
alias notify="termux-notification"
alias clip="termux-clipboard-get"
alias setclip="termux-clipboard-set"

# -- Local LLM (llama.cpp) --
alias llm-start="/data/data/com.termux/files/home/llama.cpp/llama-server"
alias llm-chat="/data/data/com.termux/files/home/llama.cpp/llama-cli"

# -- Quick Project Navigation --
alias cd-crucible="cd /data/data/com.termux/files/home/crucible"
alias cd-forge="cd /data/data/com.termux/files/home/crucible/forge"

echo "⚒️  Crucible Forge Aliases Active."

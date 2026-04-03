# Crucible Forge: Agentic Aliases (v2.1)
# Optimized for Pixel 9 Pro (Tensor G4) + Gemini CLI "New Era"
# Built: April 1, 2026

# -- Forge Management --
alias forge-init="/data/data/com.termux/files/home/crucible/forge/init.sh"
alias forge-status="git -C /data/data/com.termux/files/home/crucible status"
alias forge-sync="git -C /data/data/com.termux/files/home/crucible pull origin main"
alias forge="/data/data/com.termux/files/home/crucible/src/forge-cli.py"

# -- Gemini CLI Shortcuts (The "Powerful" Way) --
alias g="gemini"
alias gm="gemini mcp"
alias gr="gemini run"
alias gi="gemini investigator"
alias gdocs="gemini mcp gemini-docs search"

# -- Local LLM (Ollama) --
alias ol="ollama"
alias ols="ollama list"
alias olr="ollama run"
alias olsrv="ollama serve"

# -- Local LLM (llama.cpp) --
alias llm-start="/data/data/com.termux/files/home/llama.cpp/llama-server"
alias llm-chat="/data/data/com.termux/files/home/llama.cpp/llama-cli"

# -- Hardware / Termux Shortcuts --
alias bat="termux-battery-status"
alias notify="termux-notification"
alias clip="termux-clipboard-get"
alias setclip="termux-clipboard-set"
alias vib="termux-vibrate"
alias cam="termux-camera-photo"
alias mic="termux-microphone-record"
alias t-vol="termux-volume"

# -- Script Shortcuts --
alias get-ol="python3 ~/download_ollama_model.py"
alias sysmon="bash ~/sysmon.sh"
alias voiceai="python3 ~/voice_ai.py"

# -- Quick Project Navigation --
alias cd-crucible="cd /data/data/com.termux/files/home/crucible"
alias cd-forge="cd /data/data/com.termux/files/home/crucible/forge"
alias cd-wga="cd /data/data/com.termux/files/home/WoodGrainAlchemist"
alias cd-crm="cd /data/data/com.termux/files/home/Twisted-Alchemy-CRM"

echo "⚒️  Crucible Forge Aliases Active. (v2.1)"

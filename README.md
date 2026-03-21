# ⚗️ Crucible

**Twisted Alchemy Termux v2.0** — A 9-layer mobile AI development platform running natively on Android (Pixel 9 Pro).

## Stack
- Python 3.13 + Rust 1.94 on Termux
- llama.cpp (Vulkan GPU accelerated) 
- Local OpenAI-compatible API server
- aider AI coding assistant
- HuggingFace model management
- OuteTTS voice synthesis
- XFCE desktop via VNC

## Quick Start
\`\`\`bash
health        # system check
llm "prompt"  # run local LLM
llm-server    # start API server
hf-get repo/model file.gguf  # download model
\`\`\`

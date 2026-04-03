# ⚒️ Crucible Forge

**The Mobile-Native Agentic Development Platform.**

Crucible Forge is a proof of concept and a functional development environment running entirely on a **Pixel 9 Pro (Tensor G4)** via **Termux**. No laptop. No desktop. Just a phone.

It exists to prove that a solo developer can build, ship, and maintain production-grade software using a fully agentic AI stack from anywhere, at any time.

---

## 🌌 The Origin Story
Built at 5:00 AM on **April 1, 2026**. 
The project was conceived and implemented using only an Android phone, under an open sky, with no physical workspace constraints. It is the realization of the "No Walls" development philosophy — where the only limit is the compute in your pocket.

---

## 🏗️ Stack Architecture
Crucible Forge is built in layers, ensuring full control and visibility from the silicon to the agent.

1.  **Hardware Layer**: Google Pixel 9 Pro (Tensor G4, 16GB RAM).
2.  **Base Layer**: Android 15 + [Termux](https://termux.dev/).
3.  **Shell Layer**: `zsh` + [Oh My Zsh](https://ohmyz.sh/) for a robust terminal experience.
4.  **Runtime Layer**: Node.js v25.8.2 + Python 3.13 + Rust 1.94.
5.  **Inference Layer**: `llama.cpp` (ARM64, GGUF) for local LLM execution on the Tensor G4.
6.  **Protocol Layer**: Model Context Protocol (MCP) for connecting tools to agents.
7.  **Agent Layer**: Gemini CLI v0.35.3 (Auto Gemini 3) acting as the primary orchestrator.
8.  **Knowledge Layer**: `gemini-docs` MCP server for real-time API reference.
9.  **Deployment Layer**: `github` MCP server for full repository lifecycle management.

---

## ⚡ Quick Start (For Phone-Only Devs)

### 1. Prerequisite
Install Termux and the following packages:
```bash
pkg update && pkg upgrade
pkg install nodejs-lts python git zsh
```

### 2. Setup Gemini CLI
```bash
npm install -g @google/gemini-cli
gemini authenticate
```

### 3. Connect MCP Servers
```bash
gemini mcp add github
gemini mcp add gemini-docs
```

### 4. Forge Your Environment
```bash
git clone https://github.com/drewdroid86/crucible.git
cd crucible
./forge/init.sh
```

---

## 🗺️ Roadmap
We are just getting started. Crucible Forge is evolving into the ultimate portable forge.

- [ ] **Claude Code Integration**: Adding support for Anthropic's agentic tools.
- [ ] **TurboQuant Local Inference**: Optimizing 4-bit and 8-bit quantization for the Tensor G4.
- [x] **Custom MCP Servers**:
    - `termux-api`: ✅ Control phone hardware (camera, GPS, sensors) via agent.
    - `local-db`: ✅ Direct integration with local SQLite/better-sqlite3.
- [x] **Mobile-First CI/CD**: ✅ Fully automated deployment pipelines triggered from the phone.

---

## 📜 Philosophy
*"Not just another vibe coder."*

Every layer of the stack must be understood, documented, and reproducible. We don't just prompt; we build infrastructure. Crucible Forge is the tool that makes the phone a first-class citizen in the production software ecosystem.

---

**Owner:** Drew (@drewdroid86)  
**License:** Apache 2.0  
**Built on:** Pixel 9 Pro / Tensor G4

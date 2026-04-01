# 🏛️ Crucible Forge: The 9-Layer Stack

Crucible Forge is a mobile-native agentic development platform optimized for the **Google Pixel 9 Pro (Tensor G4)**. This document details each layer of the architecture, its role, and its technical configuration.

---

## 🏗️ The 9 Layers

### 1. Hardware Layer: Pixel 9 Pro (Tensor G4)
- **CPU**: ARMv9 Octa-core (1x 3.1 GHz Cortex-X4, 3x 2.6 GHz Cortex-A720, 4x 1.92 GHz Cortex-A520).
- **GPU**: Mali-G715 (Hardware acceleration for `llama.cpp` via Vulkan).
- **RAM**: 16GB LPDDR5X (Crucial for multi-agent orchestration and local LLM context).
- **Optimization**: Tensor G4's dedicated NPU and power efficiency are primary targets for upcoming `TurboQuant` optimizations.

### 2. Base Layer: Android 15 + Termux
- **Base OS**: Android 15 (Native Linux kernel access).
- **Environment**: [Termux](https://termux.dev/) (v0.118+) provides a complete, sandboxed Linux distribution.
- **Packages**: Managed via `pkg` (apt-based) with access to `x11-repo` for desktop-class tooling.

### 3. Shell Layer: zsh + Oh My Zsh
- **Interface**: `zsh` 5.9+.
- **Configuration**: `Oh My Zsh` for enhanced prompt visibility and git integration.
- **Forge Aliases**: Specialized `forge/aliases.zsh` for one-tap mobile development (e.g., `bat` for battery, `g` for gemini).

### 4. Runtime Layer: Node.js + Python + Rust
- **Node.js**: v25.8.2 (Primary for MCP servers and web development).
- **Python**: v3.13 (Primary for AI/ML scripts and `termux-api` utilities).
- **Rust**: v1.94 (Used for high-performance system tooling and `llama.cpp` components).

### 5. Inference Layer: llama.cpp (Local)
- **Engine**: `llama.cpp` compiled natively for ARM64 with Vulkan acceleration.
- **Models**: GGUF format (e.g., Llama 3 8B, Phi-3).
- **Quantization**: Primarily Q4_K_M for optimal performance/memory ratio on mobile.

### 6. Protocol Layer: Model Context Protocol (MCP)
- **Framework**: [Model Context Protocol](https://modelcontextprotocol.io/) (MCP).
- **Standard**: JSON-RPC over `stdio` for connecting agents to tools.
- **Custom Hardware Bridge**: `mcp/termux-api` for direct Android sensor/hardware control.

### 7. Agent Layer: Gemini CLI (Orchestrator)
- **Tool**: [Gemini CLI v0.35.3+](https://github.com/google/gemini-cli).
- **Model**: Gemini 2.0 / 1.5 Pro (Auto Gemini 3 Mode).
- **Role**: The "Command Center" that researches, writes code, and executes shell commands autonomously.

### 8. Knowledge Layer: Gemini API Docs
- **Source**: `gemini-docs` MCP server.
- **Capability**: Real-time access to the latest Gemini API and SDK documentation, ensuring the agent remains expert-level.

### 9. Deployment Layer: GitHub MCP
- **Management**: Direct integration with the `github` MCP server.
- **Workflow**: Create repos, pull requests, and commit code directly from the phone.
- **Repository**: [drewdroid86/crucible](https://github.com/drewdroid86/crucible).

---

## 📜 Philosophy: "No Walls"
Crucible Forge proves that the "laptop" is a legacy constraint. By understanding and owning every layer from the silicon up, we transform a mobile device into a first-class citizen of the production software ecosystem.

---
*Built: April 1, 2026 @ 05:00 AM*

#!/bin/zsh

# Crucible Forge: Local Inference Manager
# Optimized for Pixel 9 Pro (Tensor G4, 16GB RAM)

MODEL_DIR="/data/data/com.termux/files/home/llama.cpp/models"
# We recommend Phi-3-mini or Llama-3-8B-Instruct in Q4_K_M for Android
DEFAULT_MODEL="Phi-3-mini-4k-instruct-q4.gguf"
MODEL_URL="https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"

# Ensure the model directory exists
mkdir -p "$MODEL_DIR"

if [ "$1" = "download" ]; then
    echo "📥 Downloading optimized $DEFAULT_MODEL for Tensor G4..."
    curl -L -o "$MODEL_DIR/$DEFAULT_MODEL" "$MODEL_URL"
    echo "✅ Download complete."
    exit 0
fi

if [ "$1" = "start" ]; then
    if [ ! -f "$MODEL_DIR/$DEFAULT_MODEL" ]; then
        echo "❌ Model not found at $MODEL_DIR/$DEFAULT_MODEL"
        echo "Run './llm-manager.sh download' first."
        exit 1
    fi

    echo "🚀 Starting llama-server optimized for Tensor G4..."
    # Tensor G4 Optimization Flags:
    # -c 4096: Context window size
    # -t 8: 8 threads (matches octa-core Tensor G4)
    # -ngl 99: Offload all layers to GPU (if Vulkan compiled)
    /data/data/com.termux/files/home/llama.cpp/llama-server \
        -m "$MODEL_DIR/$DEFAULT_MODEL" \
        -c 4096 \
        -t 8 \
        --host 127.0.0.1 --port 8080
    exit 0
fi

echo "Usage: ./llm-manager.sh [download|start]"

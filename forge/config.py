import os
from pathlib import Path

FORGE_DIR = Path(__file__).parent
MEMORY_DIR = FORGE_DIR / ".memory"
MEMORY_DIR.mkdir(exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LOCAL_API_BASE = os.getenv("LOCAL_API_BASE", "http://localhost:8080/v1")
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "local")

BRAINS = {
    "gemini": {"name": "Gemini Pro", "available": bool(GEMINI_API_KEY)},
    "claude": {"name": "Claude", "available": bool(CLAUDE_API_KEY)},
    "local": {"name": "Local (llama.cpp)", "available": True},
}

DEFAULT_BRAIN = "gemini" if GEMINI_API_KEY else "local"

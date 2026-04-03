import json
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import MEMORY_DIR


def _mem_path(project: str) -> Path:
    return MEMORY_DIR / f"{project}.json"


def load_memory(project: str) -> dict:
    p = _mem_path(project)
    if p.exists():
        return json.loads(p.read_text())
    return {"project": project, "created": datetime.now().isoformat(), "history": [], "notes": []}


def save_memory(project: str, mem: dict):
    _mem_path(project).write_text(json.dumps(mem, indent=2))


def add_message(project: str, role: str, content: str):
    mem = load_memory(project)
    mem["history"].append({
        "role": role,
        "content": content,
        "ts": datetime.now().isoformat(),
    })
    # Keep last 50 messages to avoid bloat
    mem["history"] = mem["history"][-50:]
    save_memory(project, mem)


def add_note(project: str, note: str):
    mem = load_memory(project)
    mem["notes"].append({"note": note, "ts": datetime.now().isoformat()})
    save_memory(project, mem)


def get_history(project: str) -> list:
    """Return messages in LLM format."""
    mem = load_memory(project)
    return [{"role": m["role"], "content": m["content"]} for m in mem["history"]]


def list_projects() -> list:
    return [p.stem for p in MEMORY_DIR.glob("*.json")]


def clear_memory(project: str):
    p = _mem_path(project)
    if p.exists():
        p.unlink()

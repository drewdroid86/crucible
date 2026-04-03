import httpx
import json
import sys
import os

sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))
from config import GEMINI_API_KEY, CLAUDE_API_KEY, LOCAL_API_BASE, LOCAL_MODEL, DEFAULT_BRAIN


def _gemini(messages: list, tools: list) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key={GEMINI_API_KEY}"
    contents = []
    system = None
    for m in messages:
        if m["role"] == "system":
            system = m["content"]
        elif m["role"] == "user":
            contents.append({"role": "user", "parts": [{"text": m["content"]}]})
        elif m["role"] == "assistant":
            contents.append({"role": "model", "parts": [{"text": m["content"]}]})

    payload = {"contents": contents}
    if system:
        payload["system_instruction"] = {"parts": [{"text": system}]}

    if tools:
        fn_decls = []
        for t in tools:
            fn_decls.append({
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"],
            })
        pass  # tools disabled temporarily

    resp = httpx.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    content = data.get("candidates", [{}])[0].get("content", {}) 
    if "parts" not in content: print(f"DEBUG: Raw response: {data}"); return "Error: No parts in response." 
    candidate = next((p for p in content["parts"] if "functionCall" in p), content["parts"][0])
    if "functionCall" in candidate:
        fc = candidate["functionCall"]
        return {"type": "tool_call", "name": fc["name"], "args": fc["args"]}
    return {"type": "text", "content": candidate.get("text", "")}


def _claude(messages: list, tools: list) -> dict:
    system = None
    filtered = []
    for m in messages:
        if m["role"] == "system":
            system = m["content"]
        else:
            filtered.append(m)

    payload = {
        "model": "claude-opus-4-5",
        "max_tokens": 4096,
        "messages": filtered,
    }
    if system:
        payload["system"] = system
    if tools:
        payload["tools"] = [
            {
                "name": t["name"],
                "description": t["description"],
                "input_schema": t["parameters"],
            }
            for t in tools
        ]

    resp = httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()

    for block in data["content"]:
        if block["type"] == "tool_use":
            return {"type": "tool_call", "name": block["name"], "args": block["input"]}
    text = " ".join(b.get("text", "") for b in data["content"] if b["type"] == "text")
    return {"type": "text", "content": text}


def _local(messages: list, tools: list) -> dict:
    payload = {
        "model": LOCAL_MODEL,
        "messages": messages,
        "max_tokens": 2048,
        "temperature": 0.7,
    }
    resp = httpx.post(
        f"{LOCAL_API_BASE}/chat/completions",
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    return {"type": "text", "content": content}


BRAIN_FNS = {
    "gemini": _gemini,
    "claude": _claude,
    "local": _local,
}


def auto_select_brain(task: str) -> str:
    """Pick best brain based on task keywords."""
    task_lower = task.lower()
    if any(w in task_lower for w in ["review", "architecture", "explain", "refactor"]):
        return "claude" if CLAUDE_API_KEY else DEFAULT_BRAIN
    if any(w in task_lower for w in ["search", "find", "what is", "latest"]):
        return "gemini" if GEMINI_API_KEY else DEFAULT_BRAIN
    if any(w in task_lower for w in ["quick", "local", "private", "fast"]):
        return "local"
    return DEFAULT_BRAIN


def call_brain(brain: str, messages: list, tools: list = None) -> dict:
    """Call the selected brain and return a response dict."""
    fn = BRAIN_FNS.get(brain)
    if not fn:
        return {"type": "text", "content": f"[error] Unknown brain: {brain}"}
    return fn(messages, tools or [])

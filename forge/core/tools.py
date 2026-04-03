import subprocess
import httpx
from pathlib import Path


# ── Registry ──────────────────────────────────────────────────────────────────
TOOLS = {}

def tool(name, description, params):
    """Decorator to register a tool."""
    def decorator(fn):
        TOOLS[name] = {
            "name": name,
            "description": description,
            "params": params,
            "fn": fn,
        }
        return fn
    return decorator


def get_tool_schemas():
    """Return tool definitions for LLM function-calling."""
    return [
        {
            "name": t["name"],
            "description": t["description"],
            "parameters": {
                "type": "object",
                "properties": t["params"],
                "required": list(t["params"].keys()),
            },
        }
        for t in TOOLS.values()
    ]


def run_tool(name: str, args: dict) -> str:
    """Execute a tool by name and return string output."""
    if name not in TOOLS:
        return f"[error] Unknown tool: {name}"
    try:
        return TOOLS[name]["fn"](**args)
    except Exception as e:
        return f"[error] {name} failed: {e}"


# ── File Tools ─────────────────────────────────────────────────────────────────
@tool(
    name="read_file",
    description="Read the contents of a file.",
    params={"path": {"type": "string", "description": "Absolute or relative file path"}},
)
def read_file(path: str) -> str:
    p = Path(path).expanduser()
    if not p.exists():
        return f"[error] File not found: {path}"
    return p.read_text(errors="replace")


@tool(
    name="write_file",
    description="Write or overwrite a file with given content.",
    params={
        "path": {"type": "string", "description": "File path to write"},
        "content": {"type": "string", "description": "Content to write"},
    },
)
def write_file(path: str, content: str) -> str:
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return f"✅ Written: {path} ({len(content)} chars)"


@tool(
    name="list_dir",
    description="List files and directories at a path.",
    params={"path": {"type": "string", "description": "Directory path"}},
)
@tool(
    name="list_dir",
    description="Lists the contents of a directory.",
    params={"path": {"type": "string", "description": "The directory path to list"}}
)
def list_dir(path: str) -> str:
    p = Path(path).expanduser()
    if not p.exists():
        return f"[error] Path not found: {path}"
    entries = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name))
    lines = []
    for e in entries:
        prefix = "📁" if e.is_dir() else "📄"
        lines.append(f"{prefix} {e.name}")
    return "\n".join(lines) or "(empty)"


# ── Bash Tool ──────────────────────────────────────────────────────────────────
@tool(
    name="run_bash",
    description="Run a bash command and return stdout + stderr. Termux-native.",
    params={"command": {"type": "string", "description": "Shell command to execute"}},
)
def run_bash(command: str) -> str:
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=60,
        executable="/data/data/com.termux/files/usr/bin/bash",
    )
    out = result.stdout.strip()
    err = result.stderr.strip()
    parts = []
    if out:
        parts.append(out)
    if err:
        parts.append(f"[stderr]\n{err}")
    return "\n".join(parts) or "(no output)"


# ── Git Tools ──────────────────────────────────────────────────────────────────
def _git(args: str, cwd: str = ".") -> str:
    return run_bash(f"cd {cwd} && git {args}")


@tool(
    name="git_status",
    description="Show git status of a repository.",
    params={"path": {"type": "string", "description": "Repo directory path"}},
)
def git_status(path: str) -> str:
    return _git("status --short", cwd=path)


@tool(
    name="git_diff",
    description="Show unstaged or staged git diff.",
    params={
        "path": {"type": "string", "description": "Repo directory path"},
        "staged": {"type": "boolean", "description": "Show staged diff if true"},
    },
)
def git_diff(path: str, staged: bool = False) -> str:
    flag = "--cached" if staged else ""
    return _git(f"diff {flag}", cwd=path)


@tool(
    name="git_commit",
    description="Stage all changes and commit with a message.",
    params={
        "path": {"type": "string", "description": "Repo directory path"},
        "message": {"type": "string", "description": "Commit message"},
    },
)
def git_commit(path: str, message: str) -> str:
    _git("add -A", cwd=path)
    return _git(f'commit -m "{message}"', cwd=path)


@tool(
    name="git_log",
    description="Show recent git commit log.",
    params={
        "path": {"type": "string", "description": "Repo directory path"},
        "n": {"type": "integer", "description": "Number of commits to show"},
    },
)
def git_log(path: str, n: int = 10) -> str:
    return _git(f"log --oneline -{n}", cwd=path)


# ── Web Search Tool ────────────────────────────────────────────────────────────
@tool(
    name="web_search",
    description="Search the web using DuckDuckGo and return top results.",
    params={"query": {"type": "string", "description": "Search query"}},
)
def web_search(query: str) -> str:
    try:
        resp = httpx.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=10,
        )
        data = resp.json()
        results = []
        if data.get("AbstractText"):
            results.append(f"📖 {data['AbstractText']}\n   {data.get('AbstractURL', '')}")
        for r in data.get("RelatedTopics", [])[:5]:
            if isinstance(r, dict) and r.get("Text"):
                results.append(f"• {r['Text']}\n  {r.get('FirstURL', '')}")
        return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        return f"[error] Web search failed: {e}"

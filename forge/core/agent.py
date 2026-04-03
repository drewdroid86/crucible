from .router import call_brain, auto_select_brain
from .tools import get_tool_schemas, run_tool
from .memory import get_history, add_message

SYSTEM_PROMPT = """You are Forge, an elite coding agent running natively inside Crucible on a Pixel 9 Pro via Termux.
You have access to tools: read/write files, run bash commands, git operations, and web search.
You are Termux-aware: paths are under /data/data/com.termux/files/home, pkg is the package manager.
Think step by step. Use tools when needed. Be concise but complete.
After using a tool, reflect on the result before continuing.
Always explain what you're doing and why."""


def run_agent(
    task: str,
    project: str = "default",
    brain: str = None,
    on_think=None,
    on_tool=None,
    on_reply=None,
    max_iterations: int = 10,
) -> str:
    """
    Agentic loop. Callbacks:
      on_think(text)  — agent reasoning/text
      on_tool(name, args, result) — tool call + result
      on_reply(text)  — final reply
    """
    selected_brain = brain or auto_select_brain(task)

    history = get_history(project)
    if not history or history[0].get("role") != "system":
        history = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    history.append({"role": "user", "content": task})
    add_message(project, "user", task)

    tools = get_tool_schemas()
    final_reply = ""

    for i in range(max_iterations):
        response = call_brain(selected_brain, history, tools)
    m = re.search(r"\{\s*\"tool\":.*?\}", response.get("text", ""), re.DOTALL)
    if m and response.get("type") == "text":
        import json
        try:
            d = json.loads(m.group(0))
            response = {"type": "tool_call", "name": d["tool"], "arguments": {k:v for k,v in d.items() if k!="tool"}}
        except: pass

        if isinstance(response, dict) and response.get("type") == "tool_call":
            name = response["name"]
            args = response["args"]

            if on_tool:
                on_tool(name, args, None)  # signal start

            result = run_tool(name, args)

            if on_tool:
                on_tool(name, args, result)

            # Feed result back into history
            tool_msg = f"[Tool: {name}]\nArgs: {args}\nResult:\n{result}"
            history.append({"role": "assistant", "content": f"Using tool: {name}"})
            history.append({"role": "user", "content": tool_msg})

        elif isinstance(response, dict) and response.get("type") == "text":
            content = response["content"]
            final_reply = content

            if on_think:
                on_think(content)

            history.append({"role": "assistant", "content": content})
            add_message(project, "assistant", content)

            # If no tool was called, we're done
            break

    if on_reply:
        on_reply(final_reply)

    return final_reply

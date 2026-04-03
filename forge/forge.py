#!/usr/bin/env python3
"""
forge — Crucible Coding Agent
Usage:
  forge                          # TUI mode
  forge --cli                    # CLI mode
  forge --cli -p crm -b gemini   # CLI with project + brain
  forge "do this task"           # one-shot CLI
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def main():
    parser = argparse.ArgumentParser(
        prog="forge",
        description="🔥 Forge — Crucible Coding Agent"
    )
    parser.add_argument("task", nargs="?", help="One-shot task")
    parser.add_argument("--cli", action="store_true", help="CLI mode (no TUI)")
    parser.add_argument("-p", "--project", default="default", help="Project name")
    parser.add_argument("-b", "--brain", default=None, help="Brain: gemini | claude | local")
    parser.add_argument("--list-projects", action="store_true", help="List all projects")

    args = parser.parse_args()

    if args.list_projects:
        from core.memory import list_projects
        projects = list_projects()
        print("Projects:", ", ".join(projects) if projects else "none")
        return

    if args.task:
        # One-shot mode
        from rich.console import Console
        from rich.markdown import Markdown
        from core.agent import run_agent
        from core.router import auto_select_brain

        console = Console()
        brain = args.brain or auto_select_brain(args.task)
        console.print(f"[dim]🧠 {brain} | project: {args.project}[/dim]")

        def on_tool(name, a, result):
            if result:
                console.print(f"[yellow]⚙ {name}[/yellow] → {str(result)[:200]}")

        def on_reply(text):
            console.print(Markdown(text))

        run_agent(
            task=args.task,
            project=args.project,
            brain=brain,
            on_tool=on_tool,
            on_reply=on_reply,
        )

    elif args.cli:
        from ui.cli import cli_loop
        cli_loop(project=args.project, brain=args.brain)

    else:
        from ui.tui import launch_tui
        launch_tui(project=args.project, brain=args.brain)


if __name__ == "__main__":
    main()

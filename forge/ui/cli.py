import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

from core.agent import run_agent
from core.router import auto_select_brain
from core.memory import list_projects, clear_memory
from config import DEFAULT_BRAIN

console = Console()


def print_banner():
    console.print(Panel.fit(
        "[bold red]🔥 FORGE[/bold red] [dim]— Crucible Coding Agent[/dim]",
        border_style="red"
    ))


def cli_loop(project: str = "default", brain: str = None):
    print_banner()
    console.print(f"[dim]Project:[/dim] [cyan]{project}[/cyan]  [dim]Brain:[/dim] [yellow]{brain or auto_select_brain('default')}[/yellow]")
    console.print("[dim]Commands: /brain <name> | /project <name> | /clear | /exit[/dim]\n")

    current_brain = brain

    while True:
        try:
            user_input = Prompt.ask("[bold red]forge[/bold red]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not user_input.strip():
            continue

        # Commands
        if user_input.startswith("/exit"):
            console.print("[dim]Goodbye.[/dim]")
            break
        elif user_input.startswith("/brain "):
            current_brain = user_input.split(" ", 1)[1].strip()
            console.print(f"[yellow]Brain switched to: {current_brain}[/yellow]")
            continue
        elif user_input.startswith("/project "):
            project = user_input.split(" ", 1)[1].strip()
            console.print(f"[cyan]Project switched to: {project}[/cyan]")
            continue
        elif user_input.startswith("/clear"):
            clear_memory(project)
            console.print(f"[dim]Memory cleared for project: {project}[/dim]")
            continue
        elif user_input.startswith("/projects"):
            projects = list_projects()
            console.print("[dim]Projects:[/dim] " + ", ".join(projects) if projects else "[dim]No projects yet.[/dim]")
            continue

        # Run agent
        selected = current_brain or auto_select_brain(user_input)
        console.print(f"[dim]🧠 {selected}[/dim]")

        def on_tool(name, args, result):
            if result is None:
                console.print(f"[yellow]⚙ {name}[/yellow] [dim]{args}[/dim]")
            else:
                console.print(Panel(result[:1000], title=f"[yellow]{name}[/yellow]", border_style="yellow"))

        def on_reply(text):
            console.print(Markdown(text))

        run_agent(
            task=user_input,
            project=project,
            brain=selected,
            on_tool=on_tool,
            on_reply=on_reply,
        )
        console.print()

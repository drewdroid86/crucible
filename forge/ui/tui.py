import sys
import threading
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog, Static
from textual.containers import Horizontal, Vertical
from textual import work

from core.agent import run_agent
from core.router import auto_select_brain
from config import DEFAULT_BRAIN


class ForgeApp(App):
    CSS = """
    Screen {
        background: #0d0d0d;
    }
    #top {
        height: 1fr;
    }
    #think-panel {
        width: 2fr;
        border: solid #333;
        padding: 1;
    }
    #chat-panel {
        width: 3fr;
        border: solid #333;
        padding: 1;
    }
    #tool-panel {
        height: 10;
        border: solid #ff4500;
        padding: 1;
    }
    #status {
        height: 1;
        background: #1a1a1a;
        color: #666;
        padding: 0 1;
    }
    Input {
        border: solid #ff4500;
        background: #1a1a1a;
    }
    RichLog {
        scrollbar-color: #333;
    }
    """

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+l", "clear", "Clear"),
    ]

    def __init__(self, project="default", brain=None):
        super().__init__()
        self.project = project
        self.brain = brain
        self.selected_brain = brain or DEFAULT_BRAIN

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(
            f" 🔥 FORGE  |  Project: {self.project}  |  Brain: {self.selected_brain}",
            id="status"
        )
        with Horizontal(id="top"):
            yield RichLog(id="think-panel", highlight=True, markup=True, wrap=True)
            yield RichLog(id="chat-panel", highlight=True, markup=True, wrap=True)
        yield RichLog(id="tool-panel", highlight=True, markup=True, wrap=True)
        yield Input(placeholder="Ask forge anything... (/brain gemini | /project crm | /exit)")
        yield Footer()

    def on_mount(self):
        think = self.query_one("#think-panel", RichLog)
        chat = self.query_one("#chat-panel", RichLog)
        tool = self.query_one("#tool-panel", RichLog)

        think.write("[dim]Agent reasoning will appear here[/dim]")
        chat.write("[bold red]🔥 FORGE[/bold red] online. What do you want to build?")
        tool.write("[dim]Tool calls will stream here[/dim]")

        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted):
        user_input = event.value.strip()
        if not user_input:
            return
        event.input.value = ""

        if user_input == "/exit":
            self.exit()
            return
        elif user_input.startswith("/brain "):
            self.selected_brain = user_input.split(" ", 1)[1].strip()
            self.query_one("#status", Static).update(
                f" 🔥 FORGE  |  Project: {self.project}  |  Brain: {self.selected_brain}"
            )
            return
        elif user_input.startswith("/project "):
            self.project = user_input.split(" ", 1)[1].strip()
            self.query_one("#status", Static).update(
                f" 🔥 FORGE  |  Project: {self.project}  |  Brain: {self.selected_brain}"
            )
            return

        chat = self.query_one("#chat-panel", RichLog)
        chat.write(f"\n[bold cyan]You:[/bold cyan] {user_input}")

        self.run_agent_async(user_input)

    @work(thread=True)
    def run_agent_async(self, task: str):
        think = self.query_one("#think-panel", RichLog)
        chat = self.query_one("#chat-panel", RichLog)
        tool = self.query_one("#tool-panel", RichLog)

        selected = self.brain or auto_select_brain(task)
        self.call_from_thread(think.write, f"\n[dim]🧠 Routing to: {selected}[/dim]")

        def on_think(text):
            self.call_from_thread(think.write, f"\n[dim]{text[:500]}[/dim]")

        def on_tool(name, args, result):
            if result is None:
                self.call_from_thread(tool.write, f"[yellow]⚙ {name}[/yellow] {args}")
            else:
                self.call_from_thread(tool.write, f"[green]✓ {name}[/green]\n{str(result)[:300]}")

        def on_reply(text):
            self.call_from_thread(chat.write, f"\n[bold red]Forge:[/bold red] {text}")

        run_agent(
            task=task,
            project=self.project,
            brain=selected,
            on_think=on_think,
            on_tool=on_tool,
            on_reply=on_reply,
        )

    def action_clear(self):
        for panel_id in ["#think-panel", "#chat-panel", "#tool-panel"]:
            self.query_one(panel_id, RichLog).clear()


def launch_tui(project="default", brain=None):
    ForgeApp(project=project, brain=brain).run()

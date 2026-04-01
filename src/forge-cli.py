#!/usr/bin/env python3

"""
Crucible Forge Mobile Dashboard
A rich, mobile-optimized CLI dashboard to check system and AI health on the Pixel 9 Pro.
"""

import json
import subprocess
import os
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text

console = Console()

def get_battery():
    try:
        out = subprocess.check_output("termux-battery-status", shell=True, text=True)
        data = json.loads(out)
        level = data.get("percentage", "?")
        status = data.get("status", "UNKNOWN")
        color = "green" if level > 20 else "red"
        return f"[{color}]{level}% ({status})[/{color}]"
    except Exception:
        return "[red]Unknown[/red]"

def check_llm_running():
    try:
        # Check if llama-server is listening on port 8080
        out = subprocess.check_output("ps -A | grep llama-server", shell=True, text=True)
        return bool(out.strip())
    except subprocess.CalledProcessError:
        return False

def get_recent_commits():
    try:
        repo_dir = "/data/data/com.termux/files/home/crucible"
        out = subprocess.check_output(f"git -C {repo_dir} log -3 --oneline", shell=True, text=True)
        return out.strip()
    except Exception:
        return "[red]Not a git repo or no commits[/red]"

def main():
    console.print("\n[bold cyan]⚒️ Crucible Forge Dashboard[/bold cyan]", justify="center")
    
    # System Panel
    sys_table = Table(show_header=False, expand=True, box=None)
    sys_table.add_column("Key", style="bold yellow")
    sys_table.add_column("Value")
    sys_table.add_row("📱 Hardware", "Pixel 9 Pro (Tensor G4)")
    sys_table.add_row("🔋 Battery", get_battery())
    sys_table.add_row("🧠 Local LLM", "[green]Online (Port 8080)[/green]" if check_llm_running() else "[yellow]Offline (Run llm-start)[/yellow]")
    
    sys_panel = Panel(sys_table, title="[bold]System Status[/bold]", border_style="blue")

    # Git Panel
    git_panel = Panel(get_recent_commits(), title="[bold]Recent Forges (Commits)[/bold]", border_style="magenta")

    # Layout
    layout = Layout()
    layout.split_column(
        Layout(sys_panel, size=6),
        Layout(git_panel)
    )
    
    console.print(layout)

if __name__ == "__main__":
    main()

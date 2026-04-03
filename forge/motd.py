#!/usr/bin/env python3
"""
motd.py — Forge startup screen
Runs at shell login via .zshrc
"""
import subprocess
import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from rich.console import Console
    from rich.text import Text
    from rich.columns import Columns
    from rich.panel import Panel
    from rich import print as rprint
except ImportError:
    sys.exit(0)

console = Console()
HOME = Path.home()


# ── data collectors ───────────────────────────────────────────────────────────

def get_ram():
    try:
        mem = {}
        with open('/proc/meminfo') as f:
            for line in f:
                k, *v = line.split()
                if k in ('MemTotal:', 'MemAvailable:'):
                    mem[k] = int(v[0])
        total = mem['MemTotal:'] / 1024 / 1024
        avail = mem['MemAvailable:'] / 1024 / 1024
        used  = total - avail
        pct   = used / total * 100
        return used, total, pct
    except Exception:
        return 0, 15, 0

def get_battery():
    try:
        # Added a 2-second timeout to prevent the 'abort' crash
        r = subprocess.run(['termux-battery-status'],
                           capture_output=True, text=True, timeout=2)
        if r.returncode == 0:
            d = json.loads(r.stdout)
            return d.get('percentage', 0), d.get('status', '') == 'CHARGING'
    except Exception:
        pass
    return 0, False


def get_storage():
    try:
        r = subprocess.run(
            ['df', '-h', '/data/data/com.termux'],
            capture_output=True, text=True, timeout=2)
        parts = r.stdout.strip().split('\n')[-1].split()
        return parts[3] if len(parts) > 3 else '?'
    except Exception:
        return '?'

def check_proc(name):
    """Check if a process is running."""
    try:
        r = subprocess.run(['pgrep', '-x', name],
                           capture_output=True, timeout=2)
        return r.returncode == 0
    except Exception:
        return False

def check_cmd(cmd):
    """Check if a command exists and runs."""
    try:
        r = subprocess.run([cmd, '--version'],
                           capture_output=True, timeout=2)
        return r.returncode == 0
    except Exception:
        return False

def get_models():
    """Count GGUF models."""
    models_dir = HOME / 'models'
    try:
        gguf = list(models_dir.glob('*.gguf'))
        if not gguf:
            gguf = list(HOME.glob('*.gguf'))
        total_gb = sum(f.stat().st_size for f in gguf) / 1e9
        return len(gguf), total_gb
    except Exception:
        return 0, 0

def get_git_status(path):
    """Return dirty/clean/absent for a repo."""
    try:
        r = subprocess.run(
            ['git', '-C', str(path), 'status', '--porcelain'],
            capture_output=True, text=True, timeout=3)
        if r.returncode != 0:
            return None
        return 'dirty' if r.stdout.strip() else 'clean'
    except Exception:
        return None

def get_tmux_sessions():
    """List tmux session names."""
    try:
        r = subprocess.run(
            ['tmux', 'list-sessions', '-F', '#{session_name}'],
            capture_output=True, text=True, timeout=2)
        if r.returncode == 0:
            return r.stdout.strip().split('\n')
        return []
    except Exception:
        return []

def vulkan_active():
    bins = [
        HOME / 'llama.cpp/build/bin/llama-cli',
        HOME / 'llama.cpp/bin/llama-cli'
    ]
    for b in bins:
        if b.exists():
            try:
                # Capture both stdout and stderr
                r = subprocess.run([str(b), '--version'], 
                                   capture_output=True, text=True, timeout=5)
                full_out = (r.stdout + r.stderr).upper()
                if 'VULKAN' in full_out or 'GGML_VULKAN' in full_out:
                    return True
            except Exception:
                pass
    return False



# ── renderers ─────────────────────────────────────────────────────────────────

def bar(pct, width=12, warn=70, crit=90):
    filled = int(pct / 100 * width)
    empty  = width - filled
    color  = 'red' if pct >= crit else ('yellow' if pct >= warn else 'cyan')
    b = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
    return b

def dot(ok):
    return '[green]●[/green]' if ok else '[dim]○[/dim]'

def git_badge(status):
    if status is None:   return '[dim]–[/dim]'
    if status == 'dirty': return '[yellow]dirty[/yellow]'
    return '[green]clean[/green]'


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    now = datetime.now()

    # collect
    ram_used, ram_total, ram_pct = get_ram()
    bat_pct, charging            = get_battery()
    storage                      = get_storage()
    model_count, model_gb        = get_models()
    tmux_sessions                = get_tmux_sessions()
    gemini_ok  = check_cmd('gemini')
    ollama_ok  = check_proc('ollama')
    llama_ok   = (HOME / 'llama.cpp' / 'build' / 'bin' / 'llama-cli').exists()
    vulkan_ok  = vulkan_active()

    # git repos
    repos = {
        'crucible':  HOME / 'crucible',
        'crm':       HOME / 'Twisted-Alchemy-CRM',
        'wga':       HOME / 'WoodGrainAlchemist',
    }
    git_states = {k: get_git_status(v) for k, v in repos.items()}

    bat_color = 'red' if bat_pct < 20 else ('yellow' if bat_pct < 40 else 'green')
    bat_tag   = f"{'⚡' if charging else '·'} {bat_pct}%"

    # ── header
    console.print()
    console.print(
        f"  [bold #f59e0b]⚡ FORGE[/bold #f59e0b]  "
        f"[dim]Crucible · Twisted Alchemy[/dim]  "
        f"[dim]{now.strftime('%a %H:%M')}[/dim]"
    )
    console.print(f"  [dim]Pixel 9 Pro · Tensor G4 · Mali-G715 · aarch64[/dim]")
    console.print()

    # ── system
    console.print(f"  [bold #555555]SYSTEM[/bold #555555]")
    console.print(
        f"  [#22d3ee]RAM [/#22d3ee] {bar(ram_pct)}  "
        f"[dim]{ram_used:.1f}/{ram_total:.1f} GiB[/dim]"
    )
    console.print(
        f"  [#22d3ee]BAT [/#22d3ee] {bar(bat_pct, warn=40, crit=20)}  "
        f"[{bat_color}]{bat_tag}[/{bat_color}]"
    )
    console.print(
        f"  [#22d3ee]DISK[/#22d3ee] [dim]──────────────[/dim]  "
        f"[green]{storage} free[/green]"
    )
    console.print()

    # ── ai engines
    console.print(f"  [bold #555555]AI ENGINES[/bold #555555]")
    console.print(
        f"  {dot(gemini_ok)} [white]Gemini CLI[/white]   "
        f"{'[green]ACTIVE[/green]' if gemini_ok else '[dim]OFFLINE[/dim]'}"
    )
    console.print(
        f"  {dot(ollama_ok)} [white]Ollama[/white]       "
        f"{'[green]RUNNING[/green]' if ollama_ok else '[dim]OFFLINE[/dim]  [dim]→ ol[/dim]'}"
    )
    console.print(
        f"  {dot(llama_ok)} [white]llama.cpp[/white]    "
        f"{'[green]BUILT[/green]' if llama_ok else '[dim]NOT BUILT[/dim]'}  "
        f"{'[#f59e0b]VULKAN ⚡[/#f59e0b]' if vulkan_ok else '[dim]CPU only[/dim]'}"
    )
    if model_count > 0:
        console.print(
            f"  [dim]  models: {model_count} files · {model_gb:.1f} GB[/dim]"
        )
    console.print()

    # ── repos
    console.print(f"  [bold #555555]REPOS[/bold #555555]")
    for name, status in git_states.items():
        console.print(f"  [#22d3ee]{name:<12}[/#22d3ee]  {git_badge(status)}")
    console.print()

    # ── tmux
    if tmux_sessions:
        sessions_str = '  '.join(f'[#f59e0b]{s}[/#f59e0b]' for s in tmux_sessions if s)
        console.print(f"  [bold #555555]TMUX[/bold #555555]  {sessions_str}")
        console.print()

    # ── quick ref
    console.print(f"  [bold #555555]COMMANDS[/bold #555555]")
    cmds = [
        ('forge', 'AI agent TUI'),
        ('gi',    'Gemini Investigator'),
        ('crm',   'Twisted Alchemy CRM'),
        ('wga',   'Wood Grain Alchemist'),
        ('ol',    'Ollama Manager'),
        ('llm',   'Launch Model'),
        ('mux',   'New tmux session'),
        ('sys',   'System stats'),
    ]
    for i in range(0, len(cmds), 2):
        left  = cmds[i]
        right = cmds[i+1] if i+1 < len(cmds) else None
        line  = f"  [#f59e0b]{left[0]:<6}[/#f59e0b] [dim]{left[1]:<22}[/dim]"
        if right:
            line += f"  [#f59e0b]{right[0]:<6}[/#f59e0b] [dim]{right[1]}[/dim]"
        console.print(line)

    console.print()


if __name__ == '__main__':
    main()
import os; os._exit(0)

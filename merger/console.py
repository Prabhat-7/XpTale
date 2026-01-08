import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()

class ConsoleStyle:
    @staticmethod
    def print_section(title):
        """Prints a styled box around the section title."""
        console.print(Panel(f"[bold magenta]{title}[/bold magenta]", expand=False, border_style="bold magenta"))

    @staticmethod
    def print_step(msg):
        """Prints a processing step."""
        console.print(f"[cyan]  ➜ {msg}[/cyan]")

    @staticmethod
    def print_sub_step(msg):
        """Prints a sub-step detail."""
        console.print(f"    [blue]↳ {msg}[/blue]")

    @staticmethod
    def print_success(msg):
        """Prints a success message."""
        console.print(f"[green]  ✔ {msg}[/green]")
    @staticmethod
    def print_warning(msg):
        """Prints a warning message."""
        console.print(f"[yellow]  ⚠ {msg}[/yellow]")

    @staticmethod
    def print_error(msg):
        """Prints an error message."""
        console.print(f"[red]  ✖ {msg}[/red]")

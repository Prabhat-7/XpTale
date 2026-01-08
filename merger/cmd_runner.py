import subprocess
from merger.console import ConsoleStyle
from rich.console import Console

console=Console()

class CmdRunner:
    @staticmethod
    def run(cmd):
        style=ConsoleStyle()
        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,   # hide normal output -> Removed to show output
                stderr=subprocess.PIPE,     # capture errors
                text=True
        )
        except subprocess.CalledProcessError as e:
            style.print_error("Command failed:")
            console.print(f"      [red]{' '.join(cmd)}[/red]")
            console.print(f"\n    [bold]--- ERROR OUTPUT ---[/bold]")
            console.print(f"    [red]{e.stderr}[/red]")
            raise  # stop the program



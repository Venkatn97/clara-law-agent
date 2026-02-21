import uuid 
import argparse
from datetime import datetime 
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

from agent.agent import chat, run_single_query
from agent.memory import create_initial_state

console=Console()

def print_clara(response:str):
    console.print()
    console.print(Panel(
        Text(response, style="white"),
        title="[bold green] Clara Morrison & Associates[/bold green]",
        border_style="green",
        padding=(1,2)

    ))

def print_caller(message: str):
    console.print()
    console.print(Panel(
        Text(message, style="cyan"),
        title="[bold cyan] Caller[/bold cyan]",
        border_style="cyan",
        padding=(0,2)
    ))
def print_header():
    console.print()
    console.print(Rule("[bold yellow]CLARA — Law Firm AI Receptionist[/bold yellow]"))
    console.print(Panel(
        "[bold]Morrison & Associates Law Firm[/bold]\n"
        "Family Law | Personal Injury | Criminal Defense | Estate Planning\n\n"
        "[dim]Phase 1: Terminal Chat — AWS Bedrock + LangGraph[/dim]\n\n"
        "[yellow]Type quit to end | Type help for commands[/yellow]",
        border_style="yellow"
    ))
    console.print()

def run_session():
    print_header()

    session_id=str(uuid.uuid4())[:8]
    state=create_initial_state(session_id=session_id)

    console.print(f"[dim]Session:{session_id}|{datetime.now().strftime('%I:%M %p')}[/dim]\n")

    opening = (
    "Thank you for calling Morrison and Associates. "
    "This is Clara speaking. How can I help you today?"
    )
    print_clara(opening)

    while True:
        try:
            console.print("[cyan]You:[/cyan]",end="")
            user_input = input().strip()

            if not user_input:
                continue
            if user_input.lower() == "help":
                console.print(Panel(
                    "Commands:\n"
                    "  [cyan]quit[/cyan] — End session\n"
                    "  [cyan]help[/cyan] — Show commands\n\n"
                    "Try saying:\n"
                    "  I need help with a custody battle\n"
                    "  I was just in a car accident\n"
                    "  I was just arrested help\n"
                    "  What are your fees for estate planning",
                    border_style="dim"
                ))
                continue

            print_caller(user_input)

            with console.status("[green]Clara is thinking...[/green]"):
                response, state=chat(user_input, state)
            
            print_clara(response)

        except KeyboardInterrupt:
            console.print("\n[dim]Session interrupted.[/dim]\n")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            console.print("[dim]Check your AWS credentials in .env[/dim]")
            break


if __name__ == "__main__":
    run_session()


    
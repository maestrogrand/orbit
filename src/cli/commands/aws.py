import typer
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from pathlib import Path
import subprocess
from cli.commands.workspace import get_current_workspace
from rich.console import Console
from rich.prompt import Prompt

app = typer.Typer(help="Manage AWS accounts and resources")

WORKSPACE_DIR = Path.home() / ".orbit" / "workspaces"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
CURRENT_AWS_PROFILE_FILE = WORKSPACE_DIR / "current_aws_profile.txt"

ALLOWED_PROFILES = ["default", "dev", "staging", "prod"]


def set_current_aws_profile(profile: str):
    """
    Set the current AWS profile in a text file.
    """
    with CURRENT_AWS_PROFILE_FILE.open("w") as file:
        file.write(profile)


def get_current_aws_profile():
    """
    Get the current AWS profile from the text file.
    """
    if CURRENT_AWS_PROFILE_FILE.exists():
        with CURRENT_AWS_PROFILE_FILE.open("r") as file:
            return file.read().strip()
    return None


@app.command()
def switch(profile: str):
    """
    Switch to a specified AWS profile.
    """
    if profile not in ALLOWED_PROFILES:
        typer.echo(
            f"Profile '{profile}' is not allowed. Allowed profiles: {', '.join(ALLOWED_PROFILES)}"
        )
        raise typer.Exit(code=1)
    try:
        boto3.setup_default_session(profile_name=profile)
        set_current_aws_profile(profile)
        typer.echo(f"Switched to AWS profile '{profile}'.")
    except (BotoCoreError, NoCredentialsError) as e:
        typer.echo(f"Failed to switch AWS profile: {e}")
        raise typer.Exit(code=1)


@app.command()
def list_profiles():
    """
    List available AWS profiles from the AWS credentials file.
    """
    try:
        profiles = boto3.Session().available_profiles
        if profiles:
            typer.echo("Available AWS profiles:")
            for profile in profiles:
                typer.echo(f"- {profile}")
        else:
            typer.echo("No AWS profiles found.")
    except Exception as e:
        typer.echo(f"Failed to list AWS profiles: {e}")
        raise typer.Exit(code=1)


@app.command()
def console():
    """
    Open an interactive AWS CLI console in the current workspace and profile.
    """
    current_profile = get_current_aws_profile()
    current_workspace = get_current_workspace()

    if not current_profile:
        typer.echo(
            "No AWS profile selected. Use 'orbit aws switch <profile>' to select a profile."
        )
        raise typer.Exit(code=1)

    if current_profile not in ALLOWED_PROFILES:
        typer.echo(
            f"Current profile '{current_profile}' is not allowed. Allowed profiles: {', '.join(ALLOWED_PROFILES)}"
        )
        raise typer.Exit(code=1)

    typer.echo(f"Welcome to the AWS CLI console!")
    typer.echo(f"Current Profile: {current_profile}")
    typer.echo(f"Current Workspace: {current_workspace or 'None'}")
    console = Console()

    while True:
        try:
            command = Prompt.ask("[bold cyan]aws>[/bold cyan]")
            if command.lower() in ["exit", "quit"]:
                console.print("[green]Exiting AWS CLI console. Goodbye![/green]")
                break

            full_command = f"aws {command} --profile {current_profile}"
            result = subprocess.run(
                full_command, shell=True, text=True, capture_output=True
            )

            if result.returncode == 0:
                console.print(result.stdout)
            else:
                console.print(f"[red]Error:[/red] {result.stderr}")

        except KeyboardInterrupt:
            console.print("[yellow]Interrupted! Exiting AWS CLI console.[/yellow]")
            break

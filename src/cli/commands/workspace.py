import typer
import yaml
from pathlib import Path

app = typer.Typer(help="Manage named workspaces")

WORKSPACE_DIR = Path.home() / ".orbit" / "workspaces"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
CURRENT_WORKSPACE_FILE = WORKSPACE_DIR / "current_workspace.txt"


def load_workspaces():
    """
    Load the list of existing workspaces from the workspace directory.
    """
    return [f.stem for f in WORKSPACE_DIR.glob("*.yaml")]


def save_workspace(name: str, config: dict):
    """
    Save a workspace configuration to a YAML file.
    """
    workspace_file = WORKSPACE_DIR / f"{name}.yaml"
    with workspace_file.open("w") as file:
        yaml.dump(config, file)


def delete_workspace_file(name: str):
    """
    Delete a workspace configuration file.
    """
    workspace_file = WORKSPACE_DIR / f"{name}.yaml"
    if workspace_file.exists():
        workspace_file.unlink()


def set_current_workspace(name: str):
    """
    Set the current workspace in a text file.
    """
    with CURRENT_WORKSPACE_FILE.open("w") as file:
        file.write(name)


def get_current_workspace():
    """
    Get the current workspace from the text file.
    """
    if CURRENT_WORKSPACE_FILE.exists():
        with CURRENT_WORKSPACE_FILE.open("r") as file:
            return file.read().strip()
    return None


@app.command()
def create(name: str):
    """
    Create a new workspace.
    """
    config = {
        "name": name,
        "aws_profile": "",
        "kubernetes_context": "",
        "terraform_state": "",
    }
    save_workspace(name, config)
    typer.echo(f"Workspace '{name}' created successfully.")


@app.command()
def switch(name: str):
    """
    Switch to an existing workspace.
    """
    workspaces = load_workspaces()
    if name not in workspaces:
        typer.echo(f"Workspace '{name}' does not exist.")
        raise typer.Exit(code=1)
    set_current_workspace(name)
    typer.echo(f"Switched to workspace '{name}'.")


@app.command()
def list():
    """
    List all available workspaces.
    """
    workspaces = load_workspaces()
    if not workspaces:
        typer.echo("No workspaces found.")
    else:
        typer.echo("Available workspaces:")
        for ws in workspaces:
            typer.echo(f"- {ws}")


@app.command()
def delete(name: str):
    """
    Delete a workspace.
    """
    workspaces = load_workspaces()
    if name not in workspaces:
        typer.echo(f"Workspace '{name}' does not exist.")
        raise typer.Exit(code=1)
    delete_workspace_file(name)
    typer.echo(f"Workspace '{name}' deleted successfully.")

import typer
from cli.commands import workspace, aws, terraform

app = typer.Typer(help="Orbit AI Ops Assistant: Simplify your DevOps workflows.")

app.add_typer(workspace.app, name="workspace", help="Manage named workspaces")
app.add_typer(aws.app, name="aws", help="Manage AWS accounts and resources")
app.add_typer(terraform.app, name="tf", help="Manage Terraform configurations")


@app.callback()
def main():
    """
    Orbit AI Ops Assistant: A terminal-based assistant for managing AWS, Terraform, and Workspaces.
    """
    typer.echo("Welcome to Orbit AI Ops Assistant!")


if __name__ == "__main__":
    app()

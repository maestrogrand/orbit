import typer
from cli.commands import workspace, aws, terraform, kubernetes, helm, okta

app = typer.Typer(help="orbit AI Ops Assistant: Simplify your DevOps workflows.")

app.add_typer(workspace.app, name="workspace", help="Manage named workspaces")
app.add_typer(aws.app, name="aws", help="Manage AWS accounts and resources")


@app.callback()
def main():
    """
    orbit AI Ops Assistant: A terminal-based assistant for managing AWS, Terraform, Kubernetes, Helm, and Okta.
    """
    typer.echo("Welcome to orbit AI Ops Assistant!")


if __name__ == "__main__":
    app()

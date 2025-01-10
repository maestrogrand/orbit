import typer
import subprocess
from cli.commands.workspace import get_current_workspace
from cli.commands.aws import get_current_aws_profile

app = typer.Typer(help="Manage Terraform configurations")


def run_terraform_command(command: str, cwd: str = "."):
    """
    Helper function to run Terraform commands.
    """
    try:
        result = subprocess.run(
            ["terraform"] + command.split(),
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        typer.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error running Terraform command:\n{e.stderr}")
        raise typer.Exit(code=1)


def print_current_context():
    """
    Print the current workspace and AWS profile.
    """
    workspace = get_current_workspace()
    aws_profile = get_current_aws_profile()
    typer.echo(f"Current Workspace: {workspace or 'None'}")
    typer.echo(f"Current AWS Profile: {aws_profile or 'None'}")


@app.command()
def init(directory: str = "."):
    """
    Initialize a Terraform configuration directory.
    """
    print_current_context()
    typer.echo(f"Initializing Terraform configuration in directory: {directory}")
    run_terraform_command("init", cwd=directory)


@app.command()
def plan(directory: str = ".", out: str = "plan.out"):
    """
    Generate and show an execution plan.
    """
    print_current_context()
    typer.echo(f"Generating Terraform plan in directory: {directory}")
    run_terraform_command(f"plan -out={out}", cwd=directory)


@app.command()
def apply(plan: str = None, directory: str = "."):
    """
    Apply changes required to reach the desired state of the configuration.
    """
    print_current_context()
    if plan:
        typer.echo(f"Applying Terraform plan from file: {plan}")
        run_terraform_command(f"apply {plan}", cwd=directory)
    else:
        typer.echo(f"Applying Terraform changes in directory: {directory}")
        run_terraform_command("apply -auto-approve", cwd=directory)


@app.command()
def destroy(directory: str = "."):
    """
    Destroy Terraform-managed infrastructure.
    """
    print_current_context()
    typer.echo(f"Destroying Terraform-managed infrastructure in directory: {directory}")
    run_terraform_command("destroy -auto-approve", cwd=directory)

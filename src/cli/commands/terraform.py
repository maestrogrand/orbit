import typer
import subprocess

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


@app.command()
def init(directory: str = "."):
    """
    Initialize a Terraform configuration directory.
    """
    typer.echo(f"Initializing Terraform configuration in directory: {directory}")
    run_terraform_command("init", cwd=directory)


@app.command()
def plan(directory: str = ".", out: str = "plan.out"):
    """
    Generate and show an execution plan.
    """
    typer.echo(f"Generating Terraform plan in directory: {directory}")
    run_terraform_command(f"plan -out={out}", cwd=directory)


@app.command()
def apply(plan: str = None, directory: str = "."):
    """
    Apply changes required to reach the desired state of the configuration.
    """
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
    typer.echo(f"Destroying Terraform-managed infrastructure in directory: {directory}")
    run_terraform_command("destroy -auto-approve", cwd=directory)

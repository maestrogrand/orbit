import typer
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from botocore.session import Session

app = typer.Typer(help="Manage AWS accounts and resources")


@app.command()
def switch(profile: str):
    """
    Switch to a specified AWS profile.
    """
    try:
        boto3.setup_default_session(profile_name=profile)
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
        profiles = Session().available_profiles
        if profiles:
            typer.echo("Available AWS profiles:")
            for profile in profiles:
                typer.echo(f"- {profile}")
        else:
            typer.echo("No AWS profiles found.")
    except Exception as e:
        typer.echo(f"Failed to list AWS profiles: {e}")
        raise typer.Exit(code=1)

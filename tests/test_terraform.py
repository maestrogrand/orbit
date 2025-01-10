import pytest
from typer.testing import CliRunner
from cli.commands.terraform import app

runner = CliRunner()

def test_terraform_init(mocker):
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.return_value.stdout = "Terraform initialized successfully."

    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "Terraform initialized successfully." in result.output

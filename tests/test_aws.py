import pytest
from typer.testing import CliRunner
from cli.commands.aws import app

runner = CliRunner()

def test_list_profiles(mocker):
    mock_session = mocker.patch("botocore.session.Session")
    mock_session().available_profiles = ["default", "dev"]
    result = runner.invoke(app, ["list_profiles"])
    assert result.exit_code == 0
    assert "Available AWS profiles:" in result.output
    assert "- default" in result.output
    assert "- dev" in result.output

import pytest
from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()


def test_list_profiles(mocker):
    mock_session = mocker.patch("botocore.session.Session")
    mock_session.return_value.available_profiles = ["default", "dev"]
    result = runner.invoke(app, ["aws", "list_profiles"])

    assert result.exit_code == 0, result.output
    assert "Available AWS profiles:" in result.output
    assert "- default" in result.output
    assert "- dev" in result.output

import pytest
from typer.testing import CliRunner
from cli.commands.workspace import app

runner = CliRunner()

def test_workspace_create(tmp_path):
    workspace_name = "test_workspace"
    result = runner.invoke(app, ["create", workspace_name])
    assert result.exit_code == 0
    assert f"Workspace '{workspace_name}' created successfully." in result.output

def test_workspace_list_empty(tmp_path):
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "No workspaces found." in result.output

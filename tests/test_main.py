import pytest
from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()

def test_main_callback():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Welcome to Orbit AI Ops Assistant!" in result.output

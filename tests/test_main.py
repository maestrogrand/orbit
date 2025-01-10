import pytest
from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()


def test_main_callback():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0, result.output
    assert "Orbit AI Ops Assistant" in result.output

#!/bin/bash

set -e

VENV_DIR=".venv"

cleanup() {
    echo "Cleaning up virtual environment and temporary files..."
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
        echo "Virtual environment deleted."
    fi
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -rf {} +
    echo "Temporary Python files deleted."
}

trap cleanup SIGINT SIGTERM

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installing the project..."
pip install -e .

echo "Verifying CLI tool installation..."
if command -v orbit &>/dev/null; then
    echo "Orbit CLI is installed successfully. Type 'orbit --help' to see available commands."
else
    echo "CLI tool 'Orbit' is not installed. Check your setup."
    exit 1
fi

echo "Environment setup complete. You can now use the 'orbit' command."
echo "Type 'orbit --help' to get started."

exec "$SHELL"

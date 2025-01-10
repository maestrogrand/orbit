#!/bin/bash

set -e

VENV_DIR=".venv"
LOG_FILE="orbit_service.log"
PID_FILE="orbit_service.pid"
EGG_INFO_DIR="src/Orbit_ai_ops_assistant.egg-info"

start_service() {
    if [ -f "$PID_FILE" ]; then
        echo "Service is already running. PID: $(cat $PID_FILE)"
        exit 1
    fi

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
        echo "Orbit CLI is installed successfully."
    else
        echo "CLI tool 'Orbit' is not installed. Check your setup."
        exit 1
    fi

    echo "Starting the virtual environment service..."
    nohup bash -c "source $VENV_DIR/bin/activate && tail -f /dev/null" >"$LOG_FILE" 2>&1 &
    echo $! >"$PID_FILE"

    echo "Service started and running in the background. Logs: $LOG_FILE"
    echo "Use 'orbit' in any terminal window. Stop with './run.sh stop'."
}

stop_service() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Service is not running."
        exit 1
    fi

    echo "Stopping the service..."
    PID=$(cat "$PID_FILE")
    kill "$PID" || true
    rm -f "$PID_FILE"

    echo "Cleaning up virtual environment and temporary files..."
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
        echo "Virtual environment deleted."
    fi

    if [ -d "$EGG_INFO_DIR" ]; then
        rm -rf "$EGG_INFO_DIR"
        echo "Egg-info directory deleted."
    fi

    if [ -f "$LOG_FILE" ]; then
        rm -f "$LOG_FILE"
        echo "Log file deleted."
    fi

    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -rf {} +
    echo "Cleanup complete."
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 {start|stop}"
    exit 1
fi

case "$1" in
start)
    start_service
    ;;
stop)
    stop_service
    ;;
*)
    echo "Invalid argument: $1"
    echo "Usage: $0 {start|stop}"
    exit 1
    ;;
esac

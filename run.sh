#!/bin/bash

set -e

VENV_DIR=".venv"
LOG_FILE="orbit_service.log"
PID_FILE="orbit_service.pid"
EGG_INFO_DIR="src/Orbit_ai_ops_assistant.egg-info"

is_service_running() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

start_service() {
    if is_service_running; then
        echo "Service is already running. PID: $(cat $PID_FILE)"
        return 0
    fi

    echo "Starting service..."

    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi

    echo "Installing dependencies..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt

    echo "Installing the project..."
    pip install -e .

    echo "Verifying CLI tool installation..."
    if ! command -v orbit &>/dev/null; then
        echo "CLI tool 'Orbit' is not installed. Check your setup."
        deactivate
        exit 1
    fi

    nohup bash -c "source $VENV_DIR/bin/activate && tail -f /dev/null" >"$LOG_FILE" 2>&1 &
    echo $! >"$PID_FILE"

    echo "Service started. Logs: $LOG_FILE"
}

stop_service() {
    if is_service_running; then
        echo "Stopping service..."
        kill $(cat "$PID_FILE") || true
        rm -f "$PID_FILE"
    else
        echo "Service is not running."
    fi

    echo "Cleaning up..."
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
    fi

    if [ -d "$EGG_INFO_DIR" ]; then
        rm -rf "$EGG_INFO_DIR"
    fi

    if [ -f "$LOG_FILE" ]; then
        rm -f "$LOG_FILE"
    fi

    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type d -name ".pytest_cache" -exec rm -rf {} +
    find . -type d -name "$VENV_DIR*" -exec rm -rf {} +
    find /tmp -type f -name "tmp*.py" -delete

    echo "Service stopped and cleanup complete."
}

restart_service() {
    stop_service
    start_service
}

lint_code() {
    if ! is_service_running; then
        start_service
    fi

    echo "Running code linting..."
    source "$VENV_DIR/bin/activate"
    black --check src
    flake8 src
    echo "Linting complete."

    stop_service
}

format_code() {
    if ! is_service_running; then
        start_service
    fi

    echo "Running code formatting..."
    source "$VENV_DIR/bin/activate"
    black src tests
    echo "Formatting complete."

    stop_service
}

test_app() {
    if ! is_service_running; then
        start_service
    fi

    echo "Running tests..."
    source "$VENV_DIR/bin/activate"
    pytest
    echo "Tests complete."

    stop_service
}

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 {start|stop|restart|lint|format|test}"
    exit 1
fi

case "$1" in
start)
    start_service
    ;;
stop)
    stop_service
    ;;
restart)
    restart_service
    ;;
lint)
    lint_code
    ;;
format)
    format_code
    ;;
test)
    test_app
    ;;
*)
    echo "Invalid argument: $1"
    echo "Usage: $0 {start|stop|restart|lint|format|test}"
    exit 1
    ;;
esac

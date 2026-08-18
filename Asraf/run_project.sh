#!/usr/bin/env bash
# This launcher is for Linux/macOS users.
# Stop immediately if a command fails.
set -e
# Move into the folder that contains this script.
cd "$(dirname "$0")"
# Check that Python 3 exists.
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. Please install Python 3 first."
  exit 1
fi
# No pip dependencies are required.
echo "Python is ready. No extra pip packages are required."
# Start the graphical simulator.
python3 main.py

#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Function to print messages
print_message() {
  echo
  echo "===================="
  echo "$1"
  echo "===================="
  echo
}

print_message "Installing virtualenv..."
pip3 install --user virtualenv

print_message "Creating virtual environment..."
python3 -m virtualenv venv

print_message "Activating virtual environment..."
source venv/bin/activate

print_message "Installing required packages from requirements.txt..."
pip install -r requirements.txt

print_message "Deactivating virtual environment..."
deactivate

# Keep the terminal open (optional, depending on your terminal)
exec $SHELL

#!/bin/bash

echo "Installing virtualenv..."
pip install virtualenv

echo "Creating virtual environment..."
python3 -m virtualenv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing required packages from requirements.txt..."
pip install -r requirements.txt

echo "Deactivating virtual environment..."
deactivate

# Keep the terminal open (optional, depending on your terminal)
exec $SHELL

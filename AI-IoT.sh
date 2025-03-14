#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Run the Python script
python run_entrypoint.py

# Deactivate the virtual environment
deactivate

# Keep the terminal open (optional, depending on your terminal)
exec $SHELL

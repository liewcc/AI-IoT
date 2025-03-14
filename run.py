import subprocess
import os
import time
import psutil

# Path to your virtual environment's activate script
venv_activate = r'venv\Scripts\activate.bat'

# Streamlit application command
streamlit_command = 'streamlit run Main.py'

# Start the Command Prompt process
cmd = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Activate the virtual environment
cmd.stdin.write(f'call {venv_activate}\n')
cmd.stdin.flush()

# Run the Streamlit application
cmd.stdin.write(f'{streamlit_command}\n')
cmd.stdin.flush()

# Print statement to indicate the process is running
print("Streamlit application is running. Monitoring for termination...")

# Continuously check if the Streamlit application is running
while True:
    # Check if the Streamlit process is still running
    if not any(proc.name() == 'streamlit.exe' for proc in psutil.process_iter()):
        break

    time.sleep(0.1)

# Deactivate the virtual environment and close the terminal window
cmd.stdin.write('deactivate\n')
cmd.stdin.flush()
cmd.stdin.write('exit\n')
cmd.stdin.flush()

# Wait for the Command Prompt process to terminate
cmd.wait()
print("Streamlit application has been deactivated and the terminal window is closed.")


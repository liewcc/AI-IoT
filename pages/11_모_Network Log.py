import streamlit as st
import time
import os
import psutil
import subprocess

# Function to check for the ollama.exe process and return details
def get_process_details(process_name):
    result = subprocess.run(['tasklist'], stdout=subprocess.PIPE, text=True, shell=True)
    processes = []
    for line in result.stdout.splitlines():
        if process_name in line:
            parts = list(filter(None, line.split()))
            processes.append(parts[:5])
    return processes

# Function to format process details
def format_process_details(processes):
    header = "{:<15} {:<10} {:<15} {:<10} {:<15}".format("Image Name", "PID", "Session Name", "Session#", "Mem Usage")
    lines = [header]
    for proc in processes:
        lines.append("{:<15} {:<10} {:<15} {:<10} {:<15}".format(proc[0], proc[1], proc[2], proc[3], proc[4]))
    return "\n".join(lines)

# Function to run the ollama ps command
def run_ollama_ps():
    try:
        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else "Failed to run ollama ps command"
    except Exception as e:
        return str(e)

# Check for ollama.exe process
ollama_processes = get_process_details('ollama.exe')

if not ollama_processes:
    st.error("Ollama Server offline")
else:
    st.success("Ollama Server is online")
    formatted_details = format_process_details(ollama_processes)
    st.code(formatted_details, language='text')
    ollama_ps_output = run_ollama_ps()
    st.code(ollama_ps_output, language='text')

# Initialize session state variables
if 'view_order' not in st.session_state:
    st.session_state.view_order = 'ascending'

# Create placeholders for the status, button, and logs
status_placeholder = st.empty()
button_placeholder = st.empty()
log_placeholder = st.empty()

# Function to read log file
def read_log_file():
    with open('network_state.log', 'r') as log_file:
        return log_file.readlines()

# Function to clear log file
def clear_log_file():
    with open('network_state.log', 'w') as log_file:
        log_file.write('')

# Function to extract the latest status from logs
def extract_status(logs):
    connection_status = "Server not started"
    latest_data = "No data received yet"
    
    for log in logs[::-1]:  # Process logs in reverse order to get the latest entries first
        if "Stopping server..." in log:
            connection_status = "Server stopped"
        elif "Connection from" in log:
            connection_status = log.split(" - ")[-1].strip()
        elif "RX:" in log:
            latest_data = log.split(" - ")[-1].strip()
        elif "Server started, waiting for connections..." in log:
            connection_status = "Server started, waiting for connections..."
        if connection_status != "Server not started" and latest_data != "No data received yet":
            break

    return connection_status, latest_data

# Function to check if a port is open
def is_port_open(port):
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN' and conn.laddr.port == port:
            return True
    return False

# Sidebar button to clear the log file
if st.sidebar.button("Clear Logs"):
    clear_log_file()
    # Use st.rerun to trigger a refresh
    st.rerun()

# Display the logs and status when the page is first loaded
logs = read_log_file()

# Extract status before sorting the logs
connection_status, latest_data = extract_status(logs)

port_info = st.session_state.get('port', 'Unknown')

# Check if the port is actually open or closed
if port_info != 'Unknown' and port_info is not None:
    try:
        port_num = int(port_info)
        if not is_port_open(port_num):
            port_info = 'Closed'
    except ValueError:
        port_info = 'Invalid port'

status_placeholder.markdown(f"""
**Port:** {port_info}
**Connection Status:** {connection_status}
**Latest Data:** {latest_data}
""")

# Place the button to toggle log view order
if button_placeholder.button("Toggle View Order"):
    if st.session_state.view_order == 'ascending':
        st.session_state.view_order = 'descending'
    else:
        st.session_state.view_order = 'ascending'
    st.rerun()

# Sort the logs based on view order
if st.session_state.view_order == 'ascending':
    logs = logs[::-1]

log_placeholder.code("".join(logs))

# Track the modification time of the log file
last_mod_time = os.path.getmtime('network_state.log')

# Continuously fetch and display logs and statuses in real time
while True:
    current_mod_time = os.path.getmtime('network_state.log')
    if current_mod_time != last_mod_time:
        logs = read_log_file()
        
        # Extract status before sorting the logs
        connection_status, latest_data = extract_status(logs)
        
        port_info = st.session_state.get('port', 'Unknown')

        # Check if the port is actually open or closed
        if port_info != 'Unknown' and port_info is not None:
            try:
                port_num = int(port_info)
                if not is_port_open(port_num):
                    port_info = 'Closed'
            except ValueError:
                port_info = 'Invalid port'

        status_placeholder.markdown(f"""
        **Port:** {port_info}
        **Connection Status:** {connection_status}
        **Latest Data:** {latest_data}
        """)

        # Sort the logs based on view order
        if st.session_state.view_order == 'ascending':
            logs = logs[::-1]

        log_placeholder.code("".join(logs))

        last_mod_time = current_mod_time
    time.sleep(1)

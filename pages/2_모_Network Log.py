import streamlit as st
import time
import os
import psutil
import subprocess


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

# Sidebar button to clear the log file
if st.sidebar.button("Clear Logs"):
    clear_log_file()
    # Use st.rerun to trigger a refresh
    st.rerun()

# Display the logs and status when the page is first loaded
logs = read_log_file()

port_info = st.session_state.get('port', 'Unknown')

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
        
        # Sort the logs based on view order
        if st.session_state.view_order == 'ascending':
            logs = logs[::-1]

        log_placeholder.code("".join(logs))

        last_mod_time = current_mod_time
    time.sleep(1)

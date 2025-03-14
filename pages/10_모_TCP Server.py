import streamlit as st
import socket
import threading
import time
from datetime import datetime
import queue

# Initialize session state variables
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'stop_event' not in st.session_state:
    st.session_state.stop_event = threading.Event()
if 'server_thread' not in st.session_state:
    st.session_state.server_thread = None
if 'network_status' not in st.session_state:
    st.session_state.network_status = "Active"
if 'log_queue' not in st.session_state:
    st.session_state.log_queue = queue.Queue()
if 'state_queue' not in st.session_state:
    st.session_state.state_queue = queue.Queue()
if 'connection_status' not in st.session_state:
    st.session_state.connection_status = "Disconnected"
if 'port' not in st.session_state:
    st.session_state.port = 8888  # Default port value
if 'latest_data' not in st.session_state:
    st.session_state.latest_data = None
if 'log_view_order' not in st.session_state:
    st.session_state.log_view_order = 'descending'  # Default to descending
if 'ip_address' not in st.session_state:
    # Get the system's default IP address
    st.session_state.ip_address = socket.gethostbyname(socket.gethostname())

# Function to update log file
def update_log_file(message):
    with open('network_state.log', 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%y-%m-%d %H:%M:%S')} - {message}\n")

def start_server(stop_event, log_queue, state_queue, ip_address, port):
    while not stop_event.is_set():
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((ip_address, port))
            server_socket.listen(5)
            state_queue.put({'port': port})
            state_queue.put({'connection_status': 'Server started, waiting for connections...'})
            log_queue.put((datetime.now(), 'Server started, waiting for connections...'))
            update_log_file('Server started, waiting for connections...')

            while not stop_event.is_set():
                try:
                    server_socket.settimeout(1)
                    client_socket, client_address = server_socket.accept()
                    log_queue.put((datetime.now(), f"Connection from {client_address}"))
                    state_queue.put({'connection_status': f"Connected to {client_address}"})
                    update_log_file(f"Connection from {client_address}")
                    try:
                        data = client_socket.recv(1024)
                        hex_data = data.hex()
                        log_queue.put((datetime.now(), f"RX: {hex_data}"))
                        state_queue.put({'latest_data': hex_data})
                        update_log_file(f"RX: {hex_data}")
                    except ConnectionAbortedError as e:
                        log_queue.put((datetime.now(), f"Connection aborted: {e}"))
                        update_log_file(f"Connection aborted: {e}")
                    finally:
                        client_socket.close()
                except socket.timeout:
                    continue
            log_queue.put((datetime.now(), "Server stopped."))
            state_queue.put({'connection_status': "Server stopped"})
            update_log_file("Server stopped.")
            server_socket.close()
        except (socket.error, ConnectionAbortedError) as e:
            log_queue.put((datetime.now(), f"Error: {e}. Retrying in 5 seconds..."))
            update_log_file(f"Error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def main():
    # Add text boxes for IP address and port
    st.session_state.ip_address = st.sidebar.text_input("IP Address", value=st.session_state.ip_address)
    st.session_state.port = st.sidebar.text_input("Port", value=st.session_state.port)

    start_server_button = st.sidebar.button("Start Server")
    stop_server_button = st.sidebar.button("Stop Server")
    toggle_order_placeholder = st.empty()
    log_display = st.empty()

    if start_server_button and st.session_state.server_thread is None:
        st.session_state.stop_event.clear()
        st.session_state.server_thread = threading.Thread(
            target=start_server, args=(st.session_state.stop_event, st.session_state.log_queue, st.session_state.state_queue, st.session_state.ip_address, int(st.session_state.port))
        )
        st.session_state.server_thread.daemon = True
        st.session_state.server_thread.start()
        st.session_state.logs.append(f"{datetime.now().strftime('%y-%m-%d %H:%M:%S')} Server is running on {st.session_state.ip_address}:{st.session_state.port}...")
        update_log_file(f"Server is running on {st.session_state.ip_address}:{st.session_state.port}...")

    if stop_server_button and st.session_state.server_thread is not None:
        st.session_state.stop_event.set()
        st.session_state.logs.append(f"{datetime.now().strftime('%y-%m-%d %H:%M:%S')} Stopping server...")
        st.session_state.server_thread = None
        update_log_file("Stopping server...")

    # Place the button to toggle log view order in the separate placeholder
    with toggle_order_placeholder:
        if st.button("Toggle View Order"):
            if st.session_state.log_view_order == 'ascending':
                st.session_state.log_view_order = 'descending'
            else:
                st.session_state.log_view_order = 'ascending'
            st.rerun()

    # Update the logs display and session state in real-time
    while True:
        try:
            while not st.session_state.log_queue.empty():
                log_time, log_message = st.session_state.log_queue.get_nowait()
                st.session_state.logs.append(f"{log_time.strftime('%y-%m-%d %H:%M:%S')} {log_message}")
            while not st.session_state.state_queue.empty():
                state_update = st.session_state.state_queue.get_nowait()
                for key, value in state_update.items():
                    st.session_state[key] = value
        except queue.Empty:
            pass

        # Sort the logs based on view order
        if st.session_state.log_view_order == 'descending':
            logs_to_display = st.session_state.logs[::-1]
        else:
            logs_to_display = st.session_state.logs

        log_display.code("\n".join(logs_to_display))
        time.sleep(1)

if __name__ == "__main__":
    main()

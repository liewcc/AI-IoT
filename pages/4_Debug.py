import streamlit as st
import socket
import threading
import time
from queue import Queue

def socket_communication(log_queue):
    host = '103.169.90.54'
    port = 65432

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            while True:
                data = s.recv(1024)
                if not data:
                    break
                log_queue.put(data.decode('utf-8'))
            s.close()
            break
        except ConnectionRefusedError:
            log_queue.put("Connection refused. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            log_queue.put(f"An error occurred: {e}")
            break

st.title("TCP Socket Test")

log_queue = Queue()
log_box = st.empty()

thread = threading.Thread(target=socket_communication, args=(log_queue,))
thread.start()

def update_log():
    if not log_queue.empty():
        latest_message = log_queue.get()
        log_box.text_area("Output", value=latest_message, height=200, key="log_box")

if 'thread_started' not in st.session_state:
    thread = threading.Thread(target=socket_communication, args=(log_queue,))
    thread.start()
    st.session_state['thread_started'] = True

while True:
    update_log()
    time.sleep(1)
    st.rerun()

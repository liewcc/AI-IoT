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
    log_messages = []
    while not log_queue.empty():
        log_message = log_queue.get()
        log_messages.append(log_message)

    if log_messages:
        full_log = "\n".join(log_messages)
        log_box.text_area("Output", value=full_log, height=200)

while True:
    update_log()
    time.sleep(1)

import streamlit as st
import socket
import threading

# Function to handle socket communication
def socket_communication(log_box):
    host = '103.169.90.54'
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if not data:
            break
        log_box.text_area("Output", data.decode('utf-8'), height=200)

    s.close()

# Streamlit app
st.title("TCP Socket Test")

log_box = st.empty()
thread = threading.Thread(target=socket_communication, args=(log_box,))
thread.start()

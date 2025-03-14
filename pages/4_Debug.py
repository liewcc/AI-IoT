import streamlit as st
import socket
import threading
import time

def socket_communication(log_box):
    host = '127.0.0.1'
    port = 65432

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            while True:
                data = s.recv(1024)
                if not data:
                    break
                log_box.text_area("Output", value=data.decode('utf-8'), height=200)
            s.close()
            break
        except ConnectionRefusedError:
            log_box.text_area("Output", value="Connection refused. Retrying in 5 seconds...", height=200)
            time.sleep(5)
        except Exception as e:
            log_box.text_area("Output", value=f"An error occurred: {e}", height=200)
            break

st.title("TCP Socket Test")

log_box = st.empty()
thread = threading.Thread(target=socket_communication, args=(log_box,))
thread.start()

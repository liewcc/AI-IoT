import socket
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

def start_server():
    host = '0.0.0.0'
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    logging.info(f"Server listening on {host}:{port}")

    while True:
        conn, addr = s.accept()
        logging.info(f"Connected by {addr} at {datetime.now()}")
        try:
            conn.settimeout(120)  # Extend timeout duration for remote server
            data = conn.recv(1024)
            if data:
                hex_data = data.hex()
                logging.info(f"Received data in hex: {hex_data} at {datetime.now()}")
                conn.sendall(data)  # Optional: Echo back the data
            else:
                logging.warning(f"No data received from {addr} at {datetime.now()}")
        except socket.timeout:
            logging.error(f"Socket timeout: No data received from {addr} after waiting.")
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            conn.close()
            logging.info(f"Connection closed with {addr} at {datetime.now()}")

if __name__ == "__main__":
    start_server()

import socket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def start_server():
    host = '0.0.0.0'  # Bind to all interfaces
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    logging.info(f"Server listening on {host}:{port}")

    try:
        while True:
            conn, addr = s.accept()
            logging.info(f"Connected by {addr}")
            while True:
                try:
                    data = conn.recv(1024)
                    if data:
                        hex_data = data.hex()
                        logging.info(f"Received data in hex: {hex_data}")
                        conn.sendall(data)
                    else:
                        break
                except socket.error as e:
                    logging.error(f"Socket error: {e}")
                    break
                except Exception as e:
                    logging.error(f"Error: {e}")
                    break
    except KeyboardInterrupt:
        logging.info("Server shutting down...")
    finally:
        s.close()

start_server()

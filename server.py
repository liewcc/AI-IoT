import socket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def start_server():
    host = '0.0.0.0'
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)  # Increase backlog for multiple connections
    logging.info(f"Server listening on {host}:{port}")

    while True:
        conn, addr = s.accept()
        logging.info(f"Connected by {addr}")
        try:
            conn.settimeout(60)  # Set timeout to 60 seconds
            data = conn.recv(1024)
            if data:
                hex_data = data.hex()
                logging.info(f"Received data in hex: {hex_data}")
                # Optional: Echo back the data
                conn.sendall(data)
            else:
                logging.warning("No data received.")
        except socket.timeout:
            logging.error("Socket error: timed out while receiving data.")
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            conn.close()  # Close the connection after processing
            logging.info(f"Connection closed with {addr}")

if __name__ == "__main__":
    start_server()

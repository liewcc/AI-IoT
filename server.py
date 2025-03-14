import socket

def start_server():
    host = '103.169.90.54'
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Server listening on {host}:{port}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if data:
                    hex_data = data.hex()
                    print(f"Received data in hex: {hex_data}")
                    conn.sendall(data)
        except KeyboardInterrupt:
            print("Server shutting down...")

start_server()

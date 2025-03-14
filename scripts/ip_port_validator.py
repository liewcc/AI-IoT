# scripts/ip_port_validator.py

import socket
import sys
import time
from datetime import datetime

def update_log_file(message):
    with open('network_state.log', 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%y-%m-%d %H:%M:%S')} - {message}\n")

def validate_ip_port(ip, port):
    # Try to create a socket and connect to the IP and port
    try:
        sock = socket.create_connection((ip, int(port)), timeout=10)
        sock.close()
        result = f"IP {ip} and Port {port} are valid and reachable."
    except Exception as e:
        result = f"Failed to connect to IP {ip} and Port {port}. Error: {e}"
    
    return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ip_port_validator.py <IP> <PORT>")
        sys.exit(1)
    
    ip = sys.argv[1]
    port = sys.argv[2]

    # Validate IP and port
    validation_result = validate_ip_port(ip, port)

    # Write validation result to a temp file
    with open('scripts/temp_validation_result.txt', 'w') as temp_file:
        temp_file.write(validation_result)
    
    # Log the validation result
    update_log_file(validation_result)

    # Simulate a delay to mimic real network response time
    time.sleep(5)
    
    # Clean up: delete the temp file
    import os
    os.remove('scripts/temp_validation_result.txt')


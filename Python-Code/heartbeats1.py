import socket
import threading
import time

# Dictionary to track the last heartbeat time of each client
client_heartbeats = {}
heartbeat_timeout = 50  # Timeout in seconds to consider a client as disconnected

# Lock for thread-safe access to shared resources
lock = threading.Lock()

def handle_client(client_socket, client_address):
    global client_heartbeats
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    # Register the client in the heartbeat tracker
    with lock:
        client_heartbeats[client_address] = time.time()

    try:
        while True:
            # Receive data from the client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Client disconnected

            if message == "HEARTBEAT":
                # Update the last heartbeat time
                with lock:
                    client_heartbeats[client_address] = time.time()
                print(f"[HEARTBEAT] Received from {client_address}")
            else:
                print(f"[MESSAGE] {client_address}: {message}")
    except Exception as e:
        print(f"[ERROR] Connection with {client_address} lost: {e}")
    finally:
        # Remove the client from the heartbeat tracker
        with lock:
            del client_heartbeats[client_address]
        client_socket.close()
        print(f"[DISCONNECTED] {client_address} disconnected.")

def monitor_heartbeats():
    """Monitor client heartbeats and disconnect inactive clients."""
    global client_heartbeats
    while True:
        time.sleep(1)  # Check every second
        with lock:
            current_time = time.time()
            inactive_clients = [
                client for client, last_heartbeat in client_heartbeats.items()
                if current_time - last_heartbeat > heartbeat_timeout
            ]
            for client in inactive_clients:
                print(f"[TIMEOUT] {client} did not send heartbeat. Disconnecting...")
                del client_heartbeats[client]

def start_server(host='127.0.0.1', port=5001):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # Allow up to 5 simultaneous connections
    print(f"[LISTENING] Server is listening on {host}:{port}")

    # Start the heartbeat monitoring thread
    threading.Thread(target=monitor_heartbeats, daemon=True).start()

    while True:
        client_socket, client_address = server.accept()
        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()

import socket
import threading
import time

def send_heartbeat(client_socket):
    """Send periodic heartbeat messages to the server."""
    while True:
        try:
            client_socket.send("HEARTBEAT".encode('utf-8'))
            time.sleep(20)  # Send heartbeat every 20 seconds
        except Exception as e:
            print(f"[ERROR] Failed to send heartbeat: {e}")
            break

def start_client(server_host='127.0.0.1', server_port=5001):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))
        print(f"[CONNECTED] Connected to server at {server_host}:{server_port}")

        # Start a thread to send heartbeat messages
        threading.Thread(target=send_heartbeat, args=(client_socket,), daemon=True).start()

        # Allow the user to send messages to the server
        while True:
            message = input("Enter message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
    finally:
        client_socket.close()
        print("[DISCONNECTED] Client disconnected.")

if __name__ == "__main__":
    start_client()

import socket
import threading
import time

SERVER_IP = '127.0.0.1'  # Replace with server IP
PORT = 5001
HEARTBEAT_INTERVAL = 20  # seconds


def send_heartbeat(sock):
    while True:
        try:
            sock.sendall("HEARTBEAT".encode())
            time.sleep(20)
        except Exception:
            break


def start_client():
    client_socket = socket.socket()
    client_socket.connect((SERVER_IP, PORT))

    threading.Thread(target=send_heartbeat, args=(client_socket,), daemon=True).start()

    try:
        while True:
            message = input("You: ")
            client_socket.sendall(message.encode())
            if message.lower() == "bye":
                print("Connection closed by client.")
                break

            data = client_socket.recv(1024).decode()
            if not data:
                print("Connection closed by server.")
                break
            print(f"Server: {data}")
            if data.lower() == "bye":
                print("Connection closed by server.")
                break
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()

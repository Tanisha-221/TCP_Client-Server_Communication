import socket
import threading
import time

HOST = '0.0.0.0'
PORT = 5001
client_heartbeats = {}
heartbeats_lock = threading.Lock()
HEARTBEAT_TIMEOUT = 60  # seconds


def monitor_heartbeats():
    while True:
        time.sleep(10)
        now = time.time()
        with heartbeats_lock:
            disconnected = []
            for client_addr, last_hb in client_heartbeats.items():
                if now - last_hb > HEARTBEAT_TIMEOUT:
                    print(f"Client {client_addr} heartbeat timed out.")
                    disconnected.append(client_addr)
            for addr in disconnected:
                client_heartbeats.pop(addr, None)


def client_handler(conn, addr):
    addr_str = f"{addr[0]}:{addr[1]}"
    with heartbeats_lock:
        client_heartbeats[addr_str] = time.time()
    print(f"Connected by {addr}")

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data.strip().upper() == "HEARTBEAT":
                with heartbeats_lock:
                    client_heartbeats[addr_str] = time.time()
                continue  # skip further processing for heartbeat

            print(f"From {addr}: {data}")
            if data.lower() == "bye":
                print(f"Connection with {addr} closed by client.")
                break

            # Server reply
            reply = input(f"Reply to {addr}: ")
            conn.sendall(reply.encode())
            if reply.lower() == "bye":
                print(f"Connection with {addr} closed by server.")
                break

    finally:
        with heartbeats_lock:
            client_heartbeats.pop(addr_str, None)
        conn.close()
        print(f"Disconnected from {addr}")


def start_server():
    threading.Thread(target=monitor_heartbeats, daemon=True).start()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on port {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=client_handler, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()

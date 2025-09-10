import socket
import threading
import os

HOST = '0.0.0.0'
PORT = 5001
RECEIVED_FOLDER = 'received_files'
BUFFER_SIZE = 4096
MAX_FILE_SIZE = 40 * 1024  # 40 KB in bytes

# Make sure the folder exists
os.makedirs(RECEIVED_FOLDER, exist_ok=True)

def handle_client(conn, addr):
    print(f"Connection from {addr} started.")
    try:
        while True:
            fileinfo = conn.recv(BUFFER_SIZE).decode()
            if not fileinfo or fileinfo == "END":
                print(f"End of files from {addr}. Closing connection.")
                break

            try:
                filename, filesize = fileinfo.split("|")
                filesize = int(filesize)
                filename = os.path.basename(filename)  # sanitize filename

                if filesize > MAX_FILE_SIZE:
                    print(f"File '{filename}' from {addr} rejected (size {filesize} bytes exceeds 40 MB limit).")
                    # Send rejection notice to client and skip receiving file
                    conn.sendall(f"REJECT|{filename}".encode())
                    continue  # skip to next file

                save_path = os.path.join(RECEIVED_FOLDER, filename)
                print(f"Receiving '{filename}' ({filesize} bytes) from {addr}")

                # Notify client ready to receive
                conn.sendall(f"READY|{filename}".encode())

                with open(save_path, "wb") as f:
                    remaining = filesize
                    while remaining > 0:
                        chunk_size = BUFFER_SIZE if remaining >= BUFFER_SIZE else remaining
                        data = conn.recv(chunk_size)
                        if not data:
                            break
                        f.write(data)
                        remaining -= len(data)

                print(f"Received file '{filename}' saved to '{save_path}'")
            except Exception as e:
                print(f"Error receiving file from {addr}: {e}")
                break
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection from {addr} closed.")

def start_server():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on port {PORT}... Waiting for clients.")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()

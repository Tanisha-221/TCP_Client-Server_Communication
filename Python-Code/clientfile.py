import socket
import os

SERVER_IP = '127.0.0.1'  # Change to your server's IP address
PORT = 5001
BUFFER_SIZE = 4096

def send_file(sock, filepath):
    if not os.path.isfile(filepath):
        print(f"File '{filepath}' does not exist.")
        return

    filesize = os.path.getsize(filepath)
    filename = os.path.basename(filepath)
    fileinfo = f"{filename}|{filesize}".encode()
    sock.sendall(fileinfo)

     # Wait for server response
    response = sock.recv(BUFFER_SIZE).decode()
    if response == f"REJECT|{filename}":
        print(f"Server rejected file '{filename}' (exceeds 40 MB limit). Skipping file.")
        return
    elif response == f"READY|{filename}":
        print(f"Server ready to receive '{filename}'. Sending file data...")
    else:
        print(f"Unexpected server response: {response}. Skipping file.")
        return

    with open(filepath, "rb") as f:
        sent = 0
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            sock.sendall(bytes_read)
            sent += len(bytes_read)
            print(f"Sent {sent} / {filesize} bytes ({sent*100/filesize:.2f}%)", end="\r")

    print(f"\nFile '{filename}' sent successfully.")

def main():
    sock = socket.socket()
    sock.connect((SERVER_IP, PORT))
    print(f"Connected to server at {SERVER_IP}:{PORT}")

    files = []
    print("Enter file paths to send. Leave empty to finish.")
    while True:
        path = input(f"File {len(files)+1}: ").strip()
        if path == '':
            break
        if not os.path.isfile(path):
            print("Invalid file path, please enter again.")
            continue
        files.append(path)
        if len(files) >= 9:
            print("Reached max 9 files.")
            break

    if not files:
        print("No files to send. Exiting.")
        sock.close()
        return

    for filepath in files:
        send_file(sock, filepath)

    sock.send("END".encode())
    print("All files sent. Closing connection.")
    sock.close()

if __name__ == "__main__":
    main()

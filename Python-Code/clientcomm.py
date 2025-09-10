import socket

s=socket.socket()

s.connect(('127.0.0.1', 4001))
print("Hello, Connection established with: " + str(s.getpeername()))
while True:
    msg = input("Client: ")
    s.send(msg.encode('utf-8'))
    if msg.lower() == 'bye':
        print("You ended the chat.")
        break
    reply = s.recv(1024).decode('utf-8') 
    print("Server:", reply)
    if reply.lower() == 'bye':
        print("Server ended the chat.")
        break

s.close()
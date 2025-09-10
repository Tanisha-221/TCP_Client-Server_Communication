#server
import socket
#create a socket object 
s=socket.socket()
#bind the socket with a port no.
s.bind(('127.0.0.1' , 4001))
#listening for a request
s.listen(10)
print("Server listening on port 4001")
    #accept the connnection 
conn, addr = s.accept()
print("HELLO, Connection established with: "+str(addr))
    #sending data to the client
while True:    
   data = conn.recv(1024).decode('utf-8').strip()
   if not data or data.lower() == 'bye':
        print("Client ended the chat.")
        break
   print("Client:", data)

    # Send to client
   msg = input("Server: ").strip()
   conn.send(msg.encode('utf-8'))
   if msg.lower() == 'bye':
        print("Server ended the chat.")
        break 
#closing the connection
conn.close()
s.close()

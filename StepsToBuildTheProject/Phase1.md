## Phase1: Architecture and design 
This is the **foundation phase**, where we defined:
* System architecture
* Tools and Technologies
* Message formats 
* Client and server responsibilities 
* Ports, security and deployment model 
## System Architecture Overview 
- **System Archtechture**
```
                          ┌────────────────────────────┐
                          │     Azure Cloud Platform   │
                          └────────────┬───────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            │                                                     │
      ┌──────────────┐                                      ┌──────────────┐
      │  Client VM 1 │                                      │  Client VM 2 │
      │  - client.py │                                      │  - client.py │
      │  - Sends     │                                      │  - Sends     │
      │    HEARTBEAT │                                      │    HEARTBEAT │
      └──────┬───────┘                                      └──────┬───────┘
             │                                                       │
             └────────────── TCP PORT 5001  ─────────────────────────┘
                                (HEARTBEAT / MESSAGE / FILE)
                                       ↓
                          ┌────────────────────────────┐
                          │   Server VM (server.py)    │
                          │  - Receives connections    │
                          │  - Logs heartbeats         │
                          │  - Alerts on timeout       │
                          └────────────────────────────
```
- **Flowchart of the diagram**
  ![alt text](image-1.png)
## Communication mode
- All communication is over TCP 
- Heartbeat interval: 30sec 
- Programming language used for `socket` library for TCP communiaction is python 
-  Socket programming is used for TCP client-server communication. The server listens for incoming connections on a custom TCP port, while the client sends heartbeats, messages, and attachments over this TCP connection, all implemented using Python.
- We will use custom port like 5001
## TCP Clent need to do three things 
- Send periodic heartbeat 
- Send normal messages(text)
- Send attachments (e.g., files, images, etc)
## Sever need to do these things 
- Listens for all messages 
Parses headeer to distinguish between heartbeats, text, and file.
- For files: receives the expected number of bytes and save the file.
## Main deliverables 
- Montitoring server/ splunk 
- Cleint Agent 
- Azure Vms
- Automation Scripts 
- Github Repository 
- Failer detection 
# TCP-based Heartbeat Monitoring System on Azure

## Project Overview

This project implements a lightweight TCP client-server monitoring system deployed on Microsoft Azure free-tier VMs. Multiple client agents periodically send heartbeat messages to a central monitoring server, enabling real-time health tracking of distributed components. The project showcases networking, cloud automation, and infrastructure monitoring driven by Site Reliability Engineering (SRE) and DevOps practices.

---

## Objectives

- Build a TCP client-server system for heartbeat monitoring, communication and attachment.
- Provision and configure Azure Virtual Machines (VM) for hosting server and clients.
- Automate deployment and setup using PowerShell scripts.
- Secure networking with TCP ports and Network Security Groups (NSGs).
- Document setup, deployment, and usage in a GitHub repository.
---

 ## Project Deliverables

- **Source Code**  
  - Python TCP Server for heartbeat monitoring and alert logging  
  - Python TCP Client for sending periodic heartbeats and file transfers  
  - PowerShell scripts for automated Azure VM and network provisioning  

- **Azure Infrastructure**  
  - One Monitoring Server VM on Azure (free tier)   
  - Two Client VMs on Azure  
  - Virtual Network, Subnets, and Network Security Groups (NSGs) configured for secure TCP communication  
  - Public IPs assigned where necessary  

- **Documentation**  
  - Comprehensive README with project overview, setup, deployment instructions  
  - Architecture diagram illustrating system design and Azure networking  
  - Step-by-step deployment guide with screenshots  
  - Troubleshooting and enhancement suggestions  

- **Demonstration Artifacts**  
  - Screenshots or recordings showing heartbeat monitoring in action  
  - Logs demonstrating detection of missed heartbeats and alerts  
  - Sample client interactions including file transfer handshakes  

- **Version Control**  
  - GitHub repository with full commit history and version tags  
  - Branches reflecting development milestones and stable releases  

---

## System Architecture

- **Monitoring Server VM:** Runs a TCP server listening for heartbeat, messages and attachement
- **Client Agent VMs:** Run TCP clients sending heartbeats every 20 seconds, messages and attachment
- **Azure Network:** Configured with NSGs allowing TCP ports, subnet segmentation, and public IPs.

---

## Technology Stack

- Python (socket programming for server and client)
- Azure CLI & PowerShell scripting for automation
- Azure Virtual Machines and Networking
- Git and GitHub for version control and documentation

---
## Running the TCP Heartbeat Monitoring System on WSL

### Overview

WSL (Windows Subsystem for Linux) allows you to run a Linux environment directly on Windows without a traditional virtual machine. You can develop, test, and run your TCP heartbeat monitoring server and clients inside WSL as if on a native Linux machine.

---

### Setup Steps for WSL

1. **Install WSL on your Windows machine** (if not already installed).  
   - Use the command in PowerShell:  
     ```
     wsl --install
     ```
   - Choose a Linux distribution (e.g., Ubuntu).

2. **Open your WSL terminal** (e.g., Ubuntu).

3. **Ensure Python 3 is installed** in WSL:  
## Installing Python 3 on WSL/Linux

### Step 1: Update Package Lists

Open your WSL terminal and run:
```
sudo apt update
```
 
### Step 2: Install Python 3 and pip

Install Python 3 by running:
```
sudo apt install python3
```
### Check the version of python by running 
```
python3 -version
```
## Running the TCP Heartbeat Monitoring System Locally

### Python Code Locations

- **Server code:** Located in `tcp-monitoring/server.py`  
  This script implements the TCP monitoring server that listens for client connections, receives heartbeat messages, and receive files

- **Client code:** Located in `tcp-monitoring/client.py`  
  This script implements the TCP client agent that connects to the server and sends heartbeat messages every 20 seconds. It also have files for file transfer handshake protocol.

---

### Running the Code

1. Start the server in a terminal:



5. **Run the Server:**  
```
python3 server.py
```
This will start the TCP server listening on the default port (e.g., 5001).
```
python3 client.py
```
Clients will connect using `localhost` or `127.0.0.1` and start sending heartbeat messages.

---

### Key Points

- **Networking:**  
Inside WSL, `localhost` resolves to the Windows host machine’s loopback interface, so server and client communicate seamlessly.

- **Multiple Terminals:**  
You can open multiple WSL terminal windows or tabs to run multiple clients and the server simultaneously.

- **File Sharing:**  
WSL can access Windows files, so you can edit scripts with Windows editors and run in WSL.

- **Performance:**  
Networking performance in WSL is generally comparable to native Linux for development.

---

### Benefits of Running in WSL

- Windows users get a native Linux environment for development.  
- No need to configure full virtual machines or cloud until ready.  
- Simplifies testing your TCP server and clients on a real Linux stack locally.

---

### Transition to Cloud

Once your testing in WSL is stable, the same scripts and logic can be migrated with minimal changes to Azure Virtual Machines for production-like deployment scenarios.

---

**Note:** Ensure your local firewall or antivirus software allows TCP traffic on your chosen port.

## Deployment & Automation

### Prerequisites

- Azure free-tier subscription  
- Installed Azure CLI and PowerShell  
- Python 3.x installed locally
### Azure VM Provisioning Using PowerShell Scripts

#### Step 1: Log in to Azure Portal

Access the Azure Portal to manage your subscription and resources:

[https://portal.azure.com](https://portal.azure.com)  

Sign in with your Azure credentials.

---

#### Step 2: Run the PowerShell Deployment Script

Open PowerShell (Windows PowerShell, PowerShell Core, or Azure Cloud Shell) and run the deployment script included in this repository:
```

```

Ensure you are signed in to Azure in your PowerShell session by running:
```
Connect-AzAccount
```

### 
---

#### Step 3: What the Script Does

This script automates the creation and configuration of essential Azure resources for the TCP heartbeat monitoring system:

- **Three Virtual Machines (VMs):**  
- **Network Security Group (NSG):**  
- **Public IP Addresses:**  
- **Virtual Network (VNet):**  
  Sets up a private network space to securely connect your VMs.
---

After the script completes, your Azure environment will have all the resources required to deploy and run the monitoring system.

You can then connect to the VMs via RDP and used bash scipting connect you vm using SSH to start the server and client applications as detailed in the usage section.
---
## Testing the TCP Heartbeat Monitoring System Locally

### 1. Verify Python Installation

Ensure Python 3 is installed and accessible:
```
python3 --version
```

### 2. Run the Server

Start the TCP server:
```
python3 <>filename>server.py
```

Confirm the server starts without errors and is listening on port 5001 (default).
### Rune one or more client 
```
python3 tcp-monitoring/client.py
```

Clients will connect to `localhost:5001` and start sending heartbeats every 20 seconds.

---

### 4. Test Connection

- Verify that clients connect successfully (logger should print connection messages).
- On the server console, observe connection notifications from each client.

Optionally, on separate terminal windows you can check TCP port usage:
```
ss -tuln
```

---

### 5. Monitor Heartbeats

- On the server, watch console logs for received heartbeat messages with timestamps.
- Clients print logs of sent heartbeats.

---

### 6. Test Messaging Feature

- In the client terminal, send chat messages to the server as prompted.
- Confirm server receives and logs these messages.
- Server can respond with messages back to the client.

---

### 7. Test File Transfer

- From the client, send small test files (within 40 KB limit by default).
- Observe server response of `READY|filename` or `REJECT|filename` for oversized files.
- Confirm files are saved to `received_files` folder on the server side.

---

### 8. Simulate Failure and Alert

- Stop one client abruptly (e.g., Ctrl+C).
- Wait beyond the configured heartbeat timeout (e.g., 60 seconds).
- Server should log an alert indicating a missed heartbeat.

---

### 9. Connection Termination

- Test graceful closing of client connections (e.g., by typing `bye` or ending with `END`).
- Check server connection close logs.

---

This completes a full validation of your TCP heartbeat monitoring system in a local setup.

---

Open new terminal windows/tabs and start client agents:
## Negative Test: File Size Rejection

- **Purpose:** Confirm that files larger than 40 KB are rejected by the server as per protocol.

- **Test Steps:**  
1. Attempt to send a file larger than 40 KB from the client.  
2. The server should respond with a rejection message like:  
   ```
   REJECT|filename.ext
   ```  
3. The client should log that the file was rejected and skip sending the file data.  
4. The server should NOT save any rejected files into the `received_files` folder.

- **Expected Result:**  
- Server rejects files exceeding 40 KB limit.  
- Client honors rejection and does not send file content.

---

### 3. Connection Closing Scenarios

- **Graceful Close With 'bye' or 'END':**  
- Both server and client support closing connections by clients sending `"bye"` or `"END"`.  
- Verify that the connection closes cleanly, and server logs `"Connection from <addr> closed."`.

- **Abrupt Close Without 'bye':**  
- Client can close connection without sending `"bye"` by simply terminating the process (e.g., `Ctrl+C`).  
- Server detects the disconnection and logs the connection closure appropriately.  
- Heartbeat monitoring alerts may trigger if no reconnect occurs within timeout.

- **Validation:**  
- Test both closing scenarios and observe expected server log behavior.  
- Confirm no dangling open connections or resource leaks.

---

### Summary

- Local client and server should establish reliable TCP connections and exchange heartbeat and messages.  
- File transfer respects size limits with proper handshake rejecting oversized files.  
- Connections can be closed gracefully or abruptly with server managing state correctly.
## Testing the TCP Heartbeat Monitoring System on Azure Cloud
## Limitations of Connecting to Azure VMs via SSH from Linux

When using a Linux SSH client to connect to Azure Virtual Machines, you may encounter several common limitations and challenges:

### 1. SSH Key Management

- SSH connections require properly generated and configured public/private key pairs.  
- If the private key on your Linux machine does not match the public key configured on the Azure VM, authentication will fail.  
- Permissions of the private key file must be restricted (e.g., `chmod 600 ~/.ssh/id_rsa`), or SSH will refuse to use the key.

### 2. Network Security Group (NSG) Restrictions

- The Azure NSG must explicitly allow inbound traffic on port 22 (SSH).  
- Default NSG settings might block SSH access, causing connection timeouts.

### 3. Firewall and Local Network Issues

- Local firewalls (e.g., on your Linux desktop or corporate network) may block outbound SSH connections.  
- Some ISPs or corporate networks restrict outbound port 22 traffic.

### 4. VM State and Configuration

- The Azure VM must be running and have SSH services installed and active.  
- Incorrect VM provisioning or misconfigured SSH daemon can cause connection failures.

### 5. DNS and IP Address Errors

- Using incorrect public IP addresses or DNS names (especially if dynamic IPs are not static) leads to connection failures.  
- Ensure you have the current public IP or DNS of the VM before connecting.

### 6. Usernames and Authentication Methods

- Using incorrect usernames (e.g., `root` vs Azure-assigned usernames) may cause login failure.  
- Azure typically requires SSH key authentication by default, and password authentication is disabled.

---

### Summary

While Linux SSH clients are powerful and standard, successful connection to Azure VMs requires meticulous setup of keys, network security, VM readiness, and proper addressing. Misconfigurations in any of these areas commonly cause connection failures.
---
### Testing Connectivity to Azure VMs

Once your Azure VMs and networking resources are deployed, you can verify network connectivity using the following PowerShell commands on your local machine or Azure Cloud Shell:

#### 1. Test TCP Port Connectivity

Use `Test-NetConnection` to check if the server VM is reachable on the TCP monitoring port (default: 5001):
```
Test-NetConnection -ComputerName <VM_Public_IP_or_DNS> -Port 5001
```

- Replace `<VM_Public_IP_or_DNS>` with the public IP address or DNS name of your server VM.
- A successful `TcpTestSucceeded: True` indicates the port is open and reachable.

#### 2. Ping the VM

Use `ping` to check if the VM is reachable at the network level:
```
ping <VM_Public_IP_or_DNS>
```

- This sends ICMP echo requests to verify basic network connectivity.
- Note that some Azure VMs or NSGs may block ICMP traffic, so lack of response does not always mean the VM is down.

---

### Troubleshooting Tips

- Ensure the Network Security Group (NSG) rules allow inbound traffic on the required ports.
- Confirm the VM is running and its public IP is correctly assigned.
- Try connectivity tests from your local machine and the Azure Cloud Shell for comparison.

---

These commands help confirm your monitoring server and clients can communicate over the network as expected before running the TCP heartbeat system.
## Conclusion and Results

### Summary of Testing

- The Azure Virtual Machines provisioned via PowerShell scripts were successfully created, including:
  - Three VMs (one Monitoring Server VM and two Client Agent VMs).
  - Network Security Groups (NSGs) properly configured to allow relevant inbound traffic.
  - Public IPs and Virtual Network (VNet) set up for secure communication.

- Connectivity testing using PowerShell commands (`Test-NetConnection`) confirmed:
  - RDP port 3389 was reachable on Windows server VMs, enabling remote desktop access.
  - Monitoring server port (default 5001) was accessible, allowing TCP heartbeat communication.

- Remote access via RDP was established successfully on Windows VMs.
- SSH connection attempts from Linux encountered common limitations including key misconfiguration and blocked ports.
- Heartbeat messages from client agents were reliably received by the monitoring server.
- Alerts were correctly triggered on missed heartbeats during negative testing scenarios.
- File transfer functionality respected the configured file size limit (40 KB), rejecting oversized files as expected.
- Both graceful connection terminations (using 'bye' or 'END') and abrupt disconnections were handled appropriately by the server.

---

### Lessons Learned

- Automating Azure VM provisioning with PowerShell scripts streamlines environment setup for distributed monitoring systems.
- Proper NSG rules and firewall configurations are critical for successful connectivity.
- PowerShell provides a more integrated experience managing Azure VMs than Linux SSH clients out-of-the-box.
- Robust client-server communication including heartbeat, messaging, and file transfer protocols can be built using Python socket programming.
- Thorough testing including positive and negative scenarios is vital to ensure system reliability in cloud environments.

---

This project demonstrates a complete cycle from coded applications through cloud deployment, testing, and validation, laying a strong foundation for production-grade distributed monitoring systems.

---

*Thank you for your attention! Feel free to explore the repository for code, scripts, and detailed documentation to replicate or extend this project.*

[Go here](https://github.com/Tanisha-221/Load_Balancer-VM_Scale/blob/main/Docs/Networking/1.%20Basics.md)

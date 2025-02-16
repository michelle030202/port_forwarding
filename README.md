# SSH Local and Remote Port Forwarding 

This project enables **Local** and **Remote Port Forwarding** using `paramiko` to create SSH tunnels.  
It allows secure access to remote services as if they were running locally.

---

## Features

- **Local Port Forwarding** (`localhost:8080` → `remote_host:80`)  
  Redirects local requests to a remote server over SSH.
  
- **Remote Port Forwarding** (`remote_host:9000` → `localhost:5000`)  
  Opens a port on the remote SSH server and forwards incoming traffic back to a local service.

---

## 📦 Installation

### **1️⃣ Prerequisites**
```pip install -r requirements.txt

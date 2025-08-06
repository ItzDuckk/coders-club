# Simple Remote Desktop Control

A basic Python remote desktop application that allows you to control a remote computer's mouse and keyboard while viewing its screen.

## Files Created:
- `server.py` - Captures your input and displays the remote screen
- `client.py` - Receives input commands and sends screenshots back
- `requirements.txt` - Required Python packages

## Setup Instructions:

1. **Install dependencies on both computers:**
   ```bash
   pip install -r requirements.txt
   ```

## For Local Testing (Same Computer):
2. **Run the server first:**
   ```bash
   python server.py
   ```

3. **Run the client:**
   ```bash
   python client.py
   ```

## For WiFi Connection (Different Computers):

### Easy Method (Use Batch Files):
2. **On the SERVER computer** (computer you control FROM):
   - Double-click `start_wifi_server.bat`
   - Note the IP address shown (e.g., 192.168.1.100)

3. **On the CLIENT computer** (computer you want to control):
   - Double-click `start_wifi_client.bat`
   - Enter the server's IP address when prompted

### Manual Method:
2. **Find server IP** (on control computer):
   ```bash
   python find_ip.py
   ```

3. **Start server** (on control computer):
   ```bash
   python server.py
   ```

4. **Start client** (on target computer):
   ```bash
   python client_wifi.py 192.168.1.100
   ```
   (Replace 192.168.1.100 with your actual server IP)

## How it works:
- The **server** captures your mouse and keyboard input and sends it to the client (runs on port 8888)
- The **client** receives these commands and executes them on the remote machine  
- The **client** sends screenshots every 5 seconds back to the server
- The **server** displays screenshots in a GUI window that updates automatically

## Security Note:
This is a basic implementation for learning purposes. For production use, add authentication and encryption.
# Simple script to find your computer's WiFi IP address
import socket  # For network operations

def get_wifi_ip():
    """Find this computer's WiFi IP address"""
    try:
        # Create a dummy socket connection to get local IP
        # This doesn't actually connect, just finds the route
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to a remote address (Google DNS) to find local IP
            s.connect(("8.8.8.8", 80))
            # Get the IP address of this machine
            local_ip = s.getsockname()[0]
            return local_ip
    except Exception as e:
        print(f"Error finding IP: {e}")
        return None

if __name__ == "__main__":
    # Get and display the WiFi IP address
    ip = get_wifi_ip()
    if ip:
        print(f"\nYour WiFi IP address is: {ip}")
        print(f"\nTo connect over WiFi:")
        print(f"1. Run server on this computer (IP: {ip})")
        print(f"2. Update client.py line 14 to use: host='{ip}'")
        print(f"3. Run client on the other computer")
        print(f"\nOr use: python client_wifi.py {ip}")
    else:
        print("Could not find WiFi IP address")
        print("Make sure you're connected to WiFi")
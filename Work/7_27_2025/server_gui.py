# Remote Desktop Server with GUI - Simplified launcher
# This is the same as server.py but with a clearer name for GUI version

from server import RemoteServer

if __name__ == "__main__":
    print("Starting Remote Desktop Server with GUI...")
    print("- Screenshots will display in a window")
    print("- Move your mouse and type to control the client")
    print("- Close the window or press Ctrl+C to stop")
    print()
    
    # Create and start the server with GUI
    server = RemoteServer()
    try:
        server.start_server()  # This will show the GUI window
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nShutting down server...")
        server.stop()
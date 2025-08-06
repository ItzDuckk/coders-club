# Remote Desktop Client - Receives input commands and sends screenshots
import socket           # For network communication
import threading        # For handling multiple tasks simultaneously
import json            # For parsing received commands
import time            # For screenshot timing
import io              # For handling byte streams
from PIL import ImageGrab  # For taking screenshots
import pynput           # For controlling mouse and keyboard
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener
from pynput import mouse, keyboard

class RemoteClient:
    def __init__(self, host='192.168.1.100', port=8888):  # Replace with server's actual IP
        self.host = host                    # Server IP address
        self.port = port                    # Server port number
        self.socket = None                  # Socket object for communication
        self.mouse_controller = mouse.Controller()      # Controls mouse movements
        self.keyboard_controller = keyboard.Controller() # Controls keyboard input
        self.running = True                 # Flag to control main loop
        
    def connect_to_server(self):
        """Connect to the remote server"""
        # Create a TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False
    
    def start_client(self):
        """Start the client and begin communication"""
        if not self.connect_to_server():
            return
        
        # Start screenshot sender in a separate thread
        screenshot_thread = threading.Thread(target=self.send_screenshots)
        screenshot_thread.daemon = True  # Thread dies when main program exits
        screenshot_thread.start()
        
        # Start receiving and processing input commands
        self.receive_commands()
    
    def send_screenshots(self):
        """Capture and send screenshots every 5 seconds"""
        while self.running:
            try:
                # Capture screenshot of entire screen
                screenshot = ImageGrab.grab()
                
                # Convert image to bytes
                img_byte_array = io.BytesIO()
                # Save image as PNG format to byte stream
                screenshot.save(img_byte_array, format='PNG')
                # Get the byte data
                img_data = img_byte_array.getvalue()
                
                # Send screenshot size first (4 bytes)
                size_bytes = len(img_data).to_bytes(4, byteorder='big')
                self.socket.send(size_bytes)
                
                # Send the actual screenshot data
                self.socket.send(img_data)
                print("Screenshot sent to server")
                
                # Wait 5 seconds before next screenshot
                time.sleep(5)
                
            except Exception as e:
                print(f"Error sending screenshot: {e}")
                break
    
    def receive_commands(self):
        """Receive and execute input commands from server"""
        buffer = b''  # Buffer to store incomplete messages
        
        while self.running:
            try:
                # Receive data from server
                data = self.socket.recv(1024)
                if not data:
                    break
                
                # Add received data to buffer
                buffer += data
                
                # Process complete messages (separated by newlines)
                while b'\n' in buffer:
                    # Extract one complete message
                    line, buffer = buffer.split(b'\n', 1)
                    
                    # Parse JSON command
                    try:
                        command = json.loads(line.decode())
                        self.execute_command(command)
                    except json.JSONDecodeError as e:
                        print(f"Invalid JSON received: {e}")
                        
            except Exception as e:
                print(f"Error receiving commands: {e}")
                break
    
    def execute_command(self, command):
        """Execute received input command on local machine"""
        cmd_type = command.get('type')
        
        if cmd_type == 'mouse_move':
            # Move mouse to specified coordinates
            x, y = command['x'], command['y']
            self.mouse_controller.position = (x, y)
            
        elif cmd_type == 'mouse_click':
            # Perform mouse click
            x, y = command['x'], command['y']
            button_str = command['button']
            pressed = command['pressed']
            
            # Convert string back to Button enum
            if 'left' in button_str.lower():
                button = Button.left
            elif 'right' in button_str.lower():
                button = Button.right
            elif 'middle' in button_str.lower():
                button = Button.middle
            else:
                return
            
            # Move to position and click/release
            self.mouse_controller.position = (x, y)
            if pressed:
                self.mouse_controller.press(button)
            else:
                self.mouse_controller.release(button)
                
        elif cmd_type == 'mouse_scroll':
            # Perform mouse scroll
            x, y = command['x'], command['y']
            dx, dy = command['dx'], command['dy']
            self.mouse_controller.position = (x, y)
            self.mouse_controller.scroll(dx, dy)
            
        elif cmd_type == 'key_press':
            # Press a key
            key_str = command['key']
            key = self.parse_key(key_str)
            if key:
                self.keyboard_controller.press(key)
                
        elif cmd_type == 'key_release':
            # Release a key
            key_str = command['key']
            key = self.parse_key(key_str)
            if key:
                self.keyboard_controller.release(key)
    
    def parse_key(self, key_str):
        """Convert key string back to pynput key object"""
        # Handle special keys
        if key_str.startswith('Key.'):
            # Special keys like Key.ctrl, Key.alt, etc.
            key_name = key_str.replace('Key.', '')
            try:
                return getattr(Key, key_name)
            except AttributeError:
                return None
        else:
            # Regular character keys
            return key_str if len(key_str) == 1 else None
    
    def stop(self):
        """Stop client and close connection"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("Client stopped")

if __name__ == "__main__":
    # Create and start the client
    client = RemoteClient()
    try:
        client.start_client()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nShutting down client...")
        client.stop()
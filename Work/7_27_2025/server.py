# Remote Desktop Server - Captures input and displays client screen
import socket          # For network communication
import threading        # For handling multiple tasks simultaneously
import json            # For sending structured data
import io              # For handling byte streams
from PIL import Image, ImageTk  # For displaying received screenshots
import pynput          # For capturing mouse and keyboard input
from pynput import mouse, keyboard
import tkinter as tk   # For GUI window
from tkinter import ttk # For better widgets
import time            # For timestamps

class ScreenViewer:
    """GUI window to display remote desktop screenshots"""
    def __init__(self):
        self.root = tk.Tk()                    # Create main window
        self.root.title("Remote Desktop Viewer")  # Set window title
        self.root.geometry("800x600")          # Set initial window size
        
        # Create label to display screenshots
        self.image_label = ttk.Label(self.root)
        self.image_label.pack(expand=True, fill='both')  # Fill entire window
        
        # Status label at bottom
        self.status_label = ttk.Label(self.root, text="Waiting for client connection...")
        self.status_label.pack(side='bottom', fill='x')
        
        self.current_image = None              # Store current image
        
    def update_image(self, pil_image):
        """Update the displayed screenshot"""
        try:
            # Resize image to fit window while maintaining aspect ratio
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height() - 30  # Account for status bar
            
            # Calculate scaling to fit image in window
            img_width, img_height = pil_image.size
            scale_x = window_width / img_width
            scale_y = window_height / img_height
            scale = min(scale_x, scale_y, 1.0)  # Don't upscale
            
            # Resize image
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to tkinter format
            self.current_image = ImageTk.PhotoImage(resized_image)
            
            # Update the display
            self.image_label.configure(image=self.current_image)
            self.status_label.configure(text=f"Connected - Last update: {time.strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"Error updating image: {e}")
    
    def update_status(self, message):
        """Update the status message"""
        self.status_label.configure(text=message)
    
    def start(self):
        """Start the GUI (call this from main thread)"""
        self.root.mainloop()
    
    def close(self):
        """Close the GUI window"""
        self.root.quit()
        self.root.destroy()

class RemoteServer:
    def __init__(self, host='10.0.0.42', port=8888):
        self.host = host                    # Server IP address
        self.port = port                    # Server port number
        self.socket = None                  # Socket object for communication
        self.client_socket = None           # Connected client socket
        self.mouse_listener = None          # Mouse event listener
        self.keyboard_listener = None       # Keyboard event listener
        self.screen_viewer = ScreenViewer() # GUI window for displaying screenshots
        
    def start_server(self):
        """Start the server networking in background thread"""
        # Start server networking in a separate thread
        server_thread = threading.Thread(target=self.run_server_networking)
        server_thread.daemon = True  # Thread dies when main program exits
        server_thread.start()
        
        # Start the GUI on the main thread (required for tkinter)
        self.screen_viewer.start()
    
    def run_server_networking(self):
        """Handle server networking operations"""
        # Create a TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reusing the address if server restarts
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind socket to host and port
        self.socket.bind((self.host, self.port))
        # Listen for incoming connections (max 1 client)
        self.socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")
        
        # Update GUI status
        self.screen_viewer.update_status(f"Server listening on {self.host}:{self.port}")
        
        # Accept client connection
        self.client_socket, addr = self.socket.accept()
        print(f"Client connected from {addr}")
        
        # Update GUI status
        self.screen_viewer.update_status(f"Client connected from {addr}")
        
        # Start input capture in separate threads
        self.start_input_capture()
        # Start receiving screenshots from client
        self.receive_screenshots()
    
    def start_input_capture(self):
        """Start capturing mouse and keyboard events"""
        # Create mouse listener that calls on_mouse_event when mouse moves/clicks
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        # Create keyboard listener that calls on_key_event when keys are pressed
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        # Start both listeners in background threads
        self.mouse_listener.start()
        self.keyboard_listener.start()
        print("Input capture started")
    
    def on_mouse_move(self, x, y):
        """Send mouse movement event to client"""
        event = {'type': 'mouse_move', 'x': x, 'y': y}
        self.send_event(event)
    
    def on_mouse_click(self, x, y, button, pressed):
        """Send mouse click event to client"""
        event = {
            'type': 'mouse_click',
            'x': x, 'y': y,
            'button': str(button),  # Convert button enum to string
            'pressed': pressed      # True for press, False for release
        }
        self.send_event(event)
    
    def on_mouse_scroll(self, x, y, dx, dy):
        """Send mouse scroll event to client"""
        event = {'type': 'mouse_scroll', 'x': x, 'y': y, 'dx': dx, 'dy': dy}
        self.send_event(event)
    
    def on_key_press(self, key):
        """Send key press event to client"""
        try:
            # Try to get the character representation
            key_char = key.char
        except AttributeError:
            # Special keys (ctrl, alt, etc.) don't have .char
            key_char = str(key)
        
        event = {'type': 'key_press', 'key': key_char}
        self.send_event(event)
    
    def on_key_release(self, key):
        """Send key release event to client"""
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)
        
        event = {'type': 'key_release', 'key': key_char}
        self.send_event(event)
    
    def send_event(self, event):
        """Send input event to client as JSON"""
        try:
            # Convert event dictionary to JSON string
            json_data = json.dumps(event)
            # Encode JSON string to bytes and add newline delimiter
            message = json_data.encode() + b'\n'
            # Send message to client
            self.client_socket.send(message)
        except Exception as e:
            print(f"Error sending event: {e}")
    
    def receive_screenshots(self):
        """Continuously receive and display screenshots from client"""
        while True:
            try:
                # Receive screenshot size (4 bytes)
                size_data = self.client_socket.recv(4)
                if not size_data:
                    break
                
                # Convert bytes to integer (screenshot size)
                screenshot_size = int.from_bytes(size_data, byteorder='big')
                
                # Receive the actual screenshot data
                screenshot_data = b''
                while len(screenshot_data) < screenshot_size:
                    # Receive remaining bytes
                    chunk = self.client_socket.recv(screenshot_size - len(screenshot_data))
                    if not chunk:
                        break
                    screenshot_data += chunk
                
                # Convert bytes to PIL Image and display in GUI
                if screenshot_data:
                    image = Image.open(io.BytesIO(screenshot_data))
                    # Update the GUI window with new screenshot
                    self.screen_viewer.root.after(0, self.screen_viewer.update_image, image)
                    print("Screenshot received and displayed in GUI")
                    
            except Exception as e:
                print(f"Error receiving screenshot: {e}")
                break
    
    def stop(self):
        """Clean shutdown of server"""
        # Stop input listeners
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        # Close sockets
        if self.client_socket:
            self.client_socket.close()
        if self.socket:
            self.socket.close()
        
        # Close GUI window
        if self.screen_viewer:
            self.screen_viewer.close()
        
        print("Server stopped")

if __name__ == "__main__":
    # Create and start the server
    server = RemoteServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nShutting down server...")
        server.stop()
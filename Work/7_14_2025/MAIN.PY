import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "files"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        if self.path == '/list':
            files = os.listdir(DIRECTORY)
            file_list = '\n'.join(files)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(file_list.encode())
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        content_type = self.headers['Content-Type']

        if 'multipart/form-data' in content_type:
            boundary = content_type.split("boundary=")[1].encode()
            remainbytes = content_length
            line = self.rfile.readline()
            remainbytes -= len(line)

            if boundary not in line:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing boundary")
                return

            # Read headers (includes filename)
            line = self.rfile.readline()
            remainbytes -= len(line)
            if b'Content-Disposition' not in line:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid upload")
                return

            # Extract filename
            parts = line.decode().split(';')
            filename = None
            for part in parts:
                if "filename=" in part:
                    filename = part.split('=')[1].strip().strip('"')
                    break

            # Skip 2 lines (Content-Type and empty line)
            self.rfile.readline()
            self.rfile.readline()
            remainbytes -= len(line) * 2

            # Save file content
            file_path = os.path.join(DIRECTORY, filename)
            with open(file_path, 'wb') as f:
                while remainbytes > 0:
                    line = self.rfile.readline()
                    remainbytes -= len(line)
                    if boundary in line:
                        break
                    f.write(line)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"File '{filename}' uploaded successfully".encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Unsupported Media Type")

# Setup directory
os.makedirs(DIRECTORY, exist_ok=True)
os.chdir(DIRECTORY)

print("Files in directory:")
for f in os.listdir():
    print("-", f)

# Start server
handler_object = MyHttpRequestHandler
with socketserver.TCPServer(("", PORT), handler_object) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()

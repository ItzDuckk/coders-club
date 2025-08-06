import socket
import ssl
from cryptography.fernet import Fernet

def send_to_client(conn, message):
    conn.sendall(message.encode())

def generate_key(path):
    key = Fernet.generate_key()
    with open (path , 'a') as file:
        file.write('\n'+key.decode())
        print("writing key into storage")
    return key

HOST = 'localhost'
PORT = 12345

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# create socket
bind_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bind_socket.bind((HOST, PORT))

# socket lisening
bind_socket.listen(1)

print(f"[SERVER] Listening with SSL on {HOST}:{PORT}...")
client_socket, addr = bind_socket.accept()


ssl_conn = context.wrap_socket(client_socket, server_side=True)
print(f"[SERVER] Secure connection from {addr}")

# send key
key_storage_path = r"C:\Users\guysh\OneDrive\מסמכים\coders-club\Work\8_3_2025\Keys\key_list.txt"
send_to_client(ssl_conn, generate_key(key_storage_path).decode())


# close socket
ssl_conn.close()
bind_socket.close()

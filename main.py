import time
from _thread import *
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import socket
import tqdm
import os
server_dir = str(os.getcwd())
server_dir_len = len(server_dir)


def create_usr_dir(cwd):
    global server_dir_len
    cwd = cwd[server_dir_len:]
    return cwd


print(create_usr_dir(server_dir))


class Ftp:
    def ftp_server(self, SERVER_PORT=5001):
        SERVER_HOST = "0.0.0.0"
        BUFFER_SIZE = 65536
        SEPARATOR = "<SEPARATOR_Named_Joe>"
        s = socket.socket()
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        client_socket, address = s.accept()
        print(f"[+] {address} is connected.")
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb+") as f:
            for _ in progress:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))
        client_socket.close()
        s.close()
        with open(filename, "r") as file:
            return file

    def ftp_client(self, filename, host="192.168.0.11", port=5001):
        SEPARATOR = "<SEPARATOR_Named_Joe>"
        BUFFER_SIZE = 65536
        filesize = os.path.getsize(filename)
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            for _ in progress:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
        s.close()


ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


class CryptoMain:
    def __init__(self, mainkey=None, juststop=False):
        self.mainkey = mainkey
        self.juststop = juststop

    def getkeyfp(self, passwd, salt, fn=None):
        if self.juststop is False:
            password_provided = passwd
            password = password_provided.encode("utf-8")
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt.encode("utf-8"), iterations=100000,
                             backend=default_backend())
            key = base64.urlsafe_b64encode(kdf.derive(password))
            if fn is not None:
                file = open(fn, 'wb')
                file.write(key)
                file.close()
            else:
                return key
        else:
            print("Nah LOL")

    def readkey(self, filename):
        if self.juststop is False:
            file = open(filename, 'rb')
            key = file.read()
            file.close()
            return key
        else:
            print("Nah LOL")

    def encrypttext(self, key, text):
        if self.juststop is False:
            message = text.encode()
            f = Fernet(key)
            encrypted = f.encrypt(message)
            return encrypted
        else:
            print("Nah LOL")

    def decodetext(self, key, text, isbytes=False):
        if self.juststop is False:
            if isbytes:
                encrypted = text
            else:
                encrypted = text.encode()
            f = Fernet(key)
            decrypted = f.decrypt(encrypted)
            return decrypted
        else:
            print("Nah LOL")


def threaded_client(connection):
    server_private_key = rsa.generate_private_key(public_exponent=65537, key_size=4000, backend=default_backend())
    print("Private Key Generated")
    server_public_key = server_private_key.public_key()
    print("Public Key Generated")
    crypt = CryptoMain()
    serial_pub = server_public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    connection.send(serial_pub)
    print("Public Key Sent")
    encrypted_client_key = connection.recv(2048)
    print("Encrypted Client Key Received")
    client_key = server_private_key.decrypt(encrypted_client_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print("Client Key Decrypted")
    global server_dir
    """
        try:
        while True:
            data = crypt.decodetext(client_key, connection.recv(2048))
            print(address + " said: \n" + data.decode('utf-8'))
            reply = input("Response: ")
            crypt.encrypttext(client_key, reply)
            if not data:
                reply = crypt.encrypttext(client_key, "Go Away")
                connection.sendall(reply)
                break
            connection.sendall(reply)
    except Exception as e:
        print("Waived Exception: " + str(e))
        reply = crypt.encrypttext(client_key, "Go Away")
        connection.sendall(reply)
    finally:
        print(str(address) + " was terminated")
    #----------------------------------------------------------------------------------------------------------------#
    message = b'encrypt me!'

    encrypted = server_public_key.encrypt(message,
                                          padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                                          algorithm=hashes.SHA256(), label=None))
    print(encrypted)
    original_message = server_private_key.decrypt(encrypted, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                          algorithm=hashes.SHA256(), label=None))
    print(original_message)
    """
    import random
    pin = str(random.randint(9999999999999999999999999, 999999999999999999999999999999999999999999999999999999999999999))
    print(str(address), " - Chain Code: ", pin)
    while True:
        try:
            data = crypt.decodetext(client_key, connection.recv(2048), isbytes=True)
            print(str(address), " said: ", data.decode('utf-8'))
            if not data:
                reply = crypt.encrypttext(client_key, "Go Away")
                connection.sendall(reply)
                break
            data_decoded = data.decode('utf-8').lower()
            if data_decoded == "exit":
                print("Client Induced Exit")
            elif pin is not None and str(data_decoded) == str(pin):
                print(str(address), ": Access Granted")
                reply = "Access Granted"
                connection.sendall(crypt.encrypttext(client_key, reply))
                break
            else:
                reply = "Bad Chain Code"
                pin = str(random.randint(9999999999999999999999999, 999999999999999999999999999999999999999999999999999999999999999))
                print(str(address), " - Chain Code: ", pin)
            connection.sendall(crypt.encrypttext(client_key, reply))
        except Exception as e:
            print("Error: ", str(e))
    try:
        while True:
            data = crypt.decodetext(client_key, connection.recv(2048), isbytes=True)
            print(address, " said: ", data.decode('utf-8'))
            if not data:
                reply = crypt.encrypttext(client_key, "Go Away")
                connection.sendall(reply)
                break
            data_decoded = data.decode('utf-8').lower()
            if data_decoded == "exit":
                print("Client Induced Exit")
                reply = "Go Away"
            elif data_decoded[:2] == "cd":
                print("Current Directory Command Executed")
                if data_decoded == "cd":
                    reply = os.getcwd()
            elif data_decoded[:3] == "dir":
                reply = str(os.listdir())
            else:
                reply = "Error: Command not found"
            connection.sendall(crypt.encrypttext(client_key, reply))
    except:
        print("Exception Waived")
    finally:
        print(str(address) + " was terminated")
        connection.close()


if __name__ == '__main__':
    try:
        while True:
            Client, address = ServerSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(threaded_client, (Client,))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))
    except:
        print("Server Main was terminated")
    finally:
        ServerSocket.close()

from _thread import *
import socket
import json
import os
ServerSocket = socket.socket()
host = '192.168.0.11'
print(host)
port = 2048
ThreadCount = 0
sd = False
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


def getjsondata(filename="data.json", lang="Py"):
    with open(filename, "r") as ham:
        x = ham.read()
        if lang == "J":
            return x
        else:
            return json.loads(x)


def addjsondata(data, filename="data.json"):
    with open(filename, "w") as crowd:
        crowd.write(data)


def threaded_client(connection):
    death = 1
    try:
        while True:
            data = connection.recv(2048)
            print(address, " said: ", data.decode('utf-8'))
            if not data:
                reply = "Go Away"
                connection.sendall(reply)
                break
            data_decoded = data.decode('utf-8').lower()
            if data_decoded == "exit":
                print("Client Induced Exit")
                reply = "Go Away"
            elif data_decoded == "sjd-j":
                reply = str(getjsondata(lang="J"))
            elif data_decoded == "sjd-py":
                reply = str(getjsondata(lang="Py"))
            elif "kill" in data_decoded and data_decoded[5:] == "759135":
                print("Kill Code 759135")
                reply = "Kill Code Init"
                os._exit(0)
            elif "ping" == data_decoded:
                reply = "ping ding ling"
            elif "pm" == data_decoded[:2]:
                reply = data_decoded[3:]
                jsonstuff = getjsondata(lang="Py")
                print(max(jsonstuff[4]))
            else:
                reply = "Error: Command not found"
            connection.sendall(reply.encode("utf-8"))
    except:
        print("Exception Waived")
    finally:
        print(str(address) + " was terminated")
        connection.close()


if __name__ == '__main__':
    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        if sd is True:
            break
    ServerSocket.close()
# 759135

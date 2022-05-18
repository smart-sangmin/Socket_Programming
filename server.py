from socket import *
from threading import *
import time


def threaded(sock, addr, listen_port):
    print('Connected by :', addr[0], ':', addr[1])
    while True:
        try:
            data = sock.recv(1024)
            msg = ""

            if not data or data.decode() == "logoff":
                print('Disconnected by ' + addr[0], ':', addr[1])
                break
            data = data.decode('utf-8')
            print('Received from ' + addr[0], ':', addr[1], data)
            # help command
            if data == "help":
                msg = """
online_users : send a request to the regiServer, get back a list of all online peers and display them on the screen
connect [ip] [port] : request to chat with peer with the given IP and port
disconnect [peer] : end your chat session with the listed peer
talk [peer] [message] : send a message to the peer that you've already initiated a chat with via the \"connect\" command
logoff : send a message (notification) to regiServer for logging of the chat system"""
            # online command
            elif data == "online_users":
                for client in clients:
                    msg += (str(client) + " ")

            sock.send(msg.encode('utf-8'))
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            break
    clients.remove((addr[0], listen_port))
    sock.close()


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 9999))
server_socket.listen()

print('server start')

clients = []
while True:
    sock, addr = server_socket.accept()
    listen_port = sock.recv(1024).decode('utf-8')
    clients.append((addr[0], listen_port))
    Thread(target=threaded, args=(sock, addr, listen_port)).start()
server_socket.close()

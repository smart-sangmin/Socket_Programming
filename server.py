from socket import *
from threading import *


def threaded(client_socket, addr):
    print('Connected by :', addr[0], ':', addr[1])
    client_socket.send(f"{addr[0]}, {addr[1]}".encode())
    while True:
        try:
            data = client_socket.recv(1024)

            if not data or data.decode() == "logoff":
                print('Disconnected by ' + addr[0], ':', addr[1])
                break
            data = data.decode()
            print('Received from ' + addr[0], ':', addr[1], data)
            # help command
            if data == "help":
                msg = """
online_users : send a request to the regiServer, get back a list of all online peers and display them on the screen
connect [ip] [port] : request to chat with peer with the given IP and port
disconnect [peer] : end your chat session with the listed peer
talk [peer] [message] : send a message to the peer that you've already initiated a chat with via the \"connect\" command
logoff : send a message (notification) to regiServer for logging of the chat system
"""
            # online command
            elif data == "online":
                msg = ""
                for client in clients:
                    msg += (str(client) + " ")
            elif data[:7] == "connect":
                msg, ip, port = data.split()
                port = int(port)
                other_addr = (ip, port)
                break
            else:
                msg = "wrong command. try help command"
            client_socket.send(msg.encode())

        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            break
    clients.remove(addr)
    client_socket.close()


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 9999))
server_socket.listen()

print('server start')

clients = []
while True:
    client_socket, addr = server_socket.accept()
    clients.append(addr)
    Thread(target=threaded, args=(client_socket, addr)).start()
server_socket.close()

import time
from socket import *
from threading import Thread


def send(sock, msg):
    msg = str(msg)
    sock.send(msg.encode('utf-8'))


def receive(sock):
    while True:
        data = sock.recv(1024)
        data = data.decode('utf-8')
        try:
            idx = chat_list.index(sock)
            if data:
                print(idx, "번 peer:", data)
            if data == "disconnect":
                chat_list.pop(idx)
                print(idx, "번 peer와의 채팅이 종료되었습니다.")
                break
        except ValueError:
            break
        time.sleep(1)


def s_chat(sock):
    print("\nChatting Program START")
    Thread(target=receive, args=(sock,)).start()


def listen():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", 10003))
    sock.listen()
    while True:
        other, addr = sock.accept()
        print(len(chat_list), "번 peer의 socket object", other)
        chat_list.append(other)
        Thread(target=s_chat, args=(other,)).start()


def connect(ip, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip, port))
    chat_list.append(sock)
    print("접속 완료")
    print("\nChatting Program START")
    Thread(target=receive, args=(sock,)).start()


def server_connect():
    IP, PORT = '127.0.0.1', 9999
    sock = socket(AF_INET, SOCK_STREAM)
    chat_list.append(sock)
    sock.connect((IP, PORT))
    send(sock, listen_port)
    Thread(target=receive, args=(sock,)).start()


listen_port = 10003

# chatting 하는 peer들의 socket 정보
# index 0은 server와 통신하는 socket
chat_list = []
server_connect()
Thread(target=listen).start()

while True:
    msg = input()
    if msg == "help":
        send(chat_list[0], msg)
    elif msg == "logoff":
        print("종료")
        send(chat_list[0], msg)
        exit()
    elif msg == "online_users":
        send(chat_list[0], msg)
    elif msg[:4] == "talk":
        com, peer, msg = msg.split()
        peer = int(peer)
        send(chat_list[peer], msg)
    elif msg[:7] == "connect":
        com, ip, port = msg.split()
        port = int(port)
        connect(ip, port)
    elif msg == "chatting":
        msg = ""
        for c in chat_list:
            msg += str(c.add)
        print(msg)
    elif msg[:10] == "disconnect":
        com, peer = msg.split()
        peer = int(peer)
        send(chat_list[peer], com)
        chat_list.pop(peer)
        print(peer, "번 peer와의 채팅이 종료되었습니다.")
    else:
        print("wrong command. try help command")

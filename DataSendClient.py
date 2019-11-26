import socket
import time
import struct
import math

HOST = '127.0.0.1'
PORT = 52221

initialTime = time.time()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        t = time.time() - initialTime
        dataString = str(t)+","+str(math.sin(t))
        sendData = dataString.encode()
        s.sendall(sendData)
    time.sleep(1)

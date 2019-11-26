import socket
import struct
import threading
import time
import datetime

class CircularBuffer:

    def __init__(self, maxSize = 3600):
        self.queue = [None for i in range(maxSize)]
        self.head = -1
        self.tail = -1
        self.maxSize = maxSize

    def push(self, data):
        if self.isFull():
            print("Queue Full")
            #file output when queue full and flush one value
            return False
        if self.isEmpty():
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = data
        else:
            self.tail = (self.tail+1)%self.maxSize
            self.queue[self.tail] = data
        return True

    def pop(self):
        if self.isEmpty():
            print("Queue Empty")
            #not allowed!!
        elif self.head == self.tail:
            data = self.queue[self.head]
            self.head = -1
            self.tail = -1
            return data
        else:
            data = self.queue[self.head]
            self.head = (self.head + 1) % self.maxSize
            return data

    def isFull(self):
        return ((self.tail+1) % self.maxSize == self.head)

    def isEmpty(self):
        return (self.head == -1)

    def saveToFile(self):
        fname = "User_Log(" + str(datetime.date.today()) + " " + str(datetime.datetime.now().hour) + "." + str(datetime.datetime.now().minute) + "." + str(datetime.datetime.now().second) + ").txt"
        fo = open(fname, "w")
        if(self.head == -1):
            fo.write("Queue is empty")
        elif (self.tail >= self.head):
            for i in range(self.head, self.tail+1):
                fo.write(str(self.queue[i])+"\n")
        else:
            for i in range(self.head, self.maxSize):
                fo.write(str(self.queue[i])+"\n")
            for i in range(0, self.tail+1):
                fo.write(str(self.queue[i])+"\n")
        fo.close()

class ReceiveServer:
    def __init__(self):
        self.t1 = threading.Thread(target = self.receivingThread1)
        #self.recvQ = []
        self.qSize = 10
        self.recvQ = CircularBuffer(maxSize=self.qSize)

    def receivingThread1(self):
        HOST = '127.0.0.1'
        PORT = 52221
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            temp = 0
            while True:
                s.listen(1)
                conn, addr = s.accept()
                with conn:
                    received = conn.recv(512)
                    recData = received.decode()
                    if (temp==self.qSize):
                        print("queue is full write to file")
                        self.recvQ.saveToFile()
                        temp = 0
                    if self.recvQ.isFull():
                        self.recvQ.pop()
                    self.recvQ.push(recData)
                    temp+=1
                    print(recData)

    def receivingThread2(self):
        """
        Ethernet connection with laptop
        """
        HOST = '169.254.232.169'
        PORT = 53334
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            while True:
                s.listen(1)
                conn, addr = s.accept()
                with conn:
                    print("Connected!")
                    received = conn.recv(512)
                    recdata = received.decode()
                    print(recdata)

    def runServer(self):
        self.t1.start()

if __name__ == "__main__":
    server = ReceiveServer()
    server.runServer()
    while True:
        pass

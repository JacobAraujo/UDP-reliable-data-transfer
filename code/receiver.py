import socket
import threading
import queue

messages = queue.Queue()

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(("localhost", 9500))

def receive():
    while True:
        try:
            message, addr = receiver.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass
        
        
cont = 0        
def receiverResponse():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode())
            if isCorrupt(message) or cont > 3:
                nak = make_NAK()
                receiver.sendto(nak.encode(), addr)
                print("enviando nack")
                cont += 1
            else:
                ack = make_ACK()
                receiver.sendto(ack.encode(), addr)
                print("enviando ack")
                
def isCorrupt(message):
    return True

def make_NAK():
    return "NAK"

def make_ACK():
    return "ACK"

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=receiverResponse)

t1.start()
t2.start()
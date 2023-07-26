import socket
import threading
import queue
from utils import checkReceiverChecksum

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
            
def receiverResponse():
    while True:
        while not messages.empty():
            
            message, addr = messages.get()
            message = message.decode().split("|")
            checksum = message[1]
            message = message[0]
            
            if checkReceiverChecksum(message, checksum):
                ack = make_ACK()
                receiver.sendto(ack.encode(), addr)
                print("enviando ack")
                
            else:
                nak = make_NAK()
                receiver.sendto(nak.encode(), addr)
                print("enviando nack")

def make_NAK():
    return "NAK"

def make_ACK():
    return "ACK"

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=receiverResponse)

t1.start()
t2.start()
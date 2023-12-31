import socket
import threading
import queue
from utils import checkReceiverChecksum, findChecksum

messages = queue.Queue()

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(("localhost", 9800))

state_machine = 0
semaphore = threading.Semaphore()

def receive():
    while True:
        try:
            message, addr = receiver.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def send(data, addr, numSeq):
    checksum = findChecksum(data)
    packet = makePacket(data, checksum, numSeq)
    receiver.sendto(packet.encode(), addr)
    
def makePacket(data, checksum, numSeq):
    return f"{data}|{checksum}|{numSeq}"            

def receiverResponse0():
    global state_machine
    while True:
        with semaphore:
            if state_machine == 0:
                              
                while not messages.empty():
                    
                    message, addr = messages.get()
                    message = message.decode().split("|")
                    
                    checksum = message[1]
                    numSeq = message[2]
                    message = message[0]
                    
                    if checkReceiverChecksum(message, checksum) and numSeq == '0':
                        ack = make_ACK()
                        send(ack, addr, 0)
                        print("enviando ack 0")
                        state_machine = 1
                        
                    elif not checkReceiverChecksum(message, checksum) or numSeq == '1':
                        ack = make_ACK()
                        send(ack, addr, 1)
                        print("enviando ack 1")
                        
                        
def receiverResponse1():
    global state_machine
    while True:
        with semaphore:
            if state_machine == 1:
                              
                while not messages.empty():
                    
                    message, addr = messages.get()
                    message = message.decode().split("|")
                    checksum = message[1]
                    numSeq = message[2]
                    message = message[0]
                    
                    if checkReceiverChecksum(message, checksum) and numSeq == '1':
                        ack = make_ACK()
                        send(ack, addr, 1)
                        print("enviando ack 1")
                        state_machine = 0
                        
                    elif not checkReceiverChecksum(message, checksum) or numSeq == '0':
                        ack = make_ACK()
                        send(ack, addr, 0)
                        print("enviando ack 0")
                        
                    # elif numSeq == '0':   ## verificar qual o comportamento correto
                    #     ack = make_ACK()
                    #     send(ack, addr, 1)
                    #     print("enviando ack")
                

def make_NAK():
    return "NAK"

def make_ACK():
    return "ACK"

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=receiverResponse0)
t3 = threading.Thread(target=receiverResponse1)

t1.start()
t2.start()
t3.start()
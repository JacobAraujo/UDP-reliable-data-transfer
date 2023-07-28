import socket
import threading
import queue
from utils import findChecksum, checkReceiverChecksum

messages = queue.Queue()
toSend = queue.Queue()

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.bind(("localhost", 9999))

state_machine = 1
semaphore = threading.Semaphore()

def receive():
    while True:
        try:
            message, addr = sender.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass
        
def send(data, addr, numSeq):
    checksum = findChecksum(data)
    packet = makePacket(data, checksum, numSeq)
    sender.sendto(packet.encode(), addr)
    
def makePacket(data, checksum, numSeq):
    return f"{data}|{checksum}|{numSeq}"
        
def waitSend0(): # state 1
    global state_machine
    while True:
        with semaphore:
            if state_machine == 1:
                message = input("Menssagem: ")
                addr = input("Destino: ")
                
                send(message, (addr, 9500), 0)
                toSend.put((message, (addr, 9500)))
                state_machine = 2
                
def waitSend1(): # state 3
    global state_machine
    while True:
        with semaphore:
            if state_machine == 3:
                message = input("Menssagem: ")
                addr = input("Destino: ")
                
                send(message, (addr, 9500), 1)
                toSend.put((message, (addr, 9500)))
                state_machine = 4
    
def waitResponse1(): # state 4
    global state_machine
    while True:
        with semaphore:
            if state_machine == 4:
                while not messages.empty():
                    message, addr = messages.get()
                    fields = message.decode().split("|")
                    checksum = fields[1]
                    numSeq = fields[2]
                    data = fields[0]
                    
                    print(data)
                    if isNAK(data) or not checkReceiverChecksum(data, checksum): # adicionar verificacao corrompido
                        reSend, addrReSend = toSend.get()
                        print(reSend)
                        send(reSend, addrReSend, 1) # talvez usar send() -> mas e se o ACK/NAK vier corrompido
                        toSend.put((reSend, addrReSend))
                        print("Reenviando pacote")
                    elif isACK(data):
                        print("Confirmacao recebida")
                        state_machine = 1
                        
def waitResponse0(): # state 2
    global state_machine
    while True:
        with semaphore:
            if state_machine == 2:
                while not messages.empty():
                    message, addr = messages.get()
                    fields = message.decode().split("|")
                    checksum = fields[1]
                    numSeq = fields[2]
                    data = fields[0]
                    
                    print(data)
                    if isNAK(data) or not checkReceiverChecksum(data, checksum): # adicionar verificacao corrompido
                        reSend, addrReSend = toSend.get()
                        print(reSend)
                        send(reSend, addrReSend, 0) # talvez usar send() -> mas e se o ACK/NAK vier corrompido
                        toSend.put((reSend, addrReSend))
                        print("Reenviando pacote")
                    elif isACK(data):
                        print("Confirmacao recebida")
                        state_machine = 3
                
def isNAK(message):
    return message == "NAK"
    
def isACK(message):
    return message == "ACK"
                    
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=waitSend0)
t3 = threading.Thread(target=waitSend1)
t4 = threading.Thread(target=waitResponse0)
t5 = threading.Thread(target=waitResponse1)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

# Criando uma instância da máquina de estado





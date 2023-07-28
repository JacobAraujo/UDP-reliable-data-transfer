import socket
import threading
import queue
from utils import findChecksum, checkReceiverChecksum
import time

messages = queue.Queue()

router = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
router.bind(("localhost", 9500))

def receive():
    while True:
        try:
            message, addr = router.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def send(data, addr, numSeq):
    checksum = findChecksum(data)
    packet = makePacket(data, checksum, numSeq)
    router.sendto(packet.encode(), addr)
    
def makePacket(data, checksum, numSeq):
    return f"{data}|{checksum}|{numSeq}"

def route():
    hosts = []
    while True:
        while not messages.empty():
            message, addr = messages.get()
            
            if len(hosts) < 2:
                hosts.append(addr)
                hosts.append(("127.0.0.1", 9800))
            
            fields = message.decode().split("|")
            checksum = fields[1]
            numSeq = fields[2]
            data = fields[0]
            
            if addr == hosts[0]:
                cameFrom = "sender"
            elif addr == hosts[1]:
                cameFrom = "receiver"
                
            print(f'\nA menssagem "{data}"\nVeio do {cameFrom}\nCom numero de sequencia: {numSeq}\n')
            
            actions = input("1 - Corromper bits\nEscolha: ")
            
            if actions == '1':
                change = input(f'Mudar menssagem de "{data}" para: ')
                finalMessage = makePacket(change, checksum, numSeq).encode()
            else: 
                finalMessage = message
            
            if cameFrom == "sender": # se veio do sender
                router.sendto(finalMessage, hosts[1])
            elif cameFrom == "receiver":
                router.sendto(finalMessage, hosts[0])
                
            
        
            
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=route)

t1.start()
t2.start()
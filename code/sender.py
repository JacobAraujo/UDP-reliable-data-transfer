import socket
import threading
import queue


# Perguntas:
# - Sempre vai ser só um sender e só um receiver
# - O sender vai enviar só uma mensagem de cada vez ou vai mandar varias <- talvez respondida pelos videos

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
        
def waitSend():
    global state_machine
    while True:
        with semaphore:
            if state_machine == 1:
                message = input("Menssagem: ")
                addr = input("Destino: ")
                
                sender.sendto(message.encode(), (addr, 9500))
                toSend.put((message.encode(), (addr, 9500)))
                state_machine = 2

def send(data, addr):
    checksum = generateChecksum(data)
    packet = makePacket(data, checksum)
    sender.sendto(packet, addr)
    
def waitResponse():
    global state_machine
    while True:
        with semaphore:
            if state_machine == 2:
                while not messages.empty():
                    message, addr = messages.get()
                    print(message.decode())
                    if isNAK(message.decode()):
                        reSend, addrReSend = toSend.get()
                        sender.sendto(reSend, addrReSend)
                        toSend.put((reSend, addrReSend))
                        print("Reenviando pacote")
                    elif isACK(message.decode()):
                        print("Confirmacao recebida")
                        state_machine = 1
                
            
def isNAK(message):
    return message == "NAK"
    
def isACK(message):
    return message == "ACK"
    
def generateChecksum(data):
    pass
        
def makePacket(data, checksum):
    pass
                    
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=waitSend)
t3 = threading.Thread(target=waitResponse)

t1.start()
t2.start()
t3.start()

# Criando uma instância da máquina de estado





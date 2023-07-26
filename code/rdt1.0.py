import socket
import sys
import threading
import queue

class Sender:
    def __init__(self, receiver_ip, receiver_port):
        # Create a UDP socket
        self.sock = self.create_socket()
        
        self.receiver_addr = (receiver_ip, receiver_port)
        
    def create_socket(self):
        try:
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as err:
            print('Failed to create socket. Error: {}'.format(err))
            sys.exit()
        
        return socket_obj
        
    # rdt_send(data)
    # make_pkt(data)
    # udt_send(packet)
    # rdt_rcv(packet)
    # extract(packet, data)
    # deliver_data(data)

    def send(self, message):
        # Create and send the packet
        packet = self.make_pkt(message)
        self.sock.sendto(packet, self.receiver_addr)

    def make_pkt(self, message):
        packet = message
        return packet.encode()

class Receiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = self.create_socket()

    def create_socket(self):
        """
        Create a UDP socket for the receiver
        """
        try:
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as err:
            print('Failed to create socket. Error: {}'.format(err))
            sys.exit()
        
        return socket_obj

    def bind_socket(self):
        """
        Bind the UDP socket to the specified host and port
        """
        try:
            self.socket.bind()
        except socket.error as err:
            print('Failed to bind socket. Error: {}'.format(err))
            sys.exit()

        
        
def main ():
    choose = input('Sender - 1\nReceiver - 2')
    if choose == 1:
        receiverIp = input('IP do receiver: ')
        sender = Sender()



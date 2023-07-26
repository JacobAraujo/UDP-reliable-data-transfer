# Function to find the Checksum of Sent Message
def findChecksum(SentMessage, k=1):
    SentMessage = stringToBinary(SentMessage)
 
    # Calculating the complement of sum
    Checksum = ''
    for i in SentMessage:
        if(i == '1'):
            Checksum += '0'
        else:
            Checksum += '1'
    return Checksum

def checkReceiverChecksum(ReceivedMessage, Checksum, k=1):
    ReceivedMessage = stringToBinary(ReceivedMessage)
 
    # Calculating the complement of sum
    ReceiverChecksum = ''
    for i in ReceivedMessage:
        if(i == '1'):
            ReceiverChecksum += '0'
        else:
            ReceiverChecksum += '1'
    print(ReceiverChecksum)
    print(Checksum)
    return ReceiverChecksum == Checksum

def stringToBinary(s):
    result = ''.join(format(c, 'b') for c in bytearray(s, "utf-8"))
    return result


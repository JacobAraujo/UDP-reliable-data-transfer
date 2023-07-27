# Function to find the Checksum of Sent Message
def findChecksum(SentMessage):
    SentMessage = stringToBinary(SentMessage)
 
    # Calculating the complement of sum
    Checksum = ''
    for i in SentMessage:
        if(i == '1'):
            Checksum += '0'
        else:
            Checksum += '1'
    return Checksum

def checkReceiverChecksum(ReceivedMessage, Checksum):
    ReceivedMessage = stringToBinary(ReceivedMessage)
 
    # Calculating the complement of sum
    ReceiverChecksum = ''
    for i in range(len(ReceivedMessage)):
        if ReceivedMessage[i] == Checksum[i]:
            return False
            
    return True

def stringToBinary(s):
    result = ''.join(format(c, 'b') for c in bytearray(s, "utf-8"))
    return result


import os
import constants

# TODO: MAC to bin
# TODO: Recieve stack
# TODO: TCP Handshake

def str_to_bin(string):
    return ''.join(format(x, 'b') for x in bytearray(string, 'utf-8'))

def ip_to_Bin(ip):
    return format(int("".join([format(int(ip), "08b") for ip in ip.split(".")]), base=2), "032b")

def ones_comp_add16(num1, num2):
    result = num1 + num2
    return result if result < constants.ONES_COMP_MOD else (result+1) % constants.ONES_COMP_MOD

def calculate_checksum(payload): # ones complement sum of all 16 bit words in a payload
    parts = [int(payload[i:i + 16], base=2) for i in range(0, len(payload), 16)]
    checksum = 0b0
    for num in parts:
        checksum = ones_comp_add16(checksum, num)
    return checksum

def crc(payload):
    rem = payload[:33]
    for i in range(len(payload) - 32):
        if rem[0] == "1":
            rem = "".join([str(int(rem[i])^int(constants.CRC32Poly[i])) for i in range(len(rem))]) # bitwise xor
        if 33 + i < len(payload):
            rem = rem[1:] + payload[33 + i]
        else: # Ensure remainder is 32 bits on last cycle
            rem = rem[1:]
    rem = "".join(["1" if bit == "0" else "0" for bit in rem])[::-1] # bitwise not and reverse entity
    return rem

def calculateFCS(payload):
    payload = "".join([payload[i:i+8][::-1] for i in range(0, len(payload), 8)]) + format(0, "032b") # reverse every byte and pad
    s = "".join(["1" if bit == "0" else "0" for bit in payload[:32]]) + payload[32:] # flip first 32 bits
    return crc(s)

class Client:
    def __init__(self):
        self.ip = constants.CLIENT_IP

    def openConnection(self):
        if not os.path.exists(constants.HTTP_CLIENT2SERVER):
            os.mkfifo(constants.HTTP_CLIENT2SERVER)

    def closeConnection(self):
        try:
            os.remove(constants.HTTP_CLIENT2SERVER)
        except:
            print("Error closing server connection")

    def transmitData(self, payload):
        try:
            with open(constants.HTTP_CLIENT2SERVER, "w") as pipe:
                data = f"{''.join(['0' if i % 2 < 1 else '1' for i in range(56)])}10101011{payload}{0:096b}"
                self.log(data, "b", "Physical (IEEE 802.3)")
                pipe.write(data)
        except:
            print("Error sending request to server")
    
    def recieveData(self):
        try:
            with open(constants.HTTP_SERVER2CLIENT, "r") as pipe:
                data = pipe.read()
                self.log(data, "t", "Physical (IEEE 802.3)")
                return data
        except:
            print("Error recieving response from server")
    
    def log(self, data, key, protocol):
        try:
            if key == "b":
                data = format(int(data, base=2), "x")
                data = " ".join(data[i:i+2] for i in range(0, len(data), 2))
            with open(constants.CLIENT_LOGS, "a") as f:
                f.write(protocol + "\n" + data + "\n\n")
        except:
            print(f"Failed to log data. Data: {data}")

    def generateHTTPRequest(self):
        request = "GET / HTTP/1.1\n Host: www.gollum.mordor/ring.txt"
        self.log(request, "t", "HTTP")
        self.generateTCPPacket(request)

    def generateTCPPacket(self, payload):
        # Source port|Destination port|Sequence number|Ack number|Data offset|Reserved|Flags|Window size|Checksum|Urgent pointer|Payload
        tcpHeader = f"{13370:016b}{80:016b}{0:032b}{128:032b}{5:04b}{0:04b}00010001{65535:016b}{0:016b}{0:016b}"
        checksum = self.generateTCPChecksum(tcpHeader, payload)
        tcpPacket = f"{13370:016b}{80:016b}{0:032b}{128:032b}{5:04b}{0:04b}00010001{65535:016b}{checksum:016b}{0:016b}{str_to_bin(payload)}"
        self.log(tcpPacket, "b", "TCP")
        self.generateIPPacket(tcpPacket)

    def generateTCPChecksum(self, header, payload):
        # Source Address|Destination Address|Reserved|Protocol|Length|TCP Header|Payload
        pseudoPacket = f"{ip_to_Bin(self.ip)}{ip_to_Bin(constants.SERVER_IP)}{0:08b}{6:08b}{len(header) + len(payload):016b}{header}{str_to_bin(payload)}"
        return 2**16 - 1 - calculate_checksum(pseudoPacket) # ones complement of the ones complement sum

    def generateIPPacket(self, payload):
        # IPv4
        # Version|IHL|DSCP|ECN|Total Length|Identification|Flags|Fragment offset|Time to Live(linux kernel 4.10+)|Protocol|Header checksum
        # |Source address|Destination address|Payload
        ipHeader = f"{4:04b}{5:04b}{0:06b}{0:02b}{160 + len(payload):016b}{1:016b}010{0:013b}{64:08b}{6:08b}{0:016b}" \
                   f"{ip_to_Bin(self.ip)}{ip_to_Bin(constants.SERVER_IP)}"
        checksum = 2**16 - 1 - calculate_checksum(ipHeader) # ones complement of the ones complement sum
        ipPacket = f"{4:04b}{5:04b}{0:06b}{0:02b}{160 + len(payload):016b}{1:016b}010{0:013b}{64:08b}{6:08b}{checksum:016b}" \
                   f"{ip_to_Bin(self.ip)}{ip_to_Bin(constants.SERVER_IP)}{payload}"
        self.log(ipPacket, "b", "IPv4")
        self.generateEthernetFrame(ipPacket)

    def generateEthernetFrame(self, payload):
        # IEEE 802.3
        # Destination Address|Source Address|Length|Data|Frame Check Sequence
        ethPacket = f"{2:08b}{0:08b}{0:08b}{0:08b}{0:08b}{0:08b}{2:08b}{0:08b}{0:08b}{0:08b}{0:08b}{1:08b}{len(payload):016b}{payload}"
        frameCheckSequence = calculateFCS(ethPacket)
        ethPacket += frameCheckSequence
        self.log(ethPacket, "b", "IEEE 802.3")
        self.transmitData(ethPacket)
    
        
if __name__ == "__main__":
    
    c = Client()
    c.openConnection()

    while True:
        try:
            usinp = input(">>> ")
            c.generateHTTPRequest()
            data = c.recieveData()
            print(data)
            if usinp == "QUIT":
                raise KeyboardInterrupt

        except KeyboardInterrupt:
            c.closeConnection()
            break
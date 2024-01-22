import os
import constants

# TODO: TCP Handshake

class Client:
    def __init__(self):
        self.ip = constants.CLIENT_IP
        self.mac = constants.CLIENT_MAC

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
                # Add preamble, start frame delimeter and interpacket gap
                data = f"{''.join(['1' if i % 2 < 1 else '0' for i in range(56)])}10101011{payload}{0:096b}"
                self.log(data, "b", "Physical (IEEE 802.3)")
                pipe.write(data)
        except:
            print("Error sending request to server")
    
    def recieveData(self):
        try:
            with open(constants.HTTP_SERVER2CLIENT, "r") as pipe:
                data = pipe.read()
                self.log(data, "t", "Physical (IEEE 802.3)")
        except:
            print("Error recieving response from server")

        for i in range(len(data) - 2):
            if data[i] == data[i+1]:
                ethFrame = data[i+2:-96] # Remove preamble, sfd and interpacket gap
                break
        self.log(ethFrame, "b", "IEEE 802.3")
        self.readEthernetFrame(ethFrame)
    
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
        self.generateTCPPacket(constants.str_to_bin(request))

    def generateTCPPacket(self, payload):
        # Source port|Destination port|Sequence number|Ack number|Data offset|Reserved|Flags|Window size|Checksum|Urgent pointer|Payload
        tcpHeader = f"{13370:016b}{80:016b}{0:032b}{128:032b}{5:04b}{0:04b}00010001{65535:016b}{0:016b}{0:016b}"
        checksum = self.generateTCPChecksumOutbound(tcpHeader, payload)
        tcpPacket = f"{13370:016b}{80:016b}{0:032b}{128:032b}{5:04b}{0:04b}00010001{65535:016b}{checksum:016b}{0:016b}{payload}"
        self.log(tcpPacket, "b", "TCP")
        self.generateIPPacket(tcpPacket)

    def generateTCPChecksumOutbound(self, header, payload):
        # Source Address|Destination Address|Reserved|Protocol|Length|TCP Header|Payload
        pseudoPacket = f"{constants.ip_to_Bin(self.ip)}{constants.ip_to_Bin(constants.SERVER_IP)}{0:08b}{6:08b}{len(header) + len(payload):016b}{header}{payload}"
        return 2**16 - 1 - constants.calculate_checksum(pseudoPacket) # ones complement of the ones complement sum

    def generateIPPacket(self, payload):
        # IPv4
        # Version|IHL|DSCP|ECN|Total Length|Identification|Flags|Fragment offset|Time to Live(linux kernel 4.10+)|Protocol|Header checksum
        # |Source address|Destination address|Payload
        ipHeader = f"{4:04b}{5:04b}{0:06b}{0:02b}{160 + len(payload):016b}{1:016b}010{0:013b}{64:08b}{6:08b}{0:016b}" \
                   f"{constants.ip_to_Bin(self.ip)}{constants.ip_to_Bin(constants.SERVER_IP)}"
        checksum = 2**16 - 1 - constants.calculate_checksum(ipHeader) # ones complement of the ones complement sum
        ipPacket = f"{4:04b}{5:04b}{0:06b}{0:02b}{160 + len(payload):016b}{1:016b}010{0:013b}{64:08b}{6:08b}{checksum:016b}" \
                   f"{constants.ip_to_Bin(self.ip)}{constants.ip_to_Bin(constants.SERVER_IP)}{payload}"
        self.log(ipPacket, "b", "IPv4")
        self.generateEthernetFrame(ipPacket)

    def generateEthernetFrame(self, payload):
        # IEEE 802.3
        # Destination Address|Source Address|Length|Data|Frame Check Sequence
        ethPacket = f"{constants.mac_to_bin(constants.SERVER_MAC)}{constants.mac_to_bin(self.mac)}{len(payload):016b}{payload}"
        frameCheckSequence = constants.calculateFCS(ethPacket)
        ethPacket += frameCheckSequence
        self.log(ethPacket, "b", "IEEE 802.3")
        self.transmitData(ethPacket)

    def readEthernetFrame(self, data):
        # IEEE 802.3
        # Destination Address|Source Address|Length|Data|Frame Check Sequence
        fcs = data[-32:]
        headerData = data[:-32]
        client_fcs = constants.calculateFCS(headerData)
        if fcs != client_fcs:
            raise ValueError(f"Calculated and recieved FCS (Link layer) did not match.\n Calculated: {client_fcs}\n Recieved: {fcs}\n Data: {data}")

        if constants.bin_to_mac(data[:48]) != constants.CLIENT_MAC:
            raise ValueError("MAC address mismatch, data recieved not intended for recipient")
        
        if constants.bin_to_mac(data[48:96]) != constants.SERVER_MAC:
            raise ValueError("MAC address mismatch, data recieved not from server")
        
        ipPacket = data[112:-32]
        self.log(ipPacket, "b", "IPv4")
        self.readIPPacket(ipPacket)

    def readIPPacket(self, data):
        # IPv4
        # Version|IHL|DSCP|ECN|Total Length|Identification|Flags|Fragment offset|Time to Live(linux kernel 4.10+)|Protocol|Header checksum
        # |Source address|Destination address|Payload
        
        header = data[:160]
        header_csum = constants.calculate_checksum(header)
        if header_csum != 0xffff:
            return ValueError(f"IPv4 checksum verification failure. Calculated checksum: {header_csum}")

        if constants.bin_to_ip(header[-32:]) != constants.CLIENT_IP:
            raise ValueError("IP address mismatch, data recieved not intended for recipient")
        
        if constants.bin_to_ip(header[-64:-32]) != constants.SERVER_IP:
            raise ValueError("IP address mismatch, data recieved not from server")
        
        tcpPacket = data[160:]
        self.log(tcpPacket, "b", "TCP")
        self.readTCPPacket(tcpPacket)


    def readTCPPacket(self, data):
        # Source port|Destination port|Sequence number|Ack number|Data offset|Reserved|Flags|Window size|Checksum|Urgent pointer|Payload
        payloadOffset = 160
        calculated_csum = self.generateTCPChecksumInbound(data[:payloadOffset], data[payloadOffset:])
        if calculated_csum != 0xffff:
            return ValueError(f"TCP checksum verification failure. Calculated checksum: {calculated_csum}")
        
        if int(data[16:32], base=2) != 80:
            raise ValueError(f"Source port mismatch, expected port 80 got {int(constants.bin_to_ip(data[16:32]), base=2)}")
        
        httpResponse = data[payloadOffset:]
        self.log(httpResponse, "b", "HTTP")
        self.readHTTPResponse(httpResponse)

    def generateTCPChecksumInbound(self, header, payload):
        # Source Address|Destination Address|Reserved|Protocol|Length|TCP Header|Payload
        pseudoPacket = f"{constants.ip_to_Bin(constants.SERVER_IP)}{constants.ip_to_Bin(self.ip)}{0:08b}{6:08b}{len(header) + len(payload):016b}{header}{payload}"
        return constants.calculate_checksum(pseudoPacket)

    def readHTTPResponse(self, data):
        response = constants.bin_to_str(data)
        self.log(response, "t", "HTTP (Text)")
        print(response)
    
        
if __name__ == "__main__":
    
    c = Client()
    c.openConnection()

    while True:
        try:
            usinp = input(">>> ")
            c.generateHTTPRequest()
            c.recieveData()
            if usinp == "QUIT":
                raise KeyboardInterrupt

        except KeyboardInterrupt:
            c.closeConnection()
            break

        except ValueError as e:
            print(e)
            c.closeConnection()
            break
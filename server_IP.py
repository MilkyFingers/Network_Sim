import constants

class IP:

    def __init__(self):
        pass

    # this method will take a datagram extracted from the link layer, and extract the network layer datagram
    def network_to_transport(self, data):
        tcp_datagram = data[160:]
        return tcp_datagram
    
    # Version|IHL|DSCP|ECN|Total Length|Identification|Flags|Fragment offset|Time to Live(linux kernel 4.10+)|Protocol|Header checksum
    # |Source address|Destination address|Payload
    def network_to_link(self, tcp):
        ip = f"{4:04b}{5:04b}{0:06b}{0:02b}{160+len(tcp):016b}{1:016b}010{0:013b}{64:08b}{6:08b}{0:016b}" \
             f"{192:08b}{168:08b}{1:08b}{1:08b}{192:08b}{168:08b}{1:08b}{0:08b}{constants.strtobin(tcp)}"
        return ip
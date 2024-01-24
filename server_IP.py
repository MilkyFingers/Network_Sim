import constants

class IP:

    def __init__(self, ip = constants.SERVER_IP):
        self.ip = ip

    """
    This method will unpack the IP packet, check the destination IP is correct as well as the checksum and return the tcp segment if the 
    checks pass. 
    """
    def network_to_transport(self, packet):
        # extract the ip 
        dest_ip = packet[160:192]
        # get the checksum
        checksum = packet[80:96]
        # tcp segment
        segment = packet[192:]
        # drop the packet if the checks fail
        if (dest_ip != constants.ip_to_bin(self.ip)) or (checksum != constants.calculate_checksum(packet[:192])):
            pass
        else:
            return segment
    
    # Version|IHL|DSCP|ECN|Total Length|Identification|Flags|Fragment offset|Time to Live(linux kernel 4.10+)|Protocol|Header checksum
    # |Source address|Destination address|Payload
    def network_to_link(self, tcp):
        # variables for all the headers
        version = f"{4:04b}"
        ihl = f"{5:04b}"
        service_type = f"{0:08b}"
        total_length = f"{str(len(tcp) + 160):016b}"
        iden = f"{1:016b}"
        flags = '010'
        fragment_off = f'{0:013b}'
        ttl = f"{64:08b}"
        transport = f"{6:08b}"
        #initially set checksum to 0
        check = f"{0:016b}"
        send_ip = constants.ip_to_bin(self.ip)
        dest_ip = constants.ip_to_bin(constants.CLIENT_IP)
        
        # create a header
        header = version + ihl + service_type + total_length + iden + flags + fragment_off + ttl + transport + check + send_ip + dest_ip
        # calculate the correct checksum
        check = constants.calculate_checksum(header)
        header = version + ihl + service_type + total_length + iden + flags + fragment_off + ttl + transport + check + send_ip + dest_ip
        return header + tcp


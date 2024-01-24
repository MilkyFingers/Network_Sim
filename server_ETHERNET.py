import constants

"""
This class is the ethernet handler. The class has a single attribute - the MAC address of the 'NIC'. When a frame is recieved by the server,
it is handed to this class. For the sake of simplicity, the simulation does not include preamble or ipg in ethernet
"""
class ETHERNET:

    def __init__(self, mac = constants.SERVER_MAC):
        # the mac address - checked against the header
        self.mac = mac

    """
    Method that unwraps IP packet and also checks the destination MAC and crc is correct or frame is dropped. Frame is a byte string.
    If the checks pass, the IP packet (as a byte string) is returned.
    """
    def link_to_network(self, frame):
        # first we must break the frame into its components and check the MAC and crc are correct 
        mac = frame[:48]
        # indexing backwards. crc is a 4 byte value at the end of the frame 
        crc = frame[-32:]
        # if mac and crc are not correct, drop the frame
        if (mac != constants.mac_to_bin(self.mac)) or (crc != constants.calculateFCS(frame[:-32])):
            pass
        else:
            # return the ip packet
            ip_packet = frame[112:-32]
            return ip_packet
    
    """
    Method to encapsulate an IP packet into an ethernet frame ready to sent across the 'network'. As there is no actual network, the destination
    MAC address is a constant defined in the constants files.
    """
    def link_to_physical(self, ip):
        # set the MAC addresses, source being the server MAC in this instance
        src_mac = constants.mac_to_bin(constants.SERVER_MAC)
        des_mac = constants.mac_to_bin(constants.CLIENT_MAC)
        length = "{:016b}".format(len(ip)/8)
        data = ip
        frame = des_mac + src_mac + length + data
        crc = constants.calculateFCS(frame)
        frame += crc
        return frame

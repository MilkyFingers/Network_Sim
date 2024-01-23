import constants
"""
This class is the ethernet handler. The class has a single attribute - the MAC address of the 'NIC'. When a frame is recieved by the server,
it is handed to this class.  
"""
class ETHERNET:

    def __init__(self):
        # the mac address - checked against the header
        self.mac = constants.SERVER_MAC

    def link_to_network(self, data):
        # first we must break the frame into its components
        # we can ignore the first 8 bytes
        #src, des = 
        pass

    def link_to_physical(self, ip):
        # CSMA/CD (IEEE 802.3)
        # Server MAC: 02:00:00:00:00:00 (locally administered unicast address)
        # Client MAC: 02:00:00:00:00:01 (locally administered unicast address)
        eth = f"{''.join(['0' if i % 2 < 1 else '1' for i in range(56)])}10101011" \
        f"{2:08b}{0:08b}{0:08b}{0:08b}{0:08b}{1:08b}{2:08b}{0:08b}{0:08b}{0:08b}{0:08b}{0:08b}{len(ip):016b}{constants.strtobin(ip)}{0:032b}{0:096b}"
        return eth
        # Preamble|Start Frame Delimiter|
        # Destination Address|Source Address|Length|Data|Frame Check Sequence|Interpacket gap
import constants

"""
This class will implement tcp, the transport layer in the OSI model. This class, as with a real tcp protocol, is unaware of the other layers.
If http needs to send a request, tcp must first ensure there is an open connection between the server and the client as it is end to end. 
The tcp object will keep track of IPs that it has an open connection with. 
"""

class TCP:

    def __init__(self):
        # a list of IPs that have a session 
        self.open_connecions = []

    # method to create a connection, i.e the handshake
    def open_connection(self, ip):
        pass

    # method that passes application data to the application running on port. Checks the checksum, returns data and port number for the 'os'.
    def transport_to_application(self, datagram):
        http_data = datagram[160:]
        return http_data

    # a method that bundles up the tcp datagram and returns it
    # Source port|Destination port|Sequence number|Ack number|Data offset|Reserved|Flags|Window size|Checksum|Urgent pointer|Payload
    def transport_to_network(self, http):
        tcp = f"{80:016b}{13370:016b}{0:032b}{128:032b}{5:04b}{0:04b}00010001{65535:016b}{0:016b}{0:016b}{constants.strtobin(http)}"
        return tcp
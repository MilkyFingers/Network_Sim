import constants

"""
This class will implement tcp, the transport layer in the OSI model. This class, as with a real tcp protocol, is unaware of the other layers.
Because TCP is a conection-oriented protocol, a connection must always first be established with the client. For this reason, TCP will always
check incoming segments have an associated open session, stored in the connection_state attribute. The key values are the source and destination 
pairs, the values are the recieved number of bytes and the current ack number. ex: {'80:13370' : [seq, ack]}. The second attribute is used during
handshake to keep track of where in the handshake the process is. 

For example, when TCP recives a syn packeet from a client, it adds an entry
with the client port and sets the status to 'SYN-SENT'. Once the final ack is recieved, it changes its status to established and this is used
to check if incoming segments are associated with an established connection.  
"""

class TCP:

    def __init__(self):
        # a dict of open connections and the sequence and ack numbers for that connection
        self.open_connecions = {}
        # this dict is used during the handshake so tcp can keep track of its state. ex {'80:13370' : 'SYN-SENT'}
        self.connection_state = {}

    # this method will seperate the incoming segment into header fields and data field. NB all these fields are bit strings until converted!
    def parse_segment(self, segment):
        # the first 2 bytes are source port num, the next 2 are destination port
        src_port = segment[:16]
        des_port = segment[16:32]
        seq = segment[32:64]
        ack = segment[64:96]
        flags = segment[106:112]
        checksum = segment[128:144]
        data = segment[160:]
        return src_port,des_port,seq,ack,flags,checksum,data
    
    # this method takes the ports from the incoming segment and returns a bool --> is open connection?
    def open_connection(self, ports):
        return ports in self.open_connecions
    
    # method to return the connection state during handshake
    def connection_state(self, ports):
        return self.connection_state[ports]
    
    # method to deal with handshake if incoming packet is part of handshake 
    def handshake(self, headers):
        # get the ports values
        ports = constants.bin_to_str(headers[1]) + ":" + constants.bin_to_str(headers[0])
        # check to see if there is a connection status
        if ports in self.connection_state:
            state = self.connection_state(ports)
        # else we generate a syn/ack and uopdate the status
        else:
            self.connection_state[ports] = 'SYN-ACK'
            # not implemented yet 
            # self.transport_to_network(message = none, syn_akc=true)    
 

    # this method is always called, it hands over control to handshake if the incoming packet is not assciated with open connection
    def transport_to_application(self, segment):
        headers = self.parse_segment(segment)
        # convert to ascii
        ports = constants.bin_to_str(headers[1]) + ":" + constants.bin_to_str(headers[0])
        # is there an open connection?
        if ports in self.open_connecions:
            # return the data for the application and check the checksum is correct
            data = headers[-1]
            return data
        # else it must be a handshake request
        else:
            self.handshake(headers)

    # this method encapsulates an application message into a tcp segment to be passed down to the network layer. if syn_ack, generate a syn-ack
    def transport_to_network(self, message, syn_ack = False):
        if syn_ack:
            # not implemented
            #return self.generate_syn_ack()
            pass
        else:
            tcp = f"{80:016b}{13370:016b}{0:032b}{128:032b}{5:04b}{0:04b}00010001{65535:016b}{0:016b}{0:016b}{constants.strtobin(message)}"
            return tcp
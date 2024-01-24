import os
import constants
from server_ETHERNET import ETHERNET
from server_IP import IP
from server_TCP import TCP
from server_HTTP import HTTP

"""
This class acts as the os. There are methods to control the reading and writing of data which is to simulate the physical layer of the OSI.
There is also a method to log all the server responses. 
"""

class Server:

    def __init__(self):
        self.ip = constants.SERVER_IP
        if not os.path.exists(constants.SERVER2CLIENT):
            os.mkfifo(constants.SERVER2CLIENT)
        # the file we log all the data in
        self.logfile = constants.SERVER_LOGS
        # instantiate an instance for each layer in the OSI
        self.app = HTTP()
        self.transport = TCP()
        self.network = IP()
        self.link = ETHERNET()

    def read_pipe(self):
        with open(constants.SERVER2CLIENT, "r") as readpipe:
            data = readpipe.read()
        return data

    def write_pipe(self, data):
        with open(constants.CLIENT2SERVER, "w") as writepipe:
            writepipe.write(data)

    def logger(self, data):
        with open(self.logfile, "a") as logfile:
            logfile.write(data)
    
    # this method will take an ethernet datagram and move it up the network stack. the return value is the application (http) response.
    # this return value is passed to down_stack which moves the data down the network stack and passes the final datagram to write_pipe
    def up_stack(self, data):
        ip = self.link.link_to_network(data)
        tcp = self.network.network_to_transport(ip)
        http = self.transport.transport_to_application(tcp)
        response = self.app.req_res(http)
        return response 
    
    def down_stack(self, response):
        tcp = self.transport.transport_to_network(response)
        ip = self.network.network_to_link(tcp)
        ethernet = self.link.link_to_physical(ip)
        return ethernet

    def shutdown(self):
        try:
            os.remove(constants.SERVER2CLIENT)
        except:
            print("Error closing server connection") 

        

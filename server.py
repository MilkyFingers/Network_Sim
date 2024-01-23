import os, sys
import constants, server_HTTP, server_TCP, server_IP, server_ETHERNET

"""
This class acts as the os. There are methods to control the reading and writing of data which is to simulate the physical layer of the OSI.
There is also a method to log all the server responses. 
"""

class Server:

    def __init__(self):
        self.ip = constants.SERVER_IP
        if not os.path.exists(constants.SERVER2CLIENT):
            os.mkfifo(constants.SERVER2CLIENT)

    def read_pipe(self):
        with open(constants.SERVER2CLIENT, "r") as readpipe:
            data = readpipe.read()
        return data

    def write_pipe(self, data):
        with open(constants.CLIENT2SERVER, "w") as writepipe:
            writepipe.write(data)
    
    # this method will take an ethernet datagram and move it up the network stack. the return value is the application (http) response.
    # this return value is passed to down_stack which moves the data down the network stack and passes the final datagram to write_pipe
    def up_stack(self, data):
        ip = server_ETHERNET.link_to_network(data)
        tcp = server_IP.network_to_transport(ip)
        http = server_TCP.transport_to_application(tcp)
        response = server_HTTP.req_res(http)
        return response 
    
    def down_stack(self, response):
        tcp = server_TCP.transport_to_network(response)
        ip = server_IP.network_to_link(tcp)
        ethernet = server_ETHERNET.link_to_physical(ip)
        return ethernet

    def shutdown(self):
        try:
            os.remove(constants.SERVER2CLIENT)
        except:
            print("Error closing server connection") 

        

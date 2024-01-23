import constants
"""
The following class implements an HTTP application running on a server machine. A server_HTTP object takes a single parameter,
the client request. Due to the nature of the simulation, the server will always respond with an HTTP 301 error message. Similar to how an 
application level service in the OSI is unaware of the other layers, this HTTP class has no dependance on the underlying layers. 
"""

class server_HTTP:

    # define the port that http runs on
    def __init__(self, port = 80):
        self.port = port

    # single method that takes the http packet from tcp and returns the 301. This method also calls the log method to capture the response.
    def req_res(self, req):
        # the response is defined here and is always the same
        return "HTTP/1.1 301 Moved Permanently\nLocation: http://www.networksimulations.com"
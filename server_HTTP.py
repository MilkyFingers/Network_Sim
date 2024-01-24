import constants
"""
The following class implements an HTTP application running on a server machine. A server_HTTP object has a single method that
takes a single parameter,the client request. Due to the nature of the simulation, the server will always respond with an HTTP 301 message. 
Similar to how an application level service in the OSI is unaware of the other layers, this HTTP class has no dependance on the underlying layers. 
"""

class HTTP:

    # define the port that http runs on
    def __init__(self, port = 80):
        self.port = port
        # the new locations of the resources on the server, returned in the 301 message.
        self.resource_locations = {"/ring.txt" : "/stock/rings/ring.txt", "/wizzard.jpg" : "/images/magical/wizzard.jpg"}

    # single method that takes the http message from tcp and returns the 301.
    def req_res(self, request):
        # we need to get the requested resource from the message
        resource = ""
        # we can get the resource by fining the substring between the GET and HTTP parts of the message
        for i in range(input.index("GET")+len("GET")+1,input.index("HTTP")):
            resource = resource + input[i]
        # the response is defined here and is always the same
        return "HTTP/1.1 301 Moved Permanently\nLocation: " + self.resource_locations[resource]
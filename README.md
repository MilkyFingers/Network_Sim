# Network_Sim
Python3 simulation for networks assesment

## Part 1

The server application (HTTP) is very simple as no real data is being transferred in the simulation. The class constructor has a single attribute, the port number of the application, which is 80 in the case of HTTP. Due to the fact that the server will always respond with a 300 response code, there is a single method which will simply return a 301 message. This return message will be given to the transport layer (TCP) where it will be encapsulated into a TCP segment.

## Part 2

The TCP layer has 3 methods. One method (transport_to_application) opens the incoming tcp segment and performs a series of checks on the header. Firstly, it checks that the checksum recieved produced on the client side matches the checksum the server produces. This is how tcp ensures there hasnt been any packet corruption. 

 
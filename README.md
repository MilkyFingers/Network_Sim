# Network_Sim
Python3 simulation for networks assesment

## Part 1

The server application (HTTP) is very simple as no real data is being transferred in the simulation. The class constructor has two attributes, the port number of the application (80 in this case) and the locations of resources. Due to the fact that the server will always respond with a 300 response code, there is a single method which will simply return a 301 message. The method takes a single parameter, the incoming request, and returns the 301 message as well as the new location of the resource on the server. This new location is found by indexing into the dictionary of loactions. The message is returned as plain text and this return value is passed to the server class (which simulates the services provided by an os) which directs the message to the TCP service for encapsulation. 

## Part 2

As TCP is a connection-oriented protocol, it must be able to keep track of open connections and the number of bytes recieved/sent. This is how TCP is able to detect missing packets as well as keep recieved packets in order. The class has two object attributes, both dictionary mappings. open_connections is used to determine if the incoming segment is assciated with an open connection. connection_state is used to keep track of the handshake status. 

When an incoming segment is passed to the TCP service, if first checks to see if the ports are associated with an open connection. If they are, the checksum is evaluted (this code has not been implemented yet) to ensure no data corruption has occured. If the checksum is correct, the 
data field is extracted and returned to the server class to be passed to the application layer. 

If it is determined that the packet is not associated with an open connection, the segment is handed to the method 'handshake' which will examine the handshake status using the connection_status attribute. If it finds no entry, the segment is checked for the syn flag. If the syn flag is set, we know we have the first handshake segment. A syn/ack packet is then generated and the status is updated to syn/ack. This packet is then handed down the network stack as normal.

Once we recieve the final ack from the client, we update the status to 'established' and from now on we can simply do the required checks on the incoming segments and pass them up to the application layer.

As TCP is also responsible for flow control, the class can be extended by adding functionality in to break up application data into the appropriate window size for trasnmission. 

## Part 3

The IP class has two methods, one to pass the data up to the TCP layer and another to encapsulate network layers into IP packets to be returned to the server and passed down to the link layer. The method network_to_transport is responsible for checking the incoming packets for data corruption and removing the IP header from the packet. This method checks the destination IP matches the IP of the server (defined in the constants class) as well as calculating the checksum and verfying it matches the checksum recieved in the packet. If both of these conditions are met, the data payload is extracted and returned to the server class. 

The method network_to_link is responsible for encapsulating the transport segment into IP packets. This method creates the correctly formatted header fields as bit strings. In reality, this layer would make use of a DNS to resolve the IP address of the destination. However, due to the nature of the simualtion, we simplify things by making the destination IP a constant in the constant file. Once all of the fields are created, a checksum is calculated over the header and the data is appended to create the final IP packet. This value is returned to the server class to be passed down the network stack to the link layer. 

## Part 4

The ethernet class works in much the same way as the IP class. That is, it check incoming frames to ensure the CRC is correct and there has been no data corruption. If the CRCs are matching, the IP packet is extracted and returned to the server class. If there is a problem the packet is simply dropped. Similarly, the destination MAC is checked against the MAC of the 'NIC' (a constant defined in the constant file) to ensure the frame has arrived at the correct location and need no be forwarded. 

The link_to_physical method creates the correctly formatted headers and encapsualtes the IP packet passed to it and returns this frame to the server class to be sent down a named_pipe (defined in constants) to the 'client'. Due to the nature of the simulation, no frames are generated that are larger than the specified MTU of 750. However, I will explain how I would implement the features to deal with the scenario when this happens. 

Given that ethernet does no fragment frames, this functionality would be implemented at the network layer, i.e in the IP class. Assuming the IP service is configured so that the DF flag is not set and that the MTU of 750 is known, IPv4 can fragment packets into smaller packets suitable for transmision down the badly performing link. 
# Network_Sim
Python3 simulation for networks assesment

## Part 1

The server reads incoming HTTP requests from the pipe HTTP_CLIENT2SERVER and writes a response to the pipe HTTP_SERVER2CLINET
as defined in the constants class. Each time the server responds using a 301 code and copies this into a server log file which is referneced by 
the server object. In order for the communcation to work, the client code must be run first. This will prevent the blocking pipes from causing a deadlock as there is no code to detect and resolve this.  
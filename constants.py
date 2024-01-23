SERVER_IP = "192.168.1.0"
SERVER_NAME = "networksimulation.com"
SERVER_MAC = "02:00:00:00:00:00" # (locally administered unicast address)
CLIENT_IP = "192.168.1.1"
CLIENT_MAC = "02:00:00:00:00:01" # (locally administered unicast address)
NETMASK = "255.0.0.0"
SERVER2CLIENT = "http_pipe_S2C"
CLIENT2SERVER = "http_pipe_C2S"
SERVER_LOGS = "server_logs.txt"
CLIENT_LOGS = "client_logs.txt"
HTTP_300_RESPONSE = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + SERVER_NAME + "\r\n"


# Calculation constants
ONES_COMP_MOD = 1 << 16
CRC32Poly = "100000100110000010001110110110111" # IEEE 802.3 CRC-32 standard polynomial

def strtobin(string):
    return ''.join(format(x, 'b') for x in bytearray(string, 'utf-8'))
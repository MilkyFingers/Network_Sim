SERVER_IP = "192.168.1.0"
SERVER_NAME = "networksimulation.com"
SERVER_MAC = "02:00:00:00:00:00" # (locally administered unicast address)
CLIENT_IP = "192.168.1.1"
CLIENT_MAC = "02:00:00:00:00:01" # (locally administered unicast address)
NETMASK = "255.0.0.0"
HTTP_SERVER2CLIENT = "http_pipe_S2C"
HTTP_CLIENT2SERVER = "http_pipe_C2S"
SERVER_LOGS = "server_logs.txt"
CLIENT_LOGS = "client_logs.txt"
HTTP_300_RESPONSE = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + SERVER_NAME + "\r\n"


# Calculation constants
ONES_COMP_MOD = 1 << 16
CRC32Poly = "100000100110000010001110110110111" # IEEE 802.3 CRC-32 standard polynomial

# Functional constants
def str_to_bin(string):
    return ''.join(format(x, '08b') for x in bytearray(string, 'utf-8'))

def bin_to_str(b):
    return "".join(map(lambda byte: chr(int(byte, base=2)),[b[i:i+8] for i in range(0, len(b), 8)]))

def ip_to_Bin(ip):
    return format(int("".join([format(int(ip), "08b") for ip in ip.split(".")]), base=2), "032b")

def bin_to_ip(b):
    return "".join(map(lambda byte: str(int(byte, base=2)) + ".", [b[i:i+8] for i in range(0, len(b), 8)]))[:-1]

def mac_to_bin(mac):
    return format(int("".join([format(int(mac, base=16), "08b") for mac in mac.split(":")]), base=2), "048b")

def bin_to_mac(b):
    return "".join(map(lambda byte: format(int(byte, base=2), "02x") + ":", [b[i:i+8] for i in range(0, len(b), 8)]))[:-1]

def ones_comp_add16(num1, num2):
    result = num1 + num2
    return result if result < ONES_COMP_MOD else (result+1) % ONES_COMP_MOD

def calculate_checksum(payload): # ones complement sum of all 16 bit words in a payload
    parts = [int(payload[i:i + 16], base=2) for i in range(0, len(payload), 16)]
    checksum = 0b0
    for num in parts:
        checksum = ones_comp_add16(checksum, num)
    return checksum

def crc(payload):
    rem = payload[:33]
    for i in range(len(payload) - 32):
        if rem[0] == "1":
            rem = "".join([str(int(rem[i])^int(CRC32Poly[i])) for i in range(len(rem))]) # bitwise xor
        if 33 + i < len(payload):
            rem = rem[1:] + payload[33 + i]
        else: # Ensure remainder is 32 bits on last cycle
            rem = rem[1:]
    rem = "".join(["1" if bit == "0" else "0" for bit in rem])[::-1] # bitwise not and reverse entity
    return rem

def calculateFCS(payload):
    payload = "".join([payload[i:i+8][::-1] for i in range(0, len(payload), 8)]) + format(0, "032b") # reverse every byte and pad
    s = "".join(["1" if bit == "0" else "0" for bit in payload[:32]]) + payload[32:] # flip first 32 bits
    return crc(s)
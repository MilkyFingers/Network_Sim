"""
Example client packet for testing. Protocols and header items in comments. Checksums have been left blank.
"""

def strtobin(string):
    return ''.join(format(x, 'b') for x in bytearray(string, 'utf-8'))


http = "GET / HTTP/1.1\n Host: www.gollum.mordor/ring.txt"

tcp = f"{13370:016b}{80:016b}{0:032b}{128:032b}{5:04b}{0:04b}00010001{65535:016b}{0:016b}{0:016b}{strtobin(http)}"
# Source port|Destination port|Sequence number|Ack number|Data offset|Reserved|Flags|Window size|Checksum|Urgent pointer|Payload

#IPv4
ip = f"{4:04b}{5:04b}{0:06b}{0:02b}{160+len(tcp):032b}{1:016b}010{0:013b}{64:08b}{6:08b}{0:016b}" \
     f"{192:08b}{168:08b}{1:08b}{1:08b}{192:08b}{168:08b}{1:08b}{0:08b}{tcp}"
# Version|IHL|DSCP|ECN|Total Length|Identification|Flags|Fragment offset|Time to Live(linux kernel 4.10+)|Protocol|Header checksum
# |Source address|Destination address|Payload

# CSMA/CD (IEEE 802.3)
# Server MAC: 02:00:00:00:00:00 (locally administered unicast address)
# Client MAC: 02:00:00:00:00:01 (locally administered unicast address)
eth = f"{''.join(['0' if i % 2 < 1 else '1' for i in range(56)])}10101011" \
      f"{2:08b}{0:08b}{0:08b}{0:08b}{0:08b}{0:08b}{2:08b}{0:08b}{0:08b}{0:08b}{0:08b}{1:08b}{len(ip):016b}{ip}{0:032b}{0:096b}"
# Preamble|Start Frame Delimiter|
# Destination Address|Source Address|Length|Data|Frame Check Sequence|Interpacket gap

print(eth)

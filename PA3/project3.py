import rawsocketpy as rp
import socket

# create a raw socket
raw_socket = rp.RawSocket('eth0', 0x0800)

# bind the socket to a network interface
# raw_socket.bind('eth0')

ipcntr = 0

# start capturing packets
while True:
    packet = raw_socket.recv()

    str = rp.to_str(packet.data, separator="")
    assert str[0] == '4'
    len = str[1]
    assert len == "5"
    # ToS 2-3
    # total length 4-8
    # identification 9-12
    # ... ... ...
    # protocol 18
    protocol = int(str[18:20], base=16)
    
    ipcntr += 1 

    # print packet contents
    # print(rp.to_str(packet.data, separator=""))
    print(f"protocol = {protocol} && total_len = {int(str[4:8], base=16)}")

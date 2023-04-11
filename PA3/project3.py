import rawsocketpy as rp
import socket
import signal

# create a raw socket
raw_socket = rp.RawSocket('eth0', 0x0800)

# bind the socket to a network interface
# raw_socket.bind('eth0')

# needed content
ip_cnt = 0
tcp_cnt = 0
udp_cnt = 0
dns_cnt = 0

# extra credit content
icmp_cnt = 0
http_cnt = 0
https_cnt = 0
quic_cnt = 0

def done(signum, frame):
    print("Done!")
    print(ip_cnt, tcp_cnt, udp_cnt, dns_cnt, icmp_cnt, http_cnt, https_cnt, quic_cnt)
    exit(0)

signal.signal(signal.SIGALRM, done)
signal.alarm(30)

print("Starting!")

# start capturing packets
while True:
    try:
        packet = raw_socket.recv()

        str = rp.to_str(packet.data, separator="")
        # print(int(str, base=16))
        
        assert str[0] == '4'
        header_len = int(str[1], base=16)*4
        assert header_len == 20
        
        # ToS 2-3
        total_len = int(str[4:8], base=16)
        # identification 9-12
        # ... ... ...
        # protocol 18
        protocol = int(str[18:20], base=16)
        data = str[header_len*2:total_len*2]  
        data_len= len(data)/2
        
        # print(f"len(str/2) == {len(str)/2} && total_len = {total_len} && data_len = {data_len} && header_len = {header_len}")
        
        
        # assert len(str)/2 == total_len 
        # assert total_len == data_len+header_len
        
        ip_cnt += 1 
        
        # print(f"protocol = {protocol}")
        match protocol:
            case 6:
                tcp_cnt += 1
                
                src_port = int(data[0:4], base=16)
                # dest_port = int(data[4:8], base=16)
                
                match src_port:
                    case 80:
                        http_cnt += 1
                    case 443:
                        https_cnt += 1
                    
                
                # print(f"src port = {src_port} && dest port = {dest_port}")
                
                
            case 17:
                udp_cnt += 1
                
                src_port = int(data[0:4], base=16)
                # dest_port = int(data[4:8], base=16)
                
                match src_port:
                    case 53:
                        dns_cnt += 1
                    case 443:
                        quic_cnt += 1
                
                # print(f"src port = {src_port} && dest port = {dest_port}")
                        
            case 1:
                icmp_cnt += 1
            


        # print packet contents
        # print(rp.to_str(packet.data, separator=""))
        # print(f"protocol = {protocol} && total_len = {int(str[4:8], base=16)}")
    except AssertionError as e:
        print(e)
        continue
    

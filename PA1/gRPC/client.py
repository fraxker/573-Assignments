# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 10:36:27 2023

@author: Andrew and Sydney
"""

import grpc
from protos import proto_pb2, proto_pb2_grpc
import time
from statistics import mean, stdev
from pathlib import Path


DATAFILES = Path("../Datafiles")

ATenKB = DATAFILES.joinpath("A_10kB")
AHundredKB = DATAFILES.joinpath("A_100kB")
AOneMB = DATAFILES.joinpath("A_1MB")
ATenMB = DATAFILES.joinpath("A_10MB")
BTenKB = DATAFILES.joinpath("B_10kB")
BHundredKB = DATAFILES.joinpath("B_100kB")
BOneMB = DATAFILES.joinpath("B_1MB")
BTenMB = DATAFILES.joinpath("B_10MB")

def downlink(stub, send_file: Path, receive_file: Path, repeat_send: int, repeat_receive: int, send_size: int):
    times = []
    sizes = []
    for i in range(repeat_send):
        start_time = time.time()
       
        with send_file.open('rb') as f:
            data = f.read()
        r = stub.UploadFile(proto_pb2.FileMessage(chunk_data = data)) 
        times.append(time.time() - start_time)
        sizes.append(int(r.message))
        if i % 100 == 0:
            print(f"Send: {i}")

    for i in range(repeat_receive):
        start_time = time.time()
        r = stub.DownloadFile(proto_pb2.StringResponse(message = receive_file.name)) 
        times.append(time.time() - start_time)
        sizes.append(len(r.chunk_data))
        if i % 100 == 0:
            print(f"Receive: {i}")
       

    print(send_file.name, "Throughput Mean in kilobits:", (send_size * 0.008 / mean(times)))
    print(send_file.name, "Throughput STD in kilobits:", (send_size * 0.008 / stdev(times)))
    print(send_file.name, "Packet Size Mean in kilobits:", mean(sizes) * 0.008)

    
    
def run():
    with grpc.insecure_channel( '192.168.1.19:50051', options=[ ('grpc.max_send_message_length', -1), ('grpc.max_receive_message_length', -1)],) as channel:
        stub = proto_pb2_grpc.GreeterStub(channel)
        # Downlink 10kB file
        print("Downlinking 10KB file")
        downlink(stub, ATenKB, BTenKB, 1000, 10000, 10000)

        # Downlink 100kB file
        print("Downlinking 100KB file")
        downlink(stub, AHundredKB, BHundredKB, 100, 10, 100000)

        # Downlink 1MB file
        print("Downlinking 1MB file")
        downlink(stub, AOneMB, BOneMB, 10, 10, 1000000)

        # Downlink 10MB file
        print("Downlinking 10MB file")
        downlink(stub, ATenMB, BTenMB, 1, 1, 10000000)



if __name__ == '__main__':
    run()

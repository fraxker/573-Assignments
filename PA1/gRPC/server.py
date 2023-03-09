# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 10:36:27 2023

@author: Sydney and Andrew
"""
from concurrent import futures
import logging
import grpc
from protos import proto_pb2, proto_pb2_grpc
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


class Greeter(proto_pb2_grpc.GreeterServicer):

    def UploadFile(self, request, context):
        data = bytearray()
        data.extend(request.chunk_data)
        
        return proto_pb2.StringResponse(message= str(len(data)))

    def DownloadFile(self, request, context):
        name = request.message
        if name == BTenKB.name:
            file = BTenKB
        if name == BHundredKB.name:
            file = BHundredKB
        if name == BOneMB.name:
            file = BOneMB
        if name == BTenMB.name:
            file = BTenMB
        
        with file.open('rb') as f:
            data = f.read()
        return proto_pb2.FileMessage(chunk_data = data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options = [ ('grpc.max_send_message_length', -1), ('grpc.max_receive_message_length', -1) ])
    #server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    proto_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()


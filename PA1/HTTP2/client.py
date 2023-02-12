from statistics import mean, stdev
import pycurl
from pathlib import Path
import time
import json
from io import BytesIO
from urllib.parse import urlencode

DATAFILES = Path("../Datafiles")

ATenKB = DATAFILES.joinpath("A_10kB")
AHundredKB = DATAFILES.joinpath("A_100kB")
AOneMB = DATAFILES.joinpath("A_1MB")
ATenMB = DATAFILES.joinpath("A_10MB")
BOneKB = DATAFILES.joinpath("B_1kB")
BTenKB = DATAFILES.joinpath("B_10kB")
BOneMB = DATAFILES.joinpath("B_1MB")
BTenMB = DATAFILES.joinpath("B_10MB")

def downlink(send_file: Path, receive_file: Path, repeat_send: int, repeat_receive: int, send_size: int, receive_size: int):
    send_times = []
    send_sizes = []
    c = pycurl.Curl()
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_0)
    c.setopt(pycurl.URL, "https://192.168.1.44:8000/send")
    for _ in range(repeat_send):
        with send_file.open("rb") as f:
            buffer = BytesIO()
            c.setopt(pycurl.WRITEDATA, buffer)
            c.setopt(pycurl.READDATA, f)
            start_time = time.time()
            c.perform()
            send_times.append(time.time() - start_time)
            d = json.loads(buffer.getvalue())
            send_sizes.append(d["size"])

    receive_times = []
    receive_sizes = []
    c.setopt(pycurl.URL, 'http://192.168.1.44:8000/receive')
    c.setopt(pycurl.POSTFIELDS, urlencode())
    c.setopt(pycurl.CUSTOMREQUEST, "GET")
    c.setopt(pycurl.HTTPHEADER, ['Accept: application/json', 'Content-Type: application/json'])
    for _ in range(repeat_receive):
        buffer = BytesIO()
        headers = BytesIO()
        c.setopt(pycurl.WRITEDATA, buffer)
        c.setopt(pycurl.WRITEHEADER, headers)
        start_time = time.time()
        c.perform()
        receive_times.append(time.time() - start_time)
        receive_sizes.append(buffer.getbuffer().nbytes + headers.getbuffer().nbytes)

    print(send_file.name, "Throughput Mean in kilobits:", ((send_size * 0.008 / mean(send_times)) + (receive_size * 0.008 / mean(receive_times))) / 2)
    print(send_file.name, "Throughput STD in kilobits:", ((send_size * 0.008 / stdev(send_times)) + (receive_size * 0.008 / stdev(receive_times))) / 2)
    print(send_file.name, "Packet Size Mean in kilobits:", ((mean(send_sizes) / send_size) + (mean(receive_sizes) / receive_size)) / 2 * 0.008)

if __name__ == "__main__":
    # Downlink 10kB file
    print("Downlinking 10KB file")
    downlink(ATenKB, BOneKB, 1000, 10000, 10000, 1000)

    # Downlink 100kB file
    print("Downlinking 100KB file")
    downlink(AHundredKB, BTenKB, 100, 10, 100000, 1000)

    # Downlink 1MB file
    print("Downlinking 1MB file")
    downlink(AOneMB, BOneMB, 10, 10, 1000000, 1000000)

    # Downlink 10MB file
    print("Downlinking 10MB file")
    downlink(ATenMB, BTenMB, 1, 1, 10000000, 10000000)

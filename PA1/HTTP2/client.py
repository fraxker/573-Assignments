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
BTenKB = DATAFILES.joinpath("B_10kB")
BHundredKB = DATAFILES.joinpath("B_100kB")
BOneMB = DATAFILES.joinpath("B_1MB")
BTenMB = DATAFILES.joinpath("B_10MB")

def downlink(send_file: Path, receive_file: Path, repeat_send: int, repeat_receive: int, send_size: int, receive_size: int):
    times = []
    sizes = []
    c = pycurl.Curl()
    c.setopt(pycurl.HTTP_VERSION, pycurl.CURL_HTTP_VERSION_2_0)
    c.setopt(pycurl.URL, "http://192.168.1.19:5000/send")
    c.setopt(pycurl.CUSTOMREQUEST, "PUT")
    for _ in range(repeat_send):
        with send_file.open("rb") as f:
            buffer = BytesIO()
            c.setopt(pycurl.WRITEDATA, buffer)
            c.setopt(pycurl.READDATA, f)
            start_time = time.time()
            c.perform()
            times.append(time.time() - start_time)
            d = json.loads(buffer.getvalue())
            sizes.append(d["size"])

    c.setopt(pycurl.URL, 'http://192.168.1.19:5000/receive')
    c.setopt(pycurl.POSTFIELDS, urlencode({"name": receive_file.name}))
    for _ in range(repeat_receive):
        buffer = BytesIO()
        headers = BytesIO()
        c.setopt(pycurl.WRITEDATA, buffer)
        c.setopt(pycurl.WRITEHEADER, headers)
        start_time = time.time()
        c.perform()
        times.append(time.time() - start_time)
        sizes.append(buffer.getbuffer().nbytes + headers.getbuffer().nbytes)

    c.close()
    print(send_file.name, "Throughput Mean in kilobits:", (send_size * 0.008 / mean(times)))
    print(send_file.name, "Throughput STD in kilobits:", (send_size * 0.008 / stdev(times)))
    print(send_file.name, "Packet Size Mean in kilobits:", mean(sizes) * 0.008)

if __name__ == "__main__":
    # Downlink 10kB file
    print("Downlinking 10KB file")
    downlink(ATenKB, BTenKB, 1000, 10000, 10000, 1000)

    # Downlink 100kB file
    print("Downlinking 100KB file")
    downlink(AHundredKB, BHundredKB, 100, 10, 100000, 1000)

    # Downlink 1MB file
    print("Downlinking 1MB file")
    downlink(AOneMB, BOneMB, 10, 10, 1000000, 1000000)

    # Downlink 10MB file
    print("Downlinking 10MB file")
    downlink(ATenMB, BTenMB, 1, 1, 10000000, 10000000)

from statistics import mean, stdev
import requests
from pathlib import Path
import time
import sys

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
    for _ in range(repeat_send):
        start_time = time.time()
        r = requests.get("http://localhost:5000/send", files={"upload_file": send_file.open("rb")})
        send_sizes.append(r.json()["size"])
        send_times.append(time.time() - start_time)

    receive_times = []
    receive_sizes = []
    for _ in range(repeat_receive):
        start_time = time.time()
        r = requests.get("http://localhost:5000/receive", json={"name": receive_file.name})
        receive_sizes.append(len(r.content) + sys.getsizeof(r.headers))
        receive_times.append(time.time() - start_time)

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

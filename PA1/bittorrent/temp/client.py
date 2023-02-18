from torrentp import TorrentDownloader
from statistics import mean, stdev
from pathlib import Path
import time

DATAFILES = Path(".")

ATenKB = DATAFILES.joinpath("A_10kB")
AHundredKB = DATAFILES.joinpath("A_100kB")
AOneMB = DATAFILES.joinpath("A_1MB")
ATenMB = DATAFILES.joinpath("A_10MB")

def downlink(send_file: Path, repeat_send: int, send_size: int):
    torrent = TorrentDownloader(f"../{send_file.name}.torrent", ".")
    times = []
    sizes = []
    for _ in range(repeat_send):
        start_time = time.time()
        torrent.start_download()
        times.append(time.time() - start_time)
        sizes.append(send_file.stat().st_size)
        ATenKB.unlink()
        time.sleep(.1)

    print(send_file.name, "Throughput Mean in kilobits:", (send_size * 0.008 / mean(times)))
    print(send_file.name, "Throughput STD in kilobits:", (send_size * 0.008 / stdev(times)))
    print(send_file.name, "Packet Size Mean in kilobits:", mean(sizes) * 0.008)

if __name__ == "__main__":
    # Downlink 10kB file
    print("Downlinking 10KB file")
    downlink(ATenKB, 333, 10000)

    # Downlink 100kB file
    print("Downlinking 100KB file")
    downlink(AHundredKB, 33, 100000)

    # Downlink 1MB file
    print("Downlinking 1MB file")
    downlink(AOneMB, 3, 1000000)

    # Downlink 10MB file
    print("Downlinking 10MB file")
    downlink(ATenMB, 1, 10000000)

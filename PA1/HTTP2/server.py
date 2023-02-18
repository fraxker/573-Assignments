from quart import Quart, request, send_from_directory
import sys
from pathlib import Path
app = Quart(__name__)

DATAFILES = Path("../Datafiles")

ATenKB = DATAFILES.joinpath("A_10kB")
AHundredKB = DATAFILES.joinpath("A_100kB")
AOneMB = DATAFILES.joinpath("A_1MB")
ATenMB = DATAFILES.joinpath("A_10MB")
BTenKB = DATAFILES.joinpath("B_10kB")
BHundredKB = DATAFILES.joinpath("B_100kB")
BOneMB = DATAFILES.joinpath("B_1MB")
BTenMB = DATAFILES.joinpath("B_10MB")

@app.route('/receive', methods=['GET'])
async def receive():
    json_data = await request.get_json()
    name = json_data["name"]
    if name == BTenKB.name:
        file = BTenKB
    if name == BHundredKB.name:
        file = BHundredKB
    if name == BOneMB.name:
        file = BOneMB
    if name == BTenMB.name:
        file = BTenMB

    return send_from_directory(str(DATAFILES), file.name, as_attachment=True)

@app.route('/send', methods=['PUT'])
async def send():
    size = request.content_length + sys.getsizeof(request.headers)
    return size

if __name__ == "__main__":
    app.run(host="192.168.1.44", port=8000, certfile="./cert.pem")
from flask import Flask, request, send_from_directory
import sys
from pathlib import Path
app = Flask(__name__)

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
def receive():
    json_data = request.json
    name = json_data["name"]
    if name == BTenKB.name:
        file = BTenKB
    if name == BHundredKB.name:
        file = BHundredKB
    if name == BOneMB.name:
        file = BOneMB
    if name == BTenMB.name:
        file = BTenMB

    return send_from_directory(str(DATAFILES.resolve()), file.name)

@app.route('/send', methods=['PUT'])
def send():
    request.files["upload_file"]
    size = request.content_length + sys.getsizeof(request.headers)
    return {"size": size}
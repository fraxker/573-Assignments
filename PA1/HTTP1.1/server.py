from flask import Flask, request, send_from_directory
import sys
from pathlib import Path
app = Flask(__name__)

DATAFILES = Path("../Datafiles")

ATenKB = DATAFILES.joinpath("A_10kB")
AHundredKB = DATAFILES.joinpath("A_100kB")
AOneMB = DATAFILES.joinpath("A_1MB")
ATenMB = DATAFILES.joinpath("A_10MB")
BOneKB = DATAFILES.joinpath("B_1kB")
BTenKB = DATAFILES.joinpath("B_10kB")
BOneMB = DATAFILES.joinpath("B_1MB")
BTenMB = DATAFILES.joinpath("B_10MB")

@app.route('/receive', methods=['GET'])
def receive():
    json_data = request.json
    name = json_data["name"]
    match name:
        case BOneKB.name:
            file = BOneKB
        case BTenKB.name:
            file = BTenKB
        case BOneMB.name:
            file = BOneMB
        case BTenMB.name:
            file = BTenMB
    return send_from_directory(str(DATAFILES), file.name, as_attachment=True)

@app.route('/send', methods=['GET'])
def send():
    size = request.content_length + sys.getsizeof(request.headers)
    return {"size": size}

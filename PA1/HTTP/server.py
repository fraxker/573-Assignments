from flask import Flask, request, send_from_directory
from pathlib import Path
app = Flask(__name__)

DATAFILES = Path("/DataFiles")

HundredB = DATAFILES.joinpath("100B")
TenKB = DATAFILES.joinpath("10KB")
OneMB = DATAFILES.joinpath("1MB")
TenMB = DATAFILES.joinpath("10MB")

@app.route('/', methods=['GET'])
def hello_world():
    json_data = request.json
    name = json_data["name"]
    match name:
        case HundredB.name:
            file = HundredB
        case TenKB.name:
            file = TenKB
        case OneMB.name:
            file = OneMB
        case TenMB.name:
            file = TenMB
    return send_from_directory(str(DATAFILES), file.name, as_attachment=True)
    with file.open("rb") as f:
        return send_file(f, download_name=file.name)
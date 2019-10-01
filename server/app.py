import base64
import os

from flask import Flask, request

from roboviz import MapVisualizer

MAP_SIZE_PIXELS = int(os.environ.get("SLAM_MAP_SIZE_PIXELS", "500"))
MAP_SIZE_METERS = int(os.environ.get("SLAM_MAP_SIZE_METERS", "10"))

app = Flask(__name__)

# Set up a SLAM display
viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, "SLAM")


@app.route("/submit_data", methods=["POST"])
def submit_data():
    print(request.form["x"], request.form["y"], request.form["theta"])
    if not viz.display(
        float(request.form["x"]),
        float(request.form["y"]),
        float(request.form["theta"]),
        bytearray(base64.b64decode(request.form["mapbytes"])),
    ):
        exit(0)

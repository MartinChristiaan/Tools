from pathlib import Path
import pickle
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2

from mm_io_manager import IOData

app = Flask(__name__)
CORS(app)


class VideosetAPI:
    def __init__(self):
        self.manager = IOData(
            "aot",
            "part1/video0360",
            selected_sources=[],
            groupbys=[],
            groupbys_options=[],
        )
        self.manager.update_mm()

    def get_frame(self, timestamp):
        if timestamp == 0:
            timestamp = self.manager.timestamps[0]
        frame = self.manager.get_frame(timestamp, 0)
        _, encoded_frame = cv2.imencode(".jpeg", frame)
        encoded_frame = encoded_frame.tobytes()
        return Response(encoded_frame, content_type="image/jpeg")

    def get_detections(self, timestamp, source):
        if timestamp == 0:
            timestamp = self.manager.timestamps[0]

        data = self.manager.get_detections(timestamp)
        data = data[data.source == source]
        # TODO check if works with len(0)
        return data.to_json(orient="records")


videoset_api = VideosetAPI()

from threading import Lock

lock = Lock()


@app.route("/frame/<timestamp>", methods=["GET"])
def get_frame(timestamp):
    with lock:
        return videoset_api.get_frame(float(timestamp))


@app.route("/detections/<source_and_timstamps>", methods=["GET"])
def get_detections(source_and_timstamps):
    source, timestamp = source_and_timstamps.split("SPLIT")
    source = source.replace("DASH", "/")
    return videoset_api.get_detections(float(timestamp), source)


@app.route("/plotdata/<source>", methods=["GET"])
def get_xt_plot(source):
    source = source.replace("DASH", "/")
    return jsonify(videoset_api.manager.get_xt_plot(source))


@app.route("/videoset", methods=["GET"])
def get_videoset():
    return jsonify(videoset_api.manager.to_dict())


@app.route("/videoset", methods=["POST"])
def set_videoset():
    data = request.json  # JSON data sent in the request
    videoset_api.manager.set_videoset_data(data)
    return jsonify(videoset_api.manager.to_dict())


@app.route("/save/<timestamp>", methods=["GET"])
def save(timestamp):
    saves_folder = Path("saves/")
    saves_folder.mkdir(exist_ok=True)
    from datetime import datetime

    manager = videoset_api.manager
    manager.timestamp = float(timestamp)
    datestr = datetime.now().strftime("%Y%m%dT%H%M%S")
    save_path = saves_folder / f"{datestr}_{manager.videoset}_{manager.camera_flat}.pkl"
    with open(save_path, "wb") as f:
        pickle.dump(manager.to_dict(), f)
    return '{"status":"succes"}'


if __name__ == "__main__":
    app.run(debug=True)

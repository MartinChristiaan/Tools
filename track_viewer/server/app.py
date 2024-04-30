import json
from datetime import datetime
import os
from pathlib import Path
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2


app = Flask(__name__)
CORS(app)


from pathlib import Path

from videosets_ii.videosets_ii import VideosetsII

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)


def get_modified_date(path):
    return os.path.getmtime(path)


def find_result_csv_in_mm_path(media_manager):
    paths = list(media_manager.result_dirpath.rglob("*.csv"))
    sorted_paths = sorted(paths, key=get_modified_date)[::-1]
    path_options = [f"{x.parent.stem}/{x.name}" for x in sorted_paths]
    return path_options


class VideosetAPI:
    def __init__(self) -> None:
        self.current_videoset = None
        self.media_manager = None

        self.videoset_lut = {}

        for videoset_name, videoset in videosets.videosets_by_name.items():
            self.videoset_lut[videoset_name] = [camera for camera in videoset.cameras]

    def get_videosets(self):
        videoset_data = []
        for videoset_name, videoset in videosets.videosets_by_name.items():
            videoset_data += [dict(videoset=videoset_name, cameras=videoset.cameras)]
        return videoset_data

    def get_frame(self, videoset, camera, timestamp):
        self._set_manager(videoset, camera)

        if timestamp == 0:
            timestamp = self.media_manager.timestamps[0]

        frame = self.media_manager.get_frame(timestamp)
        _, encoded_frame = cv2.imencode(".jpeg", frame)
        encoded_frame = encoded_frame.tobytes()
        return Response(encoded_frame, content_type="image/jpeg")

    def _set_manager(self, videoset, camera):
        if videoset not in self.videoset_lut:
            return False
        if camera not in self.videoset_lut[videoset]:
            return False

        if self.current_videoset != videoset + camera:
            self.current_videoset = videoset + camera
            self.media_manager = videosets[videoset].get_mediamanager(camera)
            return True

    def get_detections_options(self, videoset, camera):
        if self._set_manager(videoset, camera):
            return [str(x) for x in find_result_csv_in_mm_path(self.media_manager)]
        else:
            return []

    def get_detection_data(self, videoset, camera, detections_path):
        self._set_manager(videoset, camera)
        data = self.media_manager.load(detections_path)
        return data.to_json()

    def save_snapshot(self, state_dict):
        snapshot_dir = Path("/data/track_viewer_shapshots/")
        snapshot_dir.mkdir(exist_ok=True, parents=True)
        videoset = state_dict["videoset"]
        camera = state_dict["camera"]
        datestr = datetime.now().strftime("%Y%m%dT%H%M%S")
        save_path = snapshot_dir / f"{datestr}_{videoset}_{camera.replace('/','_')}.pkl"
        with open(save_path, "w") as f:
            json.dump(state_dict, f)


videoset_api = VideosetAPI()

from threading import Lock

lock = Lock()


# Define endpoints
@app.route("/videosets", methods=["GET"])
def get_videosets():
    videosets = videoset_api.get_videosets()
    return jsonify(videosets)


@app.route("/frame", methods=["GET"])
def get_frame():
    videoset = request.args.get("videoset")
    camera = request.args.get("camera")
    timestamp = float(request.args.get("timestamp"))
    with lock:
        frame = videoset_api.get_frame(videoset, camera, timestamp)
    return Response(frame, content_type="image/jpeg")


@app.route("/detections_options", methods=["GET"])
def get_detections_options():
    videoset = request.args.get("videoset")
    camera = request.args.get("camera")

    options = videoset_api.get_detections_options(videoset, camera)
    return jsonify(options)


@app.route("/detection_data", methods=["GET"])
def get_detection_data():
    videoset = request.args.get("videoset")
    camera = request.args.get("camera")
    detections_path = request.args.get("detections_path")

    data = videoset_api.get_detection_data(videoset, camera, detections_path)
    return data


@app.route("/save_snapshot", methods=["POST"])
def save_snapshot():
    state_dict = request.json

    videoset_api.save_snapshot(state_dict)

    return "Snapshot saved successfully"


if __name__ == "__main__":
    app.run(debug=True)

import os
from pathlib import Path
import pickle
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2

from mm_io_manager import IOData


app = Flask(__name__)
CORS(app)


from pathlib import Path
from loguru import logger

from videosets_ii.videosets_ii import VideosetsII
from trackertoolbox.detections import Detections
from trackertoolbox.tracks import Tracks, TrackUpdates
import pandas as pd

basedirpath = Path(r"/diskstation")
videosets = VideosetsII(basedirpath=basedirpath)  # basedirpath)


def get_modified_date(path):
    return os.path.getmtime(path)


def find_result_csv_in_mm_path(self, mm):
    paths = list(mm.result_dirpath.rglob("*.csv"))
    sorted_paths = sorted(paths, key=get_modified_date)[::-1]
    path_options = [f"{x.parent.stem}/{x.name}" for x in sorted_paths]
    return path_options


class VideosetAPI:
    def __init__(self) -> None:
        self.current_videoset = None
        self.media_manager = None

    def get_videosets(self):
        videoset_data = []
        for videoset in videosets:
            videoset_data += [dict(videoset=videoset.name, cameras=videoset.cameras)]
        return videoset_data

    def get_frame(self, videoset, camera, timestamp):
        self.set_manager(videoset, camera)

        if timestamp == 0:
            timestamp = self.media_manager.timestamps[0]

        frame = self.media_manager.get_frame(timestamp)
        _, encoded_frame = cv2.imencode(".jpeg", frame)
        encoded_frame = encoded_frame.tobytes()
        return Response(encoded_frame, content_type="image/jpeg")

    def set_manager(self, videoset, camera):
        if self.current_videoset != videoset + camera:
            self.current_videoset = videoset + camera
            self.media_manager = videosets[videoset].get_mediamanager(camera)

    def get_detections_options(self, videoset, camera, timestamp):
        self.set_manager(videoset, camera)
        return find_result_csv_in_mm_path(self.media_manager)

    def get_detections(self, timestamp, source):
        if timestamp == 0:
            timestamp = self.media_manager.timestamps[0]
        data = self.media_manager.get_detections(timestamp)
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
    return jsonify(videoset_api.media_manager.get_xt_plot(source))


@app.route("/videoset", methods=["GET"])
def get_videoset():
    return jsonify(videoset_api.media_manager.to_dict())


@app.route("/videoset", methods=["POST"])
def set_videoset():
    data = request.json  # JSON data sent in the request
    videoset_api.media_manager.set_videoset_data(data)
    return jsonify(videoset_api.media_manager.to_dict())


@app.route("/save/<timestamp_and_comment>", methods=["GET"])
def save(timestamp_and_comment):
    saves_folder = Path("/data/track-viewer-saves/")
    saves_folder.mkdir(exist_ok=True)
    from datetime import datetime

    manager = videoset_api.media_manager
    timestamp, comment = timestamp_and_comment.split("___")
    manager.timestamp = float(timestamp)
    manager.comment = comment
    datestr = datetime.now().strftime("%Y%m%dT%H%M%S")
    save_path = saves_folder / f"{datestr}_{manager.videoset}_{manager.camera_flat}.pkl"
    with open(save_path, "wb") as f:
        pickle.dump(manager.to_dict(), f)
    return '{"status":"succes"}'


if __name__ == "__main__":
    app.run(debug=True)

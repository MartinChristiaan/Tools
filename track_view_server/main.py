from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import dlutils_ii as du
from videosets_ii.videosets_ii import VideosetsII
import cv2

from mm_io_manager import IOData

app = Flask(__name__)
CORS(app)

# pf = du.Pathfinder()


class VideosetAPI:
    def __init__(self):
        self.manager = IOData()

    def get_frame(self, timestamp):
        if timestamp == 0:
            timestamp = self.manager.timestamps[0]
        frame = self.manager.get_frame(timestamp)
        _, encoded_frame = cv2.imencode(".jpeg", frame)
        encoded_frame = encoded_frame.tobytes()
        return Response(encoded_frame, content_type="image/jpeg")

    def get_detections(self, timestamp):
        if timestamp == 0:
            timestamp = self.manager.timestamps[0]
        return self.manager.get_detections(timestamp).to_json(orient="records")

    def get_xt_plot(self):
        # TODO add options for how it should be vizualied
        return dict(
            x=list(self.manager.detections.timestamp),
            y=list(self.manager.detections.bbox_x),
            type="scatter",
            mode="markers",
        )


videoset_api = VideosetAPI()


@app.route("/frame/<timestamp>", methods=["GET"])
def get_frame(timestamp):
    print(timestamp)
    return videoset_api.get_frame(float(timestamp))


@app.route("/detections/<timestamp>", methods=["GET"])
def get_detections(timestamp):
    return videoset_api.get_detections(float(timestamp))


@app.route("/plotdata", methods=["GET"])
def get_xt_plot():
    return videoset_api.get_xt_plot()


@app.route("/videoset", methods=["GET"])
def get_videoset():
    return jsonify(videoset_api.manager.to_dict())


@app.route("/videoset", methods=["POST"])
def set_videoset():
    data = request.json  # JSON data sent in the request
    videoset_api.manager.set_videoset_data(data)
    return jsonify(videoset_api.manager.to_dict())


@app.route("/handle_key/<key>", methods=["GET"])
def next_frame(key):
    if key in "ad":
        delta = 1
        if key == "a":
            delta = -1
        videoset_api.frame_index += delta

    # if key in 'xz':
    # 	videoset_api.update_frame_variation(-1 if key == 'z' else 1)

    return "{}"  # videoset_api.get_annotations()


if __name__ == "__main__":
    app.run(debug=True)

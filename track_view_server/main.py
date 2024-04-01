from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2

from mm_io_manager import IOData

app = Flask(__name__)
CORS(app)


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

    def get_detections(self, timestamp, source):
        if timestamp == 0:
            timestamp = self.manager.timestamps[0]

        data = self.manager.get_detections(timestamp)
        data = data[data.source == source]
        # TODO check if works with len(0)
        return data.to_json(orient="records")

    def get_xt_plot(self, source):
        # TODO add options for how it should be vizualied
        # TODO check if works with len(0)
        data = self.manager.detections
        data = data[data.source == source]

        return dict(
            x=list(source.timestamp),
            y=list(source.bbox_x),
            type="scatter",
            mode="markers",
        )


videoset_api = VideosetAPI()


@app.route("/frame/<timestamp>", methods=["GET"])
def get_frame(timestamp):
    print(timestamp)
    return videoset_api.get_frame(float(timestamp))


@app.route("/detections/<source_and_timstamps>", methods=["GET"])
def get_detections(source_and_timstamps):
    source, timestamp = source_and_timstamps.split("AAA")
    return videoset_api.get_detections(float(timestamp), source)


@app.route("/plotdata/<source>", methods=["GET"])
def get_xt_plot(source):
    data = videoset_api.get_xt_plot(source)


@app.route("/videoset", methods=["GET"])
def get_videoset():
    return jsonify(videoset_api.manager.to_dict())


@app.route("/videoset", methods=["POST"])
def set_videoset():
    data = request.json  # JSON data sent in the request
    videoset_api.manager.set_videoset_data(data)
    return jsonify(videoset_api.manager.to_dict())


if __name__ == "__main__":
    app.run(debug=True)

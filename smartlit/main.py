from typing import List
from Container import Container
from MediaManagerSelection import MediaManagerSelection
from loguru import logger


class API:
    def __init__(self, containers: List[Container]) -> None:
        self.containers = containers
        self.container_lut = {x.name: x for x in self.containers}

    def get_ui_data(self):
        data = {}
        for c in self.containers:
            data[c.name] = {x.name: x.get_ui_data() for x in c.get_observables()}
        return data

    def set_ui_data(self, data):
        for k, container in self.container_lut.items():
            cdata = data[k]
            for observable in container.get_observables():
                observable.set_value(cdata[observable.name]["value"])
        return self.get_ui_data()


from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import List


def create_app(initial_containers):

    app = Flask(__name__)
    CORS(app)
    # Create an instance of the Server class with some initial containers
    server = API(initial_containers)

    # Endpoint to get UI data
    @app.route("/get_ui_data", methods=["GET"])
    def get_ui_data():
        data = server.get_ui_data()
        return jsonify(data)

    # Endpoint to set UI data
    @app.route("/set_ui_data", methods=["POST"])
    def set_ui_data():
        data = request.json
        updated_data = server.set_ui_data(data)
        return jsonify(updated_data)

    return app


if __name__ == "__main__":

    media_manager_selection = MediaManagerSelection()
    initial_containers = [
        media_manager_selection
    ]  # Define your initial containers here
    app = create_app
    app.run(debug=True)

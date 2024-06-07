from typing import List
from Container import Container
from MediaManagerSelection import MediaManagerSelection


class API:
    def __init__(self, containers: List[Container]) -> None:
        self.containers = containers
        self.container_lut = {x.name: x for x in self.containers}

    def get_container_data(self):
        data = []
        for c in self.containers:
            data.append({c.name: c.ctype})

    def get_ui_data(self, name):
        c = self.container_lut[name]
        # data = {x.name: x.get_ui_data() for x in c.get_observables()}
        return c.get_ui_data()

    def set_ui_data(self, data, name):
        container = self.container_lut[name]
        should_run = []
        for observable in container.get_observables():
            if observable.set_value_delayed_run(data[observable.name]["value"]):
                should_run.append(observable)
        for obs in should_run:
            print(f"running {obs.name}")
            obs.run()

        return self.get_ui_data()


from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import List


def create_app(initial_containers: List[Container]):

    app = Flask(__name__)
    CORS(app)
    # Create an instance of the Server class with some initial containers
    server = API(initial_containers)

    @app.route("/get_containers", methods=["GET"])
    def get_ui_data():
        data = server.get_ui_data()
        return jsonify(data)

    @app.route("/get_container_data/<name>", methods=["GET"])
    def get_ui_data(name):
        data = server.get_ui_data(name)
        return jsonify(data)

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
        for c in initial_containers:
            c.save_state()
        return jsonify(updated_data)

    return app


if __name__ == "__main__":

    media_manager_selection = MediaManagerSelection()
    initial_containers = [
        media_manager_selection
    ]  # Define your initial containers here
    app = create_app(initial_containers)
    app.run(debug=True)

from typing import Dict, List

import numpy as np
import pandas as pd
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

items_per_request = 30


class ImgWallInterface:
    def get_random_items(self) -> List[Dict]:
        return []

    def get_image_gallery(self, index: int) -> List[Dict]:
        return []


class MyApp(Flask):
    def __init__(self, interface: ImgWallInterface, **kwargs):
        self.imgwall_interface = interface
        self.update_items()
        super().__init__("main", **kwargs)
        CORS(self)

    def get_image(self, index):
        imdata = self.imgwall_interface.get_image(index)
        return Response(imdata, content_type="image/jpeg")

    def get_items(self):
        print(self.items)
        return jsonify(self.items)

    def update_items(self):
        self.items = self.imgwall_interface.get_random_items()

    def get_gallery(self, index):
        self.items = self.imgwall_interface.get_image_gallery(index)


import numpy as np
import paths as p
from dtypes import Item as DBITem


class CSVInterface(ImgWallInterface):
    def __init__(self) -> None:
        data = p.written_item
        with open(str(data), "r") as f:
            lines = f.read().split("\n")
        self.items = []
        for i, line in enumerate(lines):
            # print(line.split("++"))
            if len(line.split("++")) != 4:
                continue
            item = DBITem(*line.split("++")).__dict__
            # print(item)
            item["index"] = i
            self.items += [item]

    def get_random_items(self) -> List[Dict]:
        indices = np.random.randint(0, len(self.items) - 1, 30)
        items = []
        for idx in indices:
            items += [self.items[idx]]
        return items

    def get_image(self, index):
        with open(p.imdb / self.items[index]["filename"], "rb") as f:
            img = f.read()
        return img

    def get_image_gallery(self, index: int) -> List[Dict]:
        item = self.items[index]
        return [x for x in self.items if x["gallery"] == item["gallery"]]


app = MyApp(CSVInterface())


@app.route("/get_image:<int:index>", methods=["GET"])
def get_image(index):
    return app.get_image(index)


@app.route("/get_items", methods=["GET"])
def get_items():
    return app.get_items()


@app.route("/get_gallery:<int:index>", methods=["GET"])
def get_gallery(index):
    app.get_gallery(index)
    return app.get_items()


@app.route("/update", methods=["GET"])
def update():
    app.update_items()
    return app.get_items()


if __name__ == "__main__":
    app.run(debug=True, port=3333)

import random
from datetime import datetime
from typing import Dict

import pandas as pd
from datatypes import Source, readSources
from flask import Flask, jsonify, request
from flask_cors import CORS

items_per_request = 20

root_source_types = []


def weighed_select_leaf(parent_src, lookup):
    if len(parent_src.child_sources) == 0:
        return parent_src
    children = [lookup[x.id] for x in parent_src.child_sources]
    child_el = random.choices(children, weights=[x.weight for x in children])[0]
    return weighed_select_leaf(child_el)


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sources = readSources()
        self.source_lookup: Dict[int, Source] = {x.id: x for x in self.sources}
        self.root_sources = [
            x
            for x in self.sources
            if len(x.parent_sources) == 0 and len(x.child_sources) > 0
        ]
        CORS(self)

    def update_weight(self):
        data = request.data
        source = [x for x in self.root_sources if x.id == data["id"]][0]
        source.weight = data["weight"]
        return jsonify(self.root_sources)

    def set_favorite(self):
        data = request.data
        source = self.source_lookup[data["id"]]
        favorite = [x for x in self.root_sources if x.name == "favorites"]
        if len(favorite == 0):
            favorite = Source(
                "favorites", "", datetime.now(), -1, 1, [], "favorites", []
            )
            self.root_sources.append(favorite)
            self.sources.append(favorite)
        source.favorite = True
        source.attach_to_parent(favorite)

    def get_root_sources(self):
        return jsonify(self.root_sources)

    def get_random_items(self):
        # print(self.root_sources)
        self.chosen_elements = random.choices(
            self.root_sources,
            weights=[x.weight for x in self.root_sources],
            k=items_per_request,
        )
        return jsonify([weighed_select_leaf(x) for x in self.chosen_elements])

    def get_items_like(self):
        data = request.data
        source = self.source_lookup[data["id"]]
        self.chosen_elements = random.choices(
            source.parent_sources,
            weights=[x.weight for x in source.parent_sources],
            k=items_per_request,
        )
        return jsonify([weighed_select_leaf(x) for x in self.chosen_elements])


app = MyApp(__name__)

#
# items = app.get_random_items()
# with app.app_context:
# print(items)
# print(len(items))
# @app.route('/update_weight', methods=['PUT'])
# def update_weight_route():
# 	return app.update_weight()

# @app.route('/get_items', methods=['GET'])
# def get_items_route():
# 	return app.get_items()

# if __name__ == '__main__':
# 	app.run(debug=True,port=3333)

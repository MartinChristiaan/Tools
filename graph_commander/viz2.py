import os

import matplotlib.pyplot as plt
import networkx as nx

# Define the path to the folder whose subfolders you want to visualize
folder_path = "/mnt/HardDrive/"

# Initialize a NetworkX graph
G = nx.Graph()


class EqualBranchNode:
    def __init__(self, path, parent) -> None:
        self.parent = parent
        self.path = path
        self.added = False
        self.idx = 0
        self.looked_for_kids = False
        self.children = []

    def try_to_add_child(self, graph, max_nodes):
        if len(graph.nodes) >= max_nodes:
            print("node_limit_exceeded")
            return False
        if not self.added:
            self.added = True
            graph.add_node(self.path)
            if self.parent != "":
                graph.add_edge(self.path, self.parent)

            return True
        else:
            if self.idx >= len(self.children):
                self.idx = 0

            if len(self.children) == 0:
                if self.looked_for_kids:
                    return False
                self.children = [
                    EqualBranchNode(f"{self.path}/{x}", self.path)
                    for x in os.listdir(self.path)
                    if os.path.isdir(f"{self.path}/{x}")
                ]
                self.looked_for_kids = True
                if len(self.children) == 0:
                    return False

            if child_was_able_to_add := self.children[self.idx].try_to_add_child(
                graph, max_nodes
            ):
                self.idx += 1
                return True
            else:
                del self.children[self.idx]
                return self.try_to_add_child(graph, max_nodes)


root = EqualBranchNode(folder_path, "")

while root.try_to_add_child(G, 100):
    pass

pos = nx.spring_layout(G)

# Draw the graph
nx.draw(G, pos, with_labels=True, node_size=100, font_size=6)
plt.show()

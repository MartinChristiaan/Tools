import os

import matplotlib.pyplot as plt
import networkx as nx

# Define the path to the folder whose subfolders you want to visualize
folder_path = "/home/martin/git/TeamRoom/"

# Initialize a NetworkX graph
G = nx.Graph()


# Define a recursive function to add subfolders to the graph
def add_subfolders_to_graph(folder_path, graph, max_nodes):
    # If the number of nodes in the graph exceeds the maximum allowed, stop adding nodes
    if len(graph.nodes) >= max_nodes:
        return
    # Add the current folder as a node in the graph
    folder_name = os.path.basename(folder_path)
    graph.add_node(folder_name)
    # Recursively add subfolders to the graph
    num_sub_elements = len(
        [x for x in os.listdir(folder_path) if os.path.isdir(f"{folder_path}/{x}")]
    )
    print(folder_path, num_sub_elements)
    if num_sub_elements > 10:
        return
    for subfolder_name in sorted(os.listdir(folder_path)):
        subfolder_path = os.path.join(folder_path, subfolder_name)
        if os.path.isdir(subfolder_path):
            graph.add_edge(folder_name, subfolder_name)
            add_subfolders_to_graph(subfolder_path, graph, max_nodes)


# Call the function to add subfolders to the graph
add_subfolders_to_graph(folder_path, G, 200)

# Generate a layout for the graph
pos = nx.spring_layout(G)

# Draw the graph
nx.draw(G, pos, with_labels=True, node_size=100, font_size=6)
plt.show()

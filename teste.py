import grakel as gk
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from grakel.utils import graph_from_networkx

adjacency_matrix = np.matrix([
    [0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0],
    [1, 0, 0, 1, 1],
    [0, 1, 1, 0, 0],
    [1, 0, 1, 0, 0]
])

# Create an empty graph
G_nx = nx.Graph()

# Get the number of nodes from the size of the adjacency matrix
num_nodes = adjacency_matrix.shape[0]

# Add nodes to the graph


# Iterate through the adjacency matrix and add edges to the graph
for i in range(num_nodes):
    for j in range(i + 1, num_nodes):  # Avoid duplicate edges and self-loops
        if adjacency_matrix[i, j] == 1:
            G_nx.add_edge(i, j)



G = list(graph_from_networkx([G_nx]))
print(type(G))

graphlet_sampler = gk.GraphletSampling(k = 4,verbose = True)
graphlet_counts = graphlet_sampler.fit_transform(G)

print(graphlet_counts)
count_size_3 = graphlet_counts[0]

print(f"Graphlet Count (Size 3): {count_size_3}")
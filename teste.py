import networkx as nx
import matplotlib.pyplot as plt
from karateclub.node_embedding.neighbourhood.deepwalk import DeepWalk

G = nx.random_tree(40)

nx.draw_spring(G)
plt.show()


deepwalk = DeepWalk(dimensions=2)
deepwalk.fit(G)

embedding = deepwalk.get_embedding()


plt.scatter(embedding[:, 0], embedding[:, 1])

plt.show()

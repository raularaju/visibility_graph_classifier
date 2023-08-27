import networkx as nx
import numpy as np
from scipy.sparse import coo_matrix
from processamento import *
import csv
""" nome_csv = 'features_grafos.csv'
with open(nome_csv, mode='w', newline='') as arquivo_csv:
    csv_writer = csv.writer(arquivo_csv)
    csv_writer.writerow(['num_edges', 'density', 'avg_node_degree', 'connected_components_count', 'graph_diameter']) """
ler_hdf5('./saida.hdf5')


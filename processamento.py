import h5py
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.sparse.csgraph import floyd_warshall
from karateclub.node_embedding.neighbourhood.deepwalk import DeepWalk
import networkx as nx
import csv
# Open the HDF5 file
def ler_hdf5(arquivo):
    nome_csv = 'features_grafos.csv'
    with open(nome_csv, mode='w', newline='') as arquivo_csv:
        csv_writer = csv.writer(arquivo_csv)
        csv_writer.writerow(['num_edges', 'density', 'avg_node_degree', 'connected_components_count', 'graph_diameter'])
        with h5py.File(arquivo, 'r') as f:
            # Iterate through top-level groups
            for top_group_name, top_group in f.items():
                print(f'Top-Level Group: {top_group_name}')

                # Iterate through subgroups within the top-level group
                for subgroup_name, subgroup in top_group.items():
                    print(f'\tSubgroup: {subgroup_name}')
                    if 'grafo' in subgroup:
                        grafo_group = subgroup['grafo']
                        adjacency_matrix_coo = coo_matrix((grafo_group['data'][()], (grafo_group['row'][()], grafo_group['col'][()])))
                        G = nx.from_scipy_sparse_array(adjacency_matrix_coo)
                        deepwalk = DeepWalk(dimensions=2)
                        deepwalk.fit(G)

                        node_embeddings = deepwalk.get_embedding()
                        graph_embedding = np.mean(node_embeddings, axis=0)
                        print(graph_embedding)
                        csv_writer.writerow(graph_embedding)
                        """ #adjacency_matrix_csr = csr_matrix(adjacency_matrix_coo)

                        num_nodes = adjacency_matrix_coo.shape[0]
                        num_edges = adjacency_matrix_coo.nnz
                        graph_density = num_edges / (num_nodes * (num_nodes - 1))
                        average_node_degree = adjacency_matrix_coo.sum() / num_nodes
                        connected_components_count, _ = connected_components(adjacency_matrix_coo, directed=False)
                        #shortest_paths = floyd_warshall(adjacency_matrix_csr)
                        #graph_diameter = np.max(shortest_paths)
                        
                        csv_writer.writerow([num_edges, graph_density, average_node_degree, connected_components_count])
                        
                        print("Number of Nodes:", num_nodes)
                        print("Number of Edges:", num_edges)
                        print("Graph Density:", graph_density)
                        print("Average Node Degree:", average_node_degree)
                        print("Connected Components Count:", connected_components_count)
                        #print("Graph Diameter:", graph_diameter) """

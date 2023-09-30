import h5py
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.sparse.csgraph import floyd_warshall
from karateclub.node_embedding.neighbourhood.deepwalk import DeepWalk
import networkx as nx
import csv
# Open the HDF5 file
def read_hdf5(arquivo):
    nome_csv = 'features_grafos.csv'
    with open(nome_csv, mode='w', newline='') as arquivo_csv:
        csv_writer = csv.writer(arquivo_csv)
        csv_writer.writerow(['num_edges', 'density', 'avg_node_degree', 'avg_degree_centrality', 'avg_eigen_centrality', 'sum_triangle_count', 'avg_clustering_coef'])
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
                      
                        num_nodes = adjacency_matrix_coo.shape[0]
                        num_edges = adjacency_matrix_coo.nnz
                        graph_density = num_edges / (num_nodes * (num_nodes - 1))
                        average_node_degree = adjacency_matrix_coo.sum() / num_nodes
                        
                        degree_centrality_nodes = nx.degree_centrality(G)
                        average_degree_centrality = compute_average_feature(degree_centrality_nodes)
                        print("pau")
                        
                        """ betweenness_centrality_nodes = nx.betweenness_centrality(G)
                        average_betweenness_centrality = compute_average_feature(betweenness_centrality_nodes)
                        print("pau")
                        
                        closeness_centrality_nodes = nx.closeness_centrality(G)
                        average_closeness_centrality = compute_average_feature(closeness_centrality_nodes)
                        print("pau")
                        
                        current_flow_closeness_centrality_nodes = nx.current_flow_closeness_centrality(G)
                        average_current_flow_closeness_centrality = compute_average_feature(current_flow_closeness_centrality_nodes)
                        print("pau")

                        current_flow_betweenness_centrality_nodes = nx.current_flow_betweenness_centrality(G)
                        average_current_flow_betweenness_centrality = nx.current_flow_betweenness_centrality(G)
                        print("pau") 

                        load_centrality_nodes = nx.load_centrality(G)
                        average_load_centrality = compute_average_feature(load_centrality_nodes)
                        print("pau")

                        harmonic_centrality_nodes = nx.harmonic_centrality(G)
                        average_harmonic_centrality = compute_average_feature(harmonic_centrality_nodes)
                        print("pau")

                        percolation_centrality_nodes = nx.percolation_centrality(G)
                        average_percolation_centrality = compute_average_feature(percolation_centrality_nodes)
                        print("pau")"""

                        second_order_centrality_nodes = nx.second_order_centrality(G)
                        average_second_order_centrality = compute_average_feature(second_order_centrality_nodes)
                        print("pau")

                        laplacian_centrality_nodes = nx.laplacian_centrality(G)
                        average_laplacian_centrality = compute_average_feature(laplacian_centrality_nodes)
                        print("pau")

                        triangle_count_nodes = nx.triangles(G)
                        sum_triangle_count = compute_sum_feature(triangle_count_nodes)/3
                        print("pau")

                        average_clustering_coef = nx.average_clustering(G)
                        csv_writer.writerow([num_edges, graph_density, average_node_degree, average_degree_centrality, average_eigen_centrality, sum_triangle_count, average_clustering_coef, average_clustering_coef ])
                        
def compute_average_feature(feature_nodes):
    return sum(feat for nodes, feat in feature_nodes.items()) / len(feature_nodes)
def compute_sum_feature(feature_nodes):
    return(sum(feat for nodes, feat in feature_nodes.items()))               
def compute_features(G):
    pass

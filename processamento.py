import h5py
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.sparse.csgraph import floyd_warshall
from karateclub.node_embedding.neighbourhood.deepwalk import DeepWalk
import grakel as gk
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
                        avg_node_degree = adjacency_matrix_coo.sum() / num_nodes

                        print("degree centrality")
                        degree_centrality_nodes = nx.degree_centrality(G)
                        avg_degree_centrality = compute_avg_feature(degree_centrality_nodes)
                        
                        print("betweenness centrality")
                        betweenness_centrality_nodes = nx.betweenness_centrality(G)
                        avg_betweenness_centrality = compute_avg_feature(betweenness_centrality_nodes)
                        
                        print("closeness centrality")
                        closeness_centrality_nodes = nx.closeness_centrality(G)
                        avg_closeness_centrality = compute_avg_feature(closeness_centrality_nodes)

                        print("current flow closeness") 
                        curr_flow_closeness_centrality_nodes = nx.curr_flow_closeness_centrality(G)
                        avg_curr_flow_closeness_centrality = compute_avg_feature(curr_flow_closeness_centrality_nodes)

                        print("current flow betweenness") 
                        curr_flow_betweenness_centrality_nodes = nx.curr_flow_betweenness_centrality(G)
                        avg_curr_flow_betweenness_centrality = nx.curr_flow_betweenness_centrality(G)



                        print("load centrality")
                        load_centrality_nodes = nx.load_centrality(G)
                        avg_load_centrality = compute_avg_feature(load_centrality_nodes)


                        print("centralidade harmônica")
                        harmonic_centrality_nodes = nx.harmonic_centrality(G)
                        avg_harmonic_centrality = compute_avg_feature(harmonic_centrality_nodes)


                        print("centralidade de percolação")
                        percolation_centrality_nodes = nx.percolation_centrality(G)
                        avg_percolation_centrality = compute_avg_feature(percolation_centrality_nodes)

                        print("second order centrality")
                        second_order_centrality_nodes = nx.second_order_centrality(G)
                        avg_second_order_centrality = compute_avg_feature(second_order_centrality_nodes)

                        print("laplacian centrality")
                        laplacian_centrality_nodes = nx.laplacian_centrality(G)
                        avg_laplacian_centrality = compute_avg_feature(laplacian_centrality_nodes)
                        
                        print("graphlet size 3")
                        count_graphlet_size_3 = gk.GraphletSampling(k=3).fit_transform(G)[0][0]

                        print("graphlet size 4")
                        count_graphlet_size_4 = gk.GraphletSampling(k=3).fit_transform(G)[0][0]

                        print("graphlet size 5")
                        count_graphlet_size_5 = gk.GraphletSampling(k=3).fit_transform(G)[0][0]

                        avg_clustering_coef = nx.avg_clustering(G)
                        csv_writer.writerow([num_edges, density, avg_node_degree, avg_degree_centrality, 
                                             avg_betweenness_centrality, avg_closeness_centrality, avg_curr_flow_closeness_centrality, 
                                             avg_curr_flow_betweennesss_centrality,avg_load_centrality, , avg_harmonic_centrality, 
                                             avg_percolation_centrality, avg_second_order_centrality, avg_lablacian_centrality, 
                                             avg_clustering, count_graphlet_size_3, count_graphlet_size_4,count_graphlet_size_5, avg_clustering_coef])
                        
                        
def compute_avg_feature(feature_nodes):
    return sum(feat for nodes, feat in feature_nodes.items()) / len(feature_nodes)
def compute_sum_feature(feature_nodes):
    return(sum(feat for nodes, feat in feature_nodes.items()))               
def compute_features(G):
    pass

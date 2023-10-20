import h5py
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.sparse.csgraph import floyd_warshall
import grakel as gk
import networkx as nx
from igraph import Graph, plot
import csv
# Open the HDF5 file
def read_hdf5(arquivo):
    nome_csv = 'features_grafos.csv'
    with open(nome_csv, mode='w', newline='') as arquivo_csv:
        csv_writer = csv.writer(arquivo_csv)
        string_motif_3 = [f"motif_3_{i}" for i in range(4)]
        string_motif_4 = [f"motif_4_{i}" for i in range(11)]
        string_motif_5 = [f"motif_5_{i}" for i in range(34)]
        csv_writer.writerow(["exam_id"
                            "num_edges", "density", "avg_node_degree", "avg_degree_centrality", 
                             "avg_closeness_centrality", "avg_curr_flow_closeness_centrality", 
                             "avg_pagerank", "avg_clustering_coef"] +
                             string_motif_3 + string_motif_4 + string_motif_5)
        with h5py.File(arquivo, 'r') as f:
            # Iterate through top-level groups
            for exam_id, top_group in f.items():
                print(f'Top-Level Group: {exam_id}')
                
                # Iterate through subgroups within the top-level group
                for subgroup_name, subgroup in top_group.items():
                    print(f'\tSubgroup: {subgroup_name}')
                    if 'grafo' in subgroup:
                        grafo_group = subgroup['grafo']
                        adjacency_matrix_coo = coo_matrix((grafo_group['data'][()], (grafo_group['row'][()], grafo_group['col'][()])))
                        G_nx = nx.from_scipy_sparse_array(adjacency_matrix_coo)
                        G_igraph = Graph.TupleList(zip(grafo_group['row'][()], grafo_group['col'][()]), directed=False)

                        num_nodes = adjacency_matrix_coo.shape[0]
                        num_edges = adjacency_matrix_coo.nnz
                        density = num_edges / (num_nodes * (num_nodes - 1))
                        avg_node_degree = adjacency_matrix_coo.sum() / num_nodes

                        print("degree centrality")
                        degree_centrality_nodes = nx.degree_centrality(G_nx)
                        avg_degree_centrality = compute_avg_feature(degree_centrality_nodes)
                        
                        """ print("betweenness centrality")
                        betweenness_centrality_nodes = nx.betweenness_centrality(G_nx)
                        avg_betweenness_centrality = compute_avg_feature(betweenness_centrality_nodes) """
                        
                        print("closeness centrality")
                        closeness_centrality_nodes = nx.closeness_centrality(G_nx)
                        avg_closeness_centrality = compute_avg_feature(closeness_centrality_nodes)

                        print("current flow closeness") 
                        curr_flow_closeness_centrality_nodes = nx.current_flow_closeness_centrality(G_nx)
                        avg_curr_flow_closeness_centrality = compute_avg_feature(curr_flow_closeness_centrality_nodes)

                        """ print("current flow betweenness") 
                        curr_flow_betweenness_centrality_nodes = nx.current_flow_betweenness_centrality(G_nx)
                        avg_curr_flow_betweenness_centrality = nx.curr_flow_betweenness_centrality(G_nx)
 """


                        """ print("load centrality")
                        load_centrality_nodes = nx.load_centrality(G_nx)
                        avg_load_centrality = compute_avg_feature(load_centrality_nodes) """


                        """ print("centralidade harmônica")
                        harmonic_centrality_nodes = nx.harmonic_centrality(G_nx)
                        avg_harmonic_centrality = compute_avg_feature(harmonic_centrality_nodes) """

                        

                        """ print("centralidade de percolação")
                        percolation_centrality_nodes = nx.percolation_centrality(G_nx)
                        avg_percolation_centrality = compute_avg_feature(percolation_centrality_nodes) """

                        """ print("second order centrality")
                        second_order_centrality_nodes = nx.second_order_centrality(G_nx)
                        avg_second_order_centrality = compute_avg_feature(second_order_centrality_nodes) """

                        print("pagerank")
                        pagerank_nodes = nx.pagerank(G_nx)
                        avg_pagerank = compute_avg_feature(pagerank_nodes)
                       
                        print("clutering médio")
                        avg_clustering_coef = nx.average_clustering(G_nx)
                        
                        G = list(gk.graph_from_networkx([G_nx]))
                        print("motifs size 3")
                        #count_motif_size_3 =  G_igraph.motifs_randesu(3, [0.5, 0.5, 0.5])
                        count_motif_size_3 =  G_igraph.motifs_randesu(3)
                        change_nan_to_zero(count_motif_size_3)

                        print("motifs size 4")
                        count_motif_size_4 = G_igraph.motifs_randesu(4, [0.4, 0.4, 0.4, 0.4])
                        #count_motif_size_4 =  G_igraph.motifs_randesu(4)
                        change_nan_to_zero(count_motif_size_4)

                        print("motifs size 5")
                        count_motif_size_5 = G_igraph.motifs_randesu(5, [0.4, 0.4, 0.4, 0.4, 0.4])
                        #count_motif_size_5 =  G_igraph.motifs_randesu(5)
                        change_nan_to_zero(count_motif_size_5)


                        csv_writer.writerow([exam_id , num_edges, density, avg_node_degree, avg_degree_centrality, 
                                             avg_closeness_centrality, avg_curr_flow_closeness_centrality, 
                                             avg_pagerank, avg_clustering_coef] + 
                                             count_motif_size_3 + count_motif_size_4 + count_motif_size_5)
                        
                        
def compute_avg_feature(feature_nodes):
    return sum(feat for nodes, feat in feature_nodes.items()) / len(feature_nodes)
def compute_sum_feature(feature_nodes):
    return(sum(feat for nodes, feat in feature_nodes.items()))               
def compute_features(G_nx):
    pass
def change_nan_to_zero(arr):   
    for i in range(len(arr)):
        if isinstance(arr[i], float) and np.isnan(arr[i]):
            arr[i] = 0
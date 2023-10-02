import pandas as pd
import h5py
import numpy as np
from ts2vg import NaturalVG
from scipy.sparse import coo_matrix
# Separar as amostras de acordo com o arquivo
df = pd.read_csv('stratified_sample.csv')

files_list = df['trace_file'].unique()

file_groups = {}

for file in files_list:
    file_groups[file] = df[df['trace_file'] == file]['exam_id'].values.tolist()
print(files_list)

exams_dir_path = '/scratch/raularaju/ecg_graph_diagnosis/dados'
output_file_hdf5 = h5py.File('./visibility_graphs.hdf5', 'w')


def cria_grafos_visibilidade(tracings):
    grafos_visibilidade = list() #TODO mudar para bitArray
    
    for leads in tracings.T: #pega a series transposta
        grafo = NaturalVG().build(leads).adjacency_matrix()
        grafo_esparso = coo_matrix(grafo)     
        grafos_visibilidade.append(grafo_esparso)
    return np.array(grafos_visibilidade)


def cria_matriz_features(features: np.array):
    matriz_features = np.zeros((8, 4096))
    for i in range(8):
        matriz_features[i] = features.T[i]

    return matriz_features

def armazena_grafos_visibilidade_e_features(arquivo_saida, id_exame, matriz_features,  grafos_visibilidade):
    print("Iniciando armazenamento de dados")
    grupo_exame = arquivo_saida.create_group('exame {}'.format(id_exame))
    for j in range(8):
        grupo_lead = grupo_exame.create_group('lead {}'.format(j))
        grupo_lead.create_dataset('features', data=matriz_features[j])
        grupo_grafo = grupo_lead.create_group('grafo')
        grupo_grafo.create_dataset('data', data=grafos_visibilidade[j].data)
        grupo_grafo.create_dataset('row', data=grafos_visibilidade[j].row)
        grupo_grafo.create_dataset('col', data=grafos_visibilidade[j].col)
    print("Dados armazenados com sucesso")

# Para cada arquivo, computar o grafo de visibilidade das amostras e guardar e salvar
for file in files_list:
    print(f"Coletando exames do arquivo {file}")
    with h5py.File(f"{exams_dir_path}/{file}",'r') as arquivo:
        traces_ids = np.array(arquivo['exam_id'])
        selected_indexes = np.zeros(len(file_groups[file]))
        i = 0
        for index, exam_id in enumerate(traces_ids):
           if exam_id in file_groups[file]:
               selected_indexes[i] = index
               i+=1 
        id_exams = np.array(arquivo['exam_id'])[selected_indexes.astype(int)]            
        tracings = np.array(arquivo['tracings'])[selected_indexes.astype(int)]
    tracings = np.delete(tracings,[2,3,4,5],axis = 2 ) # Remove dos LEADS as combinações Lineares DIII; AVR; AVL e AVF
    j = 0
    for id_exam, trace in zip(id_exams, tracings):
        print(trace.shape)
        print(f"Processando o exame {j+1} de {len(file_groups[file])}")
        grafos_comprimidos = cria_grafos_visibilidade(trace)
        matriz_features = cria_matriz_features(trace)
        armazena_grafos_visibilidade_e_features(output_file_hdf5, id_exam, matriz_features, grafos_comprimidos)
        j+=1
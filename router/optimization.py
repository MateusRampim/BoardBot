import networkx as nx
from scipy.spatial import distance_matrix
import numpy as np

def otimizar_caminho(contornos):
    # Verificar se há pelo menos dois contornos
    if len(contornos) <= 1:
        return contornos  # Não há necessidade de otimização

    # Obter pontos médios dos contornos
    pontos = [np.mean(c.reshape(-1, 2), axis=0) for c in contornos]

    # Criar matriz de distâncias
    dist_matrix = distance_matrix(pontos, pontos)

    # Criar grafo totalmente conectado
    G = nx.complete_graph(len(pontos))

    # Atribuir pesos com base nas distâncias
    for i in range(len(pontos)):
        for j in range(i+1, len(pontos)):
            G[i][j]['weight'] = dist_matrix[i, j]

    # Resolver o problema do caixeiro viajante (TSP)
    caminho = nx.approximation.traveling_salesman_problem(G, cycle=False)

    # Reordenar contornos seguindo o caminho otimizado
    return [contornos[i] for i in caminho]

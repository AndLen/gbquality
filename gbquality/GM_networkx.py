import networkx as nx
import numpy as np

import gbquality.GM as GM


def compute_x_leaves_networkx(X, K,pairwise_geodesic_x=None, G=None):
    if pairwise_geodesic_x is None:
        pairwise_euclidean_x = GM.euclidean_distance(X.T)
        G, paths, pairwise_geodesic = compute_paths_networkx(pairwise_euclidean_x, K)


    return compute_leaves_networkx(G, pairwise_geodesic_x)

def compute_paths_networkx(pairwise_euclidean, K):
    N = pairwise_euclidean.shape[0]
    adjacency_matrix = GM.get_weighted_adjacency_matrix(K, pairwise_euclidean, no_edge_val=0.)
    G = nx.Graph(adjacency_matrix)
    pairwise_geodesic = np.zeros((N, N))
    paths = []
    _dict = dict(nx.all_pairs_dijkstra(G))
    for i in _dict:
        res = _dict[i]
        pairwise_geodesic[i][list(res[0].keys())] = list(res[0].values())
        paths.append([])
        for v in sorted(res[1].keys()):
            paths[i].append(res[1][v])
    return G, paths, pairwise_geodesic


def compute_leaves_networkx(G, pairwise_geodesic):
    centre_idx = int(np.argmin(np.max(pairwise_geodesic, axis=0)))
    dists, paths = nx.single_source_dijkstra(G, centre_idx)
    non_leaves = set()
    for p in paths:
        for v in paths[p]:
            if p != v:
                non_leaves.add(v)
    print(non_leaves)
    leaf_indices = list(set(range(len(G))).difference(non_leaves))
    leaf_dists = pairwise_geodesic[centre_idx, leaf_indices]
    return leaf_indices, leaf_dists, centre_idx

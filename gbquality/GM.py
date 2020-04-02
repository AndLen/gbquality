# GM.m
from copy import deepcopy

import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import pairwise_distances


def global_judge(X, Y, k):
    """
    Please cite: "Deyu Meng, Yee Leung, Zongben Xu.
    Evaluating nonlinear dimensionality reduction based on its local
    and global quality assessments, Neurocomputing, 2011, 74(6): 941-948."

    The code is written by Deyu Meng & adapted by Andrew Lensen

    :param X: Original data (dim1*num)
    :param Y: Embedded data (dim2*num): dim2 < dim1
    :param k: Neighborhood size
    :return global quality in [0,1].
    """
    leaf_indices, leaf_dists, centre_index = compute_x_leaves(X, k)
    return global_judge_x_precomputed(leaf_indices, leaf_dists, centre_index, Y)


def global_judge_x_precomputed(leaf_indices, x_dists, centre_index, Y):
    """
    :param leaf_indices: Indices of all the leaves of the SPT (size 1*L)
    :param x_dists: Dists along the SPT from centre to each of the leaves (1*L)
    :param centre_index: Index of the approximate circumcenter of X
    :param Y: Embedded data (dim*num)
    :return global quality in [0,1].
    """
    pairwise_y = pairwise_distances(Y.T)
    y_dists = pairwise_y[centre_index, leaf_indices]

    global_score = (1 + spearmanr(x_dists, y_dists)[0]) / 2
    return global_score


def compute_x_leaves(X, K):
    """
    All the heavy pre-processing on the source data. Only needs to be run once, so it's not particularly efficient!
    :param X: Original data (dim1*num)
    :param K: Neighbourhood size
    :return: leaf_indices, leaf_dists, centre_index
    """
    # matlab's L2_distance converts feature-major to instance-major
    pairwise_x = pairwise_distances(X.T)
    N = pairwise_x.shape[0]
    INF = 1000 * np.max(np.max(pairwise_x)) * N  # effectively infinite distance
    ind = np.argsort(pairwise_x, axis=1)[:, :K + 1]
    _D = np.full((N, N), INF)
    np.fill_diagonal(_D, 0.)
    # _D = np.zeros((N, N))
    for ii in range(N):
        # I think this is right for nx?
        _D[ii, ind[ii]] = pairwise_x[ii, ind[ii]]
    pairwise_x = _D
    pairwise_x = np.minimum(pairwise_x, pairwise_x.T)
    # CHECK
    # otherwise it uses the same list for each row...
    PP = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append([i, j])
        PP.append(row)
    # shortest paths
    for k in range(N):
        for ii in range(N):
            for jj in range(N):
                if pairwise_x[ii, jj] > pairwise_x[ii, k] + pairwise_x[k, jj]:
                    PP[ii][jj] = PP[ii][k][:- 1] + PP[k][jj]
        pairwise_x = np.minimum(pairwise_x,
                                np.repeat(pairwise_x[:, k], N).reshape(N, N) + np.tile(pairwise_x[k, :], [N, 1]))
    spt_dists_x = pairwise_x
    a = np.max(pairwise_x, axis=0)
    centre_index = int(np.argmin(a))
    max_dist = max(pairwise_x[centre_index, :])
    indices = [x for x in range(N) if x != centre_index]
    candidate_leaves = []
    while len(indices) > 0:
        idx = indices[0]
        idx_path = deepcopy(PP[centre_index][idx])
        candidate_leaves.append(idx)
        idx_path.remove(centre_index)

        while len(idx_path) > 1:
            if idx_path[0] in indices:
                # it can't be a leaf
                indices.remove(idx_path[0])
            if idx_path[0] in candidate_leaves:
                # it can't be a leaf
                candidate_leaves.remove(idx_path[0])
            idx_path.remove(idx_path[0])

        indices.remove(idx_path[0])
        idx_path.remove(idx_path[0])
    n_leaves = len(candidate_leaves)
    potential_leaves = []
    final_leaf_indices = []
    k = 0
    for i in range(n_leaves):
        temp_leaf = candidate_leaves[i]
        temp_leaf2 = PP[centre_index][temp_leaf][1]
        if temp_leaf2 in potential_leaves:
            Tempi = potential_leaves.index(temp_leaf2)
            if pairwise_x[centre_index, temp_leaf] > pairwise_x[centre_index, final_leaf_indices[Tempi]]:
                final_leaf_indices[Tempi] = temp_leaf
        elif pairwise_x[centre_index, temp_leaf] > max_dist / 6:
            k = k + 1
            potential_leaves.insert(k, temp_leaf2)
            final_leaf_indices.insert(k, temp_leaf)
    leaf_dists = spt_dists_x[centre_index, final_leaf_indices]
    return final_leaf_indices, leaf_dists, centre_index
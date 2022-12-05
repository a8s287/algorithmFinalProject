# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 12:51:01 2022

@author: Daniel
"""
import csv
import os
import networkx as nx
import matplotlib.pyplot as plt
from typing import Type


def load_instances(file_path: str) -> list[list[list]]:
    """
    load_instances will load from a csv ith format specified by project assignment
    k
    edges, vertices
    u, v
    ....
    edges, vertices
    u, v
    ....

    Parameters
    ----------
    file_path : str
        csv path.

    Returns
    -------
    list[list[list]]
        list contains 
        number of instances
        number of edges
        edge [u, v].

    """
    instances = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        
        num_instances = next(reader)
        for instance in range(int(num_instances[0])):
            vertices, edges = next(reader)
            current_instance = [[vertices, edges]]
            for i in range(int(edges)):
                current_instance.append(next(reader))
            instances.append(current_instance)
    
    return instances

def leaf_count(G: Type[nx.Graph]) -> int:
    """
    Counts number of leaves in a graph, vertices with degree 1

    Parameters
    ----------
    G : Type[nx.Graph]
        the graph, should be tree.

    Returns
    -------
    int
        number of leaves.

    """
    
    leaves = 0
    
    for vertex in list(G.nodes):
        if (G.degree[vertex] == 1):
            leaves += 1
            
    return leaves

if __name__=="__main__":
    
    instances = load_instances(os.path.join(os.getcwd(), "8_8_sparse.csv"))
    
    G = nx.Graph()
    
    G.add_edges_from(instances[0][1:])
    
    # nx.draw_networkx(G)
    
    BFS_Tree = nx.bfs_tree(G, '1')
    BFS_leaves = leaf_count(BFS_Tree)
    
    print(BFS_leaves)
    
    
    
    
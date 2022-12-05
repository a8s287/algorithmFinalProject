# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 12:51:01 2022

@author: Daniel
"""
import csv
import os
import networkx as nx
import matplotlib.pyplot as plt


def load_instances(file_path):
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

def leaf_count(G):
    
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
    
    
    
    
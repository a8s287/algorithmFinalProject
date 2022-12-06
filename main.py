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
from unionFind import union_find


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

def maximally_leafy_forest(G: Type[nx.Graph]) -> Type[union_find]:
    """
    maximally_leafy_forest generation for Lu-Ravi algorithm

    Parameters
    ----------
    G : Type[nx.Graph]
        DESCRIPTION.

    Returns
    -------
    None.

    """
    #TODO: WTF DOESNT WORK
    
    Subtrees = union_find()
    degrees = {}
    
    for vertex in list(G.nodes):
        T = nx.Graph()
        T.add_node(vertex)
        
        Subtrees.new_subtree(vertex, T, vertex)
        degrees[vertex] = 0
        
    for vertex in list(G.nodes):
        S_prime = []
        d_prime = 0
        
        for edge in G.edges(vertex):
            if((edge[1] not in Subtrees.get_subtree(vertex)) 
               and (Subtrees.getKey(edge[1]) not in S_prime)):
                d_prime = d_prime + 1
                
                #Insert subtrees[u] into S_prime
                S_prime.append(Subtrees.getKey(edge[1]))
                
        if (degrees[vertex] + d_prime >= 3):
            for subtree in S_prime:
                cur_subtree = Subtrees.get_subtree_from_key(subtree)
                
                Subtrees.merge(vertex, cur_subtree[1])
                degrees[vertex] = degrees[vertex] + 1
                degrees[cur_subtree[1]] = degrees[cur_subtree[1]] + 1
                
    
    # print(Subtrees)
    
    return Subtrees

def combine_forest(F: Type[union_find], G: Type[nx.Graph]) -> Type[nx.Graph]:
    
    root_tree = F.get_subtree_from_key(list(F.getKeys())[0])[0]
    
    for subtree in list(F.getKeys())[1:]:
        for node in F.get_subtree_from_key(subtree)[0].nodes:
            for check_node in root_tree.nodes:
                if G.has_edge(node, check_node) or G.has_edge(check_node, node):
                    F.merge(check_node, node, root1=check_node, root2=node)
    
    return F.get_subtree_from_key(list(F.getKeys())[0])[0]
    

if __name__=="__main__":
    
    instances = load_instances(os.path.join(os.getcwd(), "Graph.csv"))
    
    G = nx.Graph()
    
    G.add_edges_from(instances[0][1:])
    
    nx.draw_networkx(G)
    plt.show()
    
    
    BFS_Tree = nx.bfs_tree(G, '1')
    BFS_leaves = leaf_count(BFS_Tree)
    
    F = maximally_leafy_forest(G)
    F_tree = combine_forest(F, G)
    F_tree_leaves = leaf_count(F_tree)
    
    nx.draw_networkx(F_tree)
    plt.show()
    
    print("BFS leaves: {}, Lu-Parv leaves: {}".format(BFS_leaves, F_tree_leaves))
    
    
    
    
    
    
    
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

def maximally_leafy_forest(G: Type[nx.Graph]) -> Type[nx.Graph]:
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
    
    F = nx.Graph()
    Subtrees = {}
    degrees = {}
    
    
    for vertex in list(G.nodes):
        Subtrees[vertex] = {vertex}
        degrees[vertex] = 0
        
    for vertex in list(G.nodes):
        S_prime = []
        d_prime = 0
        
        for edge in G.edges(vertex):
            if((edge[1] not in Subtrees[vertex]) and (edge[1] not in S_prime)):
                d_prime = d_prime + 1
                
                #Insert subtrees[u] into S_prime
                S_prime.append(edge[1])
                
        if (degrees[vertex] + d_prime >= 3):
            for u in S_prime:
                F.add_edge(u, vertex)
                
                temp = Subtrees[vertex]
                Subtrees[vertex] = Subtrees[vertex].union(Subtrees[u])
                Subtrees[u] = Subtrees[u].union(temp)
                
                degrees[u] = degrees[u] + 1
                degrees[vertex] = degrees[vertex] + 1
    
    return F

if __name__=="__main__":
    
    instances = load_instances(os.path.join(os.getcwd(), "hard.in"))
    
    G = nx.Graph()
    
    G.add_edges_from(instances[3][1:])
    
    nx.draw_networkx(G)
    plt.show()
    
    
    BFS_Tree = nx.bfs_tree(G, '1')
    BFS_leaves = leaf_count(BFS_Tree)
    
    F = maximally_leafy_forest(G)
    nx.draw_networkx(F)
    plt.show()
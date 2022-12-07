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
        reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
        
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
    

def solve_instance(instance, draw=True):
    
    G = nx.Graph()
    
    G.add_edges_from(instance[1:])
    
    if draw:
        nx.draw_networkx(G)
        plt.show()
    
    
    BFS_Tree = nx.bfs_tree(G, '1')
    BFS_leaves = leaf_count(BFS_Tree)
    
    F = maximally_leafy_forest(G)
    F_tree = combine_forest(F, G)
    F_tree_leaves = leaf_count(F_tree)
    
    if draw:
        nx.draw_networkx(F_tree)
        plt.show()
    
    print("BFS leaves: {}, Lu-Parv leaves: {}".format(BFS_leaves, F_tree_leaves))
    
    if(F_tree_leaves > BFS_leaves):
        return (F_tree, F_tree_leaves)
    
    else:
        return (BFS_Tree, BFS_leaves)
    

def run_instances(instances, file_name="Solved.out"):
    for instance in instances:
        
        T, leaves = solve_instance(instance)
        
        outlist = []
        
        head = [leaves, 0]
        
        for edge in T.edges:
            outlist.append(list(map(int, edge)))
            head[1] += 1
            
        outlist = sorted(outlist, key=lambda x: x[0])
        
        outlist = [head] + outlist
        
        with open(file_name, "a", newline='') as f:
           writer = csv.writer(f)
           
           writer.writerows(outlist)
    
def Solis(instances):
    instances.pop()
    instances.pop()
    instances.pop()
    instances.pop()
    instances.pop()
    instances.pop()
    instances.pop()
    for instance in instances:
        G = nx.Graph()
        copyG = nx.Graph()
        node_num = 0
        edges_num = 0
        # build the input graph with nodes and edges
        for i in range(0,len(instance),1) :
            if i == 0:
                node_num = instance[i][0]
                edges_num = instance[i][1]
            else:
                copyG.add_edge(instance[i][0],instance[i][1])
                G.add_edge(instance[i][0],instance[i][1])
        #nx.draw(G, with_labels=True, font_weight='bold')
        print(G.nodes)
        
        
        
        #build a forest which is void at first
        F = []
        #while there is a vertex v of degree at least 3 do
        flag = 1
        while flag == 1:
            flag = 0
            vertex = None
            for v in G.nodes:
                if G.degree(v) > 2:
                    flag = 1
                    vertex = v
                    break
            if flag == 1:
                #Build a tree Ti with root v and leaves the neighbors of v
                T = nx.Graph()
                T.add_node(vertex)
                print("root:"+vertex)
                G,T = root_expand(G, vertex, T)
                #nx.draw(T, with_labels=True, font_weight='bold')
                #plt.show() 
                F.append(T)
                #print(T.nodes)
                #print(G.nodes)
                #print(G.edges)
                        
                    #while at least one leaf of Ti can be expanded do
                    #case v has exactly two neighbors outside F
                    #G.adjacency(v)
                    
                    #print(v)
        
        
        """for i in F: 
            print(i.nodes)
            nx.draw(i, with_labels=True, font_weight='bold')
            plt.show() """
        print(G.edges)
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show() 
        
        for i in list(G.nodes):
            Ti = nx.Graph()
            if i in G.nodes:
                Ti,G = separateGNodes(G,i,Ti)
            if len(Ti.nodes) > 0:
                F.append(Ti)
        for i in F:
            nx.draw(i, with_labels=True, font_weight='bold')
            plt.show() 
        #Connect the trees in F and all vertices not in F to form a spanning tree T .
        
        return connect(F,copyG)
def connect(F,G):
    C = nx.Graph()
    C.add_edges_from(F[0].edges)
    F.remove(F[0])
    #print("edg")
    #print(G.edges)
    
    
    
    while len(F) != 0:
        for node in C.nodes:
            flag = False
            for tree in F:
                for nodes in tree:
                    if (node,nodes) in G.edges:
                        C.add_edges_from(tree.edges)
                        C.add_edge(node,nodes)
                        flag = True
                        F.remove(tree)
                        break
                if flag == True:
                    break
            if flag == True:
                break
      
    
    
    return C
def root_expand(G, v, T):
    for root in list(G.adjacency()):
        if root[0] == v:
            #add neighbor into Ti
            #neighbors = []
            for neighbor in root[1]:
                """color = None
                if G.degree(neighbor) == 3:
                    #color blue means priorty 1
                    color = "blue"
                elif G.degree(neighbor) > 3:
                    #color green means priorty 2
                    color = "green"
                else:
                    #color NULL means no need to expand
                    color = "NULL"
                neighbors.append(neighbor)"""
                #print(v+" "+neighbor)
                T.add_node(neighbor)
                """.nodes[neighbor]['color'] = color"""
                if T.degree(neighbor) == 0:
                    T.add_edge(*(v,neighbor))
            #after adding v to T and find all neighbor of v, remove it
            G.remove_node(v)
            #calculate T.nodes priorty
            for t_node in list(T.nodes):
               t = 0
               for r in list(G.adjacency()):
                   if r[0] == t_node:
                       for neigh in r[1]:
                           if neigh in T.nodes:
                               t+=1
               #if(type(G.degree(t_node)) == (int)):
                   #print(G.degree(t_node))
               #print(t)
               if type(G.degree(t_node)) == (int) and G.degree(t_node)-t== 2:
                   #color blue means priorty 1
                   color = "blue"
                   #print(t_node +" "+color)
               elif type(G.degree(t_node)) == (int) and G.degree(t_node)-t> 2:
                    #color green means priorty 2
                    color = "green"
                   # print(t_node +" "+color)
               else:
                    #color NULL means no need to expand
                    color = "NULL"
                    #print(t_node +" "+color)
                    if t_node in G.nodes:
                        G.remove_node(t_node)
            
               T.nodes[t_node]['color'] = color
            #expand the highest priorty in the T tree
            for t_node in list(T.nodes):
                if T.nodes[t_node]['color'] == "green":
                    t = 0
                    for r in list(G.adjacency()):
                        if r[0] == t_node:
                            for neigh in r[1]:
                                if neigh in T.nodes:
                                    t+=1
                        #print(t_node+" "+t)
                        if type(G.degree(t_node)) == (int) and G.degree(t_node)-t >= 2:
                            G,T = root_expand(G,t_node,T)
                            #print(t_node+" expand_neighbor")
                        else:
                            if t_node in G.nodes:
                                G.remove_node(t_node)
                            #G,T = neighbor_expand(G,t_node,T)
            for t_node in list(T.nodes):
                if T.nodes[t_node]['color'] == "blue":
                    t = 0
                    for r in list(G.adjacency()):
                        if r[0] == t_node:
                            for neigh in r[1]:
                                if neigh in T.nodes:
                                    t+=1
                        #print(str(t_node)+" "+str(t))
                    if type(G.degree(t_node)) == (int) and G.degree(t_node)-t >= 2:
                        G,T = root_expand(G,t_node,T)
                        print(t_node+" expand_neighbor")
                    else:
                        if t_node in G.nodes:
                            G.remove_node(t_node)
                        #G,T = neighbor_expand(G,t_node,T)
                        
            #expand neighbor with priorty 2 first, then expand priorty 1
            """for neighbor in neighbors:
                if(T.nodes[neighbor]['color'] == "green"):
                    print(neighbor)
                    G,T = neighbor_expand(G,neighbor,T)
            for neighbor in neighbors:
                if(T.nodes[neighbor]['color'] == "blue"):
                    print(neighbor)
                    G,T = neighbor_expand(G,neighbor,T)
            for neighbor in neighbors:
                if(T.nodes[neighbor]['color'] == "NULL"):
                    if neighbor in G.nodes:
                        G.remove_node(neighbor)  """
    return(G,T)
"""def neighbor_expand(G,v,T):
    t = 0
    for r in list(G.adjacency()):
        if r[0] == v:
            for neigh in r[1]:
                if neigh in T.nodes:
                    t+=1
    if type(G.degree(v)) != (int) or G.degree(v)-t < 2:
        return G,T
    for root in list(G.adjacency()):
        if root[0] == v:
            #add neighbor into Ti
            #neighbors = []
            for neighbor in root[1]:
                t = 0
                for r in list(G.adjacency()):
                    if r[0] == neighbor:
                        for neigh in r[1]:
                            if neigh in T.nodes:
                                t+=1
                color = None
                print(neighbor+" "+str(G.degree(neighbor)-t))
                if G.degree(neighbor)-t == 2:
                    #color blue means priorty 1
                    color = "blue"
                elif G.degree(neighbor)-t > 2:
                    #color green means priorty 2
                    color = "green"
                else:
                    #color NULL means no need to expand
                    color = "NULL"
                neighbors.append(neighbor)
                T.add_node(neighbor)
                #T.nodes[neighbor]['color'] = color
                if T.degree(neighbor) == 0:
                    T.add_edge(*(v,neighbor))
            #after adding v to T and find all neighbor of v, remove it
            G.remove_node(v)
            
            
            #expand T.leaves with priorty 2 first, then expand priorty 1
            for t in list(T.nodes):
                indegree = 0
                for r in list(T.adjacency()):
                    if r[0] == t:
                        for neigh in r[1]:
                            if neigh in T.nodes:
                                indegree+=1
                color = None
                print(t+" "+str( T.degree(t)-indegree))
                if type(G.degree(t)) == (int) and G.degree(t)-indegree == 2:
                    #color blue means priorty 1
                    color = "blue"
                elif type(G.degree(t)) == (int) and G.degree(t)-indegree > 2:
                    #color green means priorty 2
                    color = "green"
                else:
                    #color NULL means no need to expand
                    color = "NULL"
                    if t in G.nodes:
                        G.remove_node(t)
                T.nodes[t]['color'] = color
                G,T = neighbor_expand(G,t,T)
            for neighbor in neighbors:
                if(T.nodes[neighbor]['color'] == "green"):
                    print(neighbor)
                    G,T = neighbor_expand(G,neighbor,T)
            for neighbor in neighbors:
                if(T.nodes[neighbor]['color'] == "blue"):
                    print(neighbor)
                    G,T = neighbor_expand(G,neighbor,T)
            for neighbor in neighbors:
                if(T.nodes[neighbor]['color'] == "NULL"):
                    if neighbor in G.nodes:
                        G.remove_node(neighbor)  
    return(G,T)"""

def separateGNodes(G,root,Ti):
    flag = False
    if root not in Ti.nodes:
        Ti.add_node(root)
    for edge in G.edges:
        if root in edge:
            flag = True
    if flag == False:
        if root in G.nodes:                    
            G.remove_node(root)
        return Ti,G
    
    """for edge in G.edges:
        if root in edge:
            Ti.add_edges_from([edge])
            G.remove_edges_from([edge])"""
    for adj in list(G.adjacency()):
        if adj[0] == root:
            if(len(adj[1]) == 0):
                break
            for neighbor in list(adj[1]):
                Ti.add_edge(root,neighbor)
                G.remove_edge(root,neighbor)
                separateGNodes(G,neighbor,Ti)
    if root in G.nodes:                    
        G.remove_node(root)
    return Ti,G
        
if __name__=="__main__":
    
    instances = load_instances(os.path.join(os.getcwd(), "Hard.in"))
    
    #run_instances(instances)
    C = Solis(instances)
    print(len(C.nodes))
    print(len(C.edges))
    nx.draw(C, with_labels=True, font_weight='bold')
    plt.show() 
    """
    Testing of seperate G nodes
    G = nx.Graph()
    G.add_nodes_from([3,18,7,10,20,21,8,17,1,2,5,9])
    G.add_edges_from([(7,10),(8,18), (18,20), (20,21),(1,2),(2,5),(2,17),(20,9)])
    
    F = []
    
    for i in list(G.nodes):
        Ti = nx.Graph()
        if i in G.nodes:
            Ti,G = separateGNodes(G,i,Ti)
        if len(Ti.nodes) > 0:
            F.append(Ti)
    for i in F:
        nx.draw(i, with_labels=True, font_weight='bold')
        plt.show() 
    """
    
    
    
    
    
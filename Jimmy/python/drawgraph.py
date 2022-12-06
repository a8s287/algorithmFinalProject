# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 13:51:33 2022

@author: qq306
"""
import matplotlib.pyplot as plt
import networkx as nx
import random
G = nx.Graph()
"""
for i in range(20):
    G.add_node(i)
    
G.add_edge(0, 2)
G.add_edge(0, 3)
G.add_edge(0, 4)
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(0, 1)
G.add_edge(0, 5)
G.add_edge(5, 6)
G.add_edge(4, 6)

nx.draw_random(G)

for i in range (40):
    G.add_node(i)

for j in range(1, 4):
    G.add_edge(0,j)
    
for j in range(4, 13):
    if (j<=6):
        G.add_edge(1,j)
    elif (j <= 9):
        G.add_edge(2,j)
    else:
        G.add_edge(3,j)
        
for j in range (13, 40):
    if (j<= 15):
        G.add_edge(4,j)
    elif (j<= 18):
        G.add_edge(5,j)
    elif (j<= 21):
        G.add_edge(6,j)
    elif (j<= 24):
        G.add_edge(7,j)
"""       
for i in range(0,40):
    G.add_node(i)
    
a = random.randint(1,4)
print(a)
for j in range(0,13):
    G.add_edge(j, j*3+1)
    G.add_edge(j, j*3+2)
    G.add_edge(j, j*3+3)
        
nx.draw(G, with_labels= True, )

plt.show()

#print("Vertex set: ",G.nodes())
print("Edge set: ",G.edges())

#print(list(nx.bfs_edges(G,0)))

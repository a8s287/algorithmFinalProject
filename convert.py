# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 17:13:12 2022

@author: Daniel
"""

import csv
import os


if __name__ == "__main__":
    
    graph = [[0,0]]
    
    with open("out_file.csv", 'r') as f:
        reader = csv.reader(f)

        for v, vertex_list in enumerate(reader):
            graph[0][0] += 1
            for edge in vertex_list:
                graph[0][1] += 1
                
                graph.append([v, edge])
        
    print(graph)
    
    with open("instance.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        
        writer.writerows(graph)
                
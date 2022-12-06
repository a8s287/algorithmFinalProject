# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 21:31:18 2022

@author: qq306
"""
from graph import *
from graph_helper import *
from constants import *
from collections import deque

def input_graphs_from_file(file_name):

	# Read in raw lines
	with open(file_name) as input_file:
		raw_lines = input_file.readlines()

	# Strip newline from each line
	for i in range(len(raw_lines)):
		raw_lines[i] = raw_lines[i].strip()

	# Store lines in a queue (using deque) for efficient processing
	lines = deque(raw_lines)

	# Maintain a list of graphs
	graphs = []

	# Read the number of graphs in file
	if len(lines) > 0:
		number_of_graphs = int(lines.popleft())
	else:
		return []

	# Read lines in nested structure
	for _ in range(number_of_graphs):
		edges = []
		number_of_edges = int(lines.popleft())

		for _ in range(number_of_edges):
			edge_ends = lines.popleft().split()
			u = int(edge_ends[0])
			v = int(edge_ends[1])
			edges.append(Edge(u, v))

		graph = make_graph(edges)
		graphs.append(graph)
        

    
	return graphs
if __name__=="__main__":
    print(input_graphs_from_file("hard.in"))
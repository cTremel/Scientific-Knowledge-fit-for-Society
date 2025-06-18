import os
import numpy as np
import pandas as pd
import wikipedia
from helpers import cleaning
from helpers import createGraph

import networkx as nx
from pyvis.network import Network

src_folder = "source/"
directory = os.fsencode(src_folder)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    openedFile = open((src_folder + filename), "r")
    text = openedFile.read()
    initial_tup_ls = cleaning.create_svo_triples(text, print_lists=False)
    """ f = open("tup_ls.txt", "w")
    f.write(str(initial_tup_ls) + '\n')
    f.close()
 """

print(text)

edges_word_vec_ls = createGraph.edge_tuple_creation(text)
node_tup_ls = createGraph.node_tuple_creation(edges_word_vec_ls)

G = nx.Graph()
G.add_nodes_from(edges_word_vec_ls)
G.add_edges_from(node_tup_ls)

net = Network(notebook=True, cdn_resources='in_line')
net.from_nx(G)
net.show("ipccPR.html") 


#text= wikipedia.summary('barack obama')

# ----------------------------------------------- Method 1 ---------------------------------------------------------------------------------------------------------------------------------
"""
initial_tup_ls = cleaning.create_svo_triples(text, print_lists=False)

init_obj_tup_ls = cleaning.get_obj_properties(initial_tup_ls)
new_layer_ls = cleaning.add_layer(init_obj_tup_ls)

f = open("tup_ls.txt", "w")
f.write(str(initial_tup_ls) + '\n')
f.write(str(init_obj_tup_ls) + '\n')
f.write(str(new_layer_ls) + '\n')
f.close()

starter_edge_ls = init_obj_tup_ls + new_layer_ls
edge_ls = cleaning.subj_equals_obj(starter_edge_ls)
#clean_edge_ls = check_for_string_labels(edge_ls)
#clean_edge_ls[0:3]
clean_edge_ls = edge_ls


edges_word_vec_ls = cleaning.create_word_vectors(edge_ls)

f = open("edge.txt", "w")
f.write(str(starter_edge_ls) + '\n')
f.write(str(edge_ls) + '\n')
f.write(str(edges_word_vec_ls) + '\n')
f.close()

orig_node_tup_ls = [(edge_ls[0][0], '', ['Subject'], '', np.random.uniform(low=-1.0, high=1.0, size=(300,)))]
obj_node_tup_ls = [(tup[2], tup[3], tup[4], tup[5], tup[6]) for tup in edges_word_vec_ls]
full_node_tup_ls = orig_node_tup_ls + obj_node_tup_ls
dedup_node_tup_ls = createGraph.dedup(full_node_tup_ls)

f = open("node.txt", "w")
f.write(str(orig_node_tup_ls) + '\n')
f.write(str(obj_node_tup_ls) + '\n')
f.write(str(full_node_tup_ls) + '\n')
f.write(str(dedup_node_tup_ls) + '\n')
f.close()

print(len(full_node_tup_ls), len(dedup_node_tup_ls)) """

# ----------------------------------------------- Method 2 ---------------------------------------------------------------------------------------------------------------------------------


""" G = nx.Graph()
G.add_nodes_from([2, 3])
G.add_edges_from([(1, 2), (1, 3)])

net = Network(notebook=True, cdn_resources='in_line')
net.from_nx(G)
net.show("example.html") """

""" barack_text = wikipedia.summary('barack obama')
barack_edges_word_vec_ls = createGraph.edge_tuple_creation(barack_text)
barack_node_tup_ls = createGraph.node_tuple_creation(barack_edges_word_vec_ls)
G = nx.Graph()
G.add_nodes_from(barack_node_tup_ls)
G.add_edges_from(barack_edges_word_vec_ls)

net = Network(notebook=True, cdn_resources='in_line')
net.from_nx(G)
net.show("barack.html") """
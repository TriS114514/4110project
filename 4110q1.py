#4110 final project assignment
#Author: Shohei Saito & 
#Topic 1: generate random path, illistrate puring process, compute p-center problem

# p-center
import osmnx as ox
import networkx as nx
import random
from random import choice
%matplotlib inline
np.random.seed(1)

#generate random path
rnd = random.randint(8,16) # number of nodes
G = nx.Graph()
H=nx.path_graph(rnd)
G.add_nodes_from(H)
i = 0
for n in G:
    j = choice([k for k in range(0,rnd) if k not in [i]])
    G.add_edge(i,j)
    i+=1



nd = G.number_of_nodes()
ed = G.number_of_edges()
ndc = G.nodes()
edc = G.edges()
print('number of nodes: ', nd)
print('number of edges: ', ed)
print(ndc)
print(edc)

#puring process


#p-center
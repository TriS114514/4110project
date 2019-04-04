#4110 final project assignment
#Author: Shohei Saito & 
#Topic 1: generate random path, illistrate puring process, compute p-center problem

# p-center
import osmnx as ox
import networkx as nx
import numpy as np
import random
import math
from random import choice
%matplotlib inline
np.random.seed(1)

#generate random path
#rnd = random.randint(10,15)

#set number of nodes
src = int(input("# of nodes for the graph: ")) # user enters # of nodes
G = nx.Graph()
H=nx.path_graph(src)
G.add_nodes_from(H)

#add edges to nodes(random)
#i = 0
#for n in G:
#    j = choice([k for k in range(0,src) if k not in [i]])
#    G.add_edge(i,j)
#    i+=1

#add edges to node(straight)
for n in range(src-1):
    G.add_edge(n,n+1)

#compute graph data
nd = G.number_of_nodes()
ed = G.number_of_edges()
ndc = G.nodes()
edc = G.edges()
print('number of nodes: ', nd)
print('number of edges: ', ed)
print(ndc)
print(edc)

#set the p value
p = int(input("the # of facilities: "))
opt = int(float(src)/p) #round down
ppt = math.ceil(opt/2)
print(opt)
print(ppt)
plist = []
#puring process


#p-center
y=0
for x in range(src):
    if y == ppt:
        plist.append(x)
        y=-ppt
    y+=1

print("vertex with facilities: ", plist)
b=0
c=0
for nd in G:
    for fc in plist:
        if nd == fc:
            b=0
            continue
        a= nx.shortest_path_length(G, nd, fc)
        if a < b or b==0:
            b=a
    if b > c:
        c=b
    b=0
print("p-center max length: ",c)
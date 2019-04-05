#4110 final project assignment
#Author: Shohei Saito & Darsh Thanki
#Topic 1: generate random path, illistrate puring process, compute p-center problem

# p-center
#import osmnx as ox
import networkx as nx
import numpy as np
import random
import math
from random import choice
#%matplotlib inline
np.random.seed(1)

#get all_pairs_shortest_path (apsp) of given graph.
def get_apsp(graphx, all_node_keys):
    apsp = {}
    for i, node in enumerate(all_node_keys):
        #print('{}:{}'.format(i, len(all_node_keys)))
        # Compute the length of paths from node to every other node
        apsp[node] = nx.shortest_path_length(graphx, source=node)

    return apsp

def p_center(p, graphx):

    all_node_keys = list(graphx._node.keys())

    apsp = get_apsp(graphx, all_node_keys)

    # Get the maximum length to each node
    app_maxs = {
        k: max(v.values()) for k, v in
        apsp.items()
    }

    # Get rid of 0 length paths
    all_node_keys = [x for x in all_node_keys if app_maxs[x] != 0]
    apsp = {k:v for k,v in apsp.items() if v != 0}

    # Assign the first 'p' nodes to be our solution
    centers = all_node_keys[:p]

    # Compute the total cost for each center in `centers`
    cost_center = {k: app_maxs[k] for k in centers}

    centers, cost_center = calc_p_center(
        centers,
        all_node_keys,
        app_maxs,
        cost_center
    )

    node_information = {}
    for center in centers:
        node = graphx._node[center]
        node_information[center] = {
            'id': center,
        }

    total_cost = sum(cost_center.values())

    return total_cost, node_information

def calc_p_center(centers, all_node_keys, app_maxs, cost_center):
    """
    Pick an arbitrary solution. Then replace each with was a node that isn't part of the
    previous solution. If the max distance is less that the prior solution, swap that node.
    """
    while True:
        wrap = False
        for i, center in enumerate(centers):
            if wrap:
                break
            for j, prospect in enumerate(all_node_keys):
                prospect_distance = app_maxs[prospect]
                if prospect not in cost_center:
                    # Replace `center` in cost_center with `prospect`
                    print("prospect: ", prospect)
                    new_cost_center = {k:v for k,v in cost_center.items() if k != center}
                    new_cost_center[prospect] = prospect_distance
                    if sum(new_cost_center.values()) < sum(cost_center.values()):
                        # If we're better off with `prospect`, then use it instead
                        cost_center.pop(center, None)
                        cost_center[prospect] = app_maxs[prospect]
                        # Reassign centers and restart the while loop
                        medians = [x for x in cost_center]
                        wrap = True
                        break # out of the For loop
        if not wrap:
            # This happens if we've iterated all nodes
            # and none of them improved the solution.
            return centers, cost_center

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

p_center(p, G);

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

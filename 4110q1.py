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
import matplotlib.pyplot as plt
#%matplotlib inline
np.random.seed(1)

#get all_pairs_shortest_path (apsp) of given graph.
def get_apsp(graphx, all_nodes):
    apsp = {}
    for i, node in enumerate(all_nodes):
        # Compute the length of paths from node to every other node
        apsp[node] = nx.shortest_path_length(graphx, source=node)

    return apsp

def c_cost(centers, all_nodes, graphx, node_pointer): # determine the max cost for current p-centers
    cost = 0
    min_cost = len(all_nodes)
    pop = False
    apsp = get_apsp(graphx, all_nodes)
    # find the shortest path from all p, keep the max value
    for node in node_pointer:
        min_cost = len(all_nodes)
        for center in centers: # do a pruning step if a node can't be max length
            print("Evaluating Node: ", node)
            print("Evaluating Center Candidate: ", center)
            print("Centers: ", *centers)
            print("Node_pointer: ", *node_pointer)

            temp_cost = nx.shortest_path_length(graphx, center, node)
            if temp_cost <= cost:
                print("prune this Node")
                pop=True# prune out if a cost was 0
            elif temp_cost < min_cost:
                min_cost = temp_cost
            print("---")
        if pop:
            pop = False
            continue
        if min_cost > cost:
            cost=min_cost

    return cost


def p_center(p, graphx):

    all_nodes = list(graphx._node.keys())

    apsp = get_apsp(graphx, all_nodes)

    # Get the maximum length to each node
    app_maxs = {
        k: max(v.values()) for k, v in
        apsp.items()
    }

    # Some pruning handled here to remove 0 length paths
    all_nodes = [x for x in all_nodes if app_maxs[x] != 0]
    apsp = {k:v for k,v in apsp.items() if v != 0}

    # Assign the first 'p' nodes to be our solution
    centers = all_nodes[:p]

    # Compute the total cost for each center in `centers
    node_pointer = []
    for e in graphx:
        node_pointer.append(e)

    cost_center = c_cost(centers, all_nodes, graphx, node_pointer) # compute the largest cost for current p-center

    centers, cost_center = calc_p_center(
        centers,
        all_nodes,
        app_maxs,
        graphx,
        cost_center,
        node_pointer
    )

    node_information = {}
    for center in centers:
        node = graphx._node[center]
        node_information[center] = {
            'id': center,
        }

    total_cost = cost_center

    return total_cost, node_information

def calc_p_center(centers, all_nodes, app_maxs, graphx, cost_center, node_pointer):
    """
    Pick an arbitrary solution. Then replace each with was a node that isn't part of the
    previous solution. If the max distance is less that the prior solution, swap that node.
    """
    while True:
        wrap = False
        for i, center in enumerate(centers):
            for j, prospect in enumerate(all_nodes):
                new_centers = centers # make copy of center to change
                if prospect not in centers:
                    # Replace `center` in cost_center with `prospect`
                    original = new_centers[i]
                    new_centers[i]=prospect
                    new_cost = c_cost(new_centers, all_nodes, graphx, node_pointer)
                    if new_cost <= cost_center: # set new center, restart from first for loop
                        centers = new_centers
                        cost_center=new_cost
                        wrap = True
                    else:
                        new_centers[i]=original
                        break

        if not wrap:
            # This happens if we've iterated all nodes
            # and none of them improved the solution.
            return centers, cost_center

#set number of nodes
src = int(input("# of nodes for the graph: ")) # user enters # of nodes
G = nx.Graph()
H=nx.path_graph(src)
G.add_nodes_from(H)

#add edges to node
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
p = 1
opt = int(float(src)/p) #round down
ppt = math.ceil(opt/2)
print(opt)
print(ppt)
plist = []

final_cost, final_center = p_center(p, G);

print("final cost: ",final_cost)
print("facilities: ",final_center)

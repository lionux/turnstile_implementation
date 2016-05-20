import networkx as nx
import random
import numpy

#calculates the weight of an edge in Graph F (corresponds to a particular flow) 
#  1 if there is a path from edge.start -> edge.end without edge in the graph
#  0 otherwise
def calculateFlowEdgeWeight(edge, F):
    pass

#calculates the new weights of each edge in graph F (corresponds to a particular flow)
#  for each edge in F:
#    calculateFlowEdgeWeight(edge, F \ edge)
def calculateAllFlowEdgeWeights(F):
    pass

#calculates the weights on each edge in graph G for each flow in F
def calculateGraphEdgeWeights(G, Flows):
    pass

#place a turnstile on the highest weighted edge
#recalculate edge weights for each flow that traverses that edge
def placeTurnstile(G):
    pass

#while all weights on all edges are not 0:
#  placeTurnstile(G)
#  calculateGraphEdgeWeights(G, Flows)
#return G
def approx(G, Flows):
    pass

def main():
    pass

if __name__ == '__main__':main()

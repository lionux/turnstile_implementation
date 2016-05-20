import networkx as nx
import random
import numpy

#calculates the weight of an edge in Graph F (corresponds to a particular flow) 
#Note that e should be removed from F before F is sent into this function
#  n: one for each path from edge.start -> edge.end without e in the graph
#  0: otherwise
def calculateFlowEdgeWeight(e, F):
    return str(list(nx.all_simple_paths(F,e[0],e[1])))
    
#calculates the new weights of each edge in graph F (corresponds to a particular flow)
#  for each edge in F:
#    calculateFlowEdgeWeight(edge, F \ edge)
#    add the weight to the corresponding edge in G
def calculateAllFlowEdgeWeights(G, F):
    for e in F.edges():
        Fnew = F.copy()
        F[e[0]][e[1]]['weight']=calculateFlowEdgeWeight(e,F.remove_edge(e))
        G[e[0]][e[1]]['weight']+=F[e[0]][e[1]]['weight']

#calculates the weights on each edge in graph G for each flow in F
def calculateGraphEdgeWeights(G, Flows):
    for F in Flows:
        calculateAllFlowEdgeWeights(G, F)

#place a turnstile on the highest weighted edge
#recalculate edge weights for each flow that traverses that edge
def placeTurnstile(G):
    pass

#while any weight on an edge is > |flows on that edge|:
#  placeTurnstile(G)
#  Reset edge weights to 0 on G
#  calculateGraphEdgeWeights(G, Flows)
#return G
def approx(G, Flows):
    pass

#print out the edges in the graph
def printGraph(G):
    for e in G.edges(data=True):
        print e

def main():
    G = nx.Graph()
    G.add_edge(1,2)
    G.add_edge(2,3)
    G.add_edge(3,4)
    G.add_edge(2,5)
    G.add_edge(5,4)
    G.add_edge(4,6)
    G.add_edge(6,1)
    for e in G.edges(data=True):
        G[e[0]][e[1]]['turnstile']=False
        G[e[0]][e[1]]['weight']=0

    print "Graph"
    printGraph(G)

    Flow1 = nx.Graph()
    Flow1.add_edge(1,2)
    Flow1.add_edge(2,3)
    Flow1.add_edge(3,4)
    Flow1.add_edge(4,6)
    Flow1.add_edge(6,1)
    for e in Flow1.edges(data=True):
        Flow1[e[0]][e[1]]['turnstile']=False
        Flow1[e[0]][e[1]]['weight']=0

    print "Flow 1"
    printGraph(Flow1)

    Flow2 = nx.Graph()
    Flow2.add_edge(1,2)
    Flow2.add_edge(2,5)
    Flow2.add_edge(5,4)
    Flow2.add_edge(4,6)
    Flow2.add_edge(6,1)
    for e in Flow2.edges(data=True):
        Flow2[e[0]][e[1]]['turnstile']=False
        Flow2[e[0]][e[1]]['weight']=0

    print "Flow 2"
    printGraph(Flow2)

    Test = nx.Graph()
    Test.add_edge(1,2)
    Test.add_edge(2,3)
    Test.add_edge(4,5)
    Test.add_edge(1,3)
    print calculateFlowEdgeWeight((1,2), Test)

if __name__ == '__main__':main()

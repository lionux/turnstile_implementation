import networkx as nx
import random
import numpy

#calculates the weight of an edge in Graph F (corresponds to a particular flow) 
#Note that e should be removed from F before F is sent into this function
#  n: one for each path from edge.start -> edge.end without e in the graph
#  0: otherwise
def calculateFlowEdgeWeight(e, F):
    return len(list(nx.all_simple_paths(F,e[0],e[1])))
    
#calculates the new weights of each edge in graph F (corresponds to a particular flow)
#  for each edge in F:
#    calculateFlowEdgeWeight(edge, F \ edge)
#    add the weight to the corresponding edge in G
def calculateAllFlowEdgeWeights(G, F):
    for e in F.edges():
        Fnew = F.copy()
        Fnew.remove_edge(e[0],e[1])
        F[e[0]][e[1]]['weight'] = calculateFlowEdgeWeight(e,Fnew)
        G[e[0]][e[1]]['weight'] += F[e[0]][e[1]]['weight']

#calculates the weights on each edge in graph G for each flow in F
def calculateGraphEdgeWeights(G, Flows):
    for F in Flows:
        calculateAllFlowEdgeWeights(G, F)

#while any weight on an edge is > |flows on that edge|:
#  placeTurnstile(G)
#  Reset edge weights to 0 on G
#  calculateGraphEdgeWeights(G, Flows)
#return G
def approx(G, Flows):
    done=False
    while not done:
        largest_weight = 0
        largest_weight_edge = ()
        for e in G.edges():
            if G[e[0]][e[1]]['weight'] >= largest_weight:
                largest_weight=G[e[0]][e[1]]['weight']
                largest_weight_edge=e

        #place a turnstile on the largest weighted edge and remove it from the flows
        G[largest_weight_edge[0]][largest_weight_edge[1]]['turnstile']=True
        for f in G[largest_weight_edge[0]][largest_weight_edge[1]]['flows']:
            Flows[f].remove_edge(largest_weight_edge[0], largest_weight_edge[1])

        #reset all weights in G to 0
        for e in G.edges(data=True):
            G[e[0]][e[1]]['weight']=0

        #recalculate edge weights for the flows and graph
        #this can be optimized to only send the flows that were affected by adding a TS to the edge
        calculateGraphEdgeWeights(G, Flows)

        done=True
        for e in G.edges(data=True):
            if G[e[0]][e[1]]['weight'] > len(G[e[0]][e[1]]['flows']):
                done=False
    print "Flow0"
    printGraph(Flows[0])
    print "Flow1"
    printGraph(Flows[1])
    print "Final Graph"
    printGraph(G)

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
        G[e[0]][e[1]]['flows']=[]

    #print "Graph"
    #printGraph(G)

    Flow0 = nx.Graph()
    Flow0.add_edge(1,2)
    Flow0.add_edge(2,3)
    Flow0.add_edge(3,4)
    Flow0.add_edge(4,6)
    Flow0.add_edge(6,1)
    for e in Flow0.edges(data=True):
        Flow0[e[0]][e[1]]['turnstile']=False
        Flow0[e[0]][e[1]]['weight']=0
        G[e[0]][e[1]]['flows'].append(0)

    #print "Flow 1"
    #printGraph(Flow0)

    Flow1 = nx.Graph()
    Flow1.add_edge(1,2)
    Flow1.add_edge(2,5)
    Flow1.add_edge(5,4)
    Flow1.add_edge(4,6)
    Flow1.add_edge(6,1)
    for e in Flow1.edges(data=True):
        Flow1[e[0]][e[1]]['turnstile']=False
        Flow1[e[0]][e[1]]['weight']=0
        G[e[0]][e[1]]['flows'].append(1)

    #print "Flow 2"
    #printGraph(Flow1)

    #print "G again"
    #printGraph(G)

    approx(G, [Flow0, Flow1])

    Test = nx.Graph()
    Test.add_edge(1,2)
    Test.add_edge(2,3)
    Test.add_edge(4,5)
    Test.add_edge(1,3)
    #print calculateFlowEdgeWeight((1,2), Test)

if __name__ == '__main__':main()

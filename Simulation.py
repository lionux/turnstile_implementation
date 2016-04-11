import networkx as nx

#Takes a graph and MST, places turnstiles on edges in graph that aren't in MST
def placeTurnstiles(G, MST):
    for e in G.edges_iter():
        if e not in MST.edges_iter():
            G[e[0]][e[1]]['turnstile'] = True
    return G

def createSubGraphs(G, flows):
    flowMSTs = {}
    for f in flows:
        flowMSTs[f] = nx.Graph()
        for e in G.edges(data=True):
            if f in e[2]['flows']:
                flowMSTs[f].add_edge(e[0], e[1], e[2])
    return flowMSTs

#finds MST for every flow
def MSTPerFlow(G, flows):
    flowMSTs = createSubGraphs(G, flows)
    print "Printing for MSTPerFlow:"
    for f, flowG in flowMSTs.iteritems():
        print "Flow number "+ str(f) + " has edges "+  str(flowG.edges(data = True))
    
#finds MST for every flow with edge weights adjusted for number of flows on that edge
def weightedMSTPerFlow(G, flows):
    flowMSTs = createSubGraphs(G, flows)
    for f, flowG in flowMSTs.iteritems():
        for e in flowG.edges(data=True):
            e[2]['weight'] = len(e[2]['flows'])
    print "Printing for weightedMSTPerFlow:"
    for f, flowG in flowMSTs.iteritems():
        print "Flow number " + str(f) + " has edges "+ str(flowG.edges(data = True))

def main():
    flows = [1,2,3,4]
    G = nx.Graph()
    G.add_nodes_from([1,2,3])
    G.add_edge(1, 2, weight=1, flows=[1, 2], turnstile = False)
    G.add_edge(1, 3, weight=1, flows=[1], turnstile = False)
    G.add_edge(3, 2, weight=1, flows=[1], turnstile = False)
    
    MST =  nx.minimum_spanning_tree(G)
    #print MST.nodes()
    G = placeTurnstiles(G, MST)
    #print G.edges(data=True)
    #for e in G.edges(data=True):
    #    print e[0]
    MSTPerFlow(G, flows)
    weightedMSTPerFlow(G, flows)
    
if __name__ == '__main__':main()

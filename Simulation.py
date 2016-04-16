import networkx as nx


def mergeGraphs(G1, G2):
    G = nx.Graph()
    for e in G1.edges(data=True):
        G.add_edge(e[0], e[1], e[2])
        if (e[0], e[1]) in G2.edges():
            G.edge[e[0]][e[1]]['flows'].append(G2.edge[e[0]][e[1]]['flows'][0])
    return G

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
def MSTPerFlow(input_graph, flows):
    G = input_graph.copy()
    flowMSTs = createSubGraphs(G, flows)
    print "Printing for MSTPerFlow:"

    print "FLOW MST LEN: "+str(len(flowMSTs))
    for f, flowG in flowMSTs.iteritems():
        MST = nx.minimum_spanning_tree(flowG)
        flowMSTs[f] = placeTurnstiles(flowG, MST)

    tsCount = 0
    for f, flowG in flowMSTs.iteritems():
        for e in flowG.edges(data = True):
            if e[2]['turnstile'] == True:
                G[e[0]][e[1]]['turnstile'] = True
                tsCount = tsCount+1

    print "Turnstiles: "+str(tsCount)
    for e in G.edges(data=True):
        print "Edge ("+ str(e[0])+", " + str(e[1]) + ") has status "+  str(e[2])
    
#finds MST for every flow with edge weights adjusted for number of flows on that edge
def weightedMSTPerFlow(input_graph, flows):
    G = input_graph.copy()
    flowMSTs = createSubGraphs(G, flows)
    print "FLOW MST LEN: "+str(len(flowMSTs))
    for f, flowG in flowMSTs.iteritems():
        for e in flowG.edges(data=True):
            e[2]['weight'] = len(e[2]['flows'])
            G[e[0]][e[1]]['weight'] = len(e[2]['flows'])
    for f in range(1, len(flowMSTs) + 1):
        MST = nx.minimum_spanning_tree(flowMSTs[f])
        flowMSTs[f] = placeTurnstiles(flowMSTs[f], MST)
        for e in flowMSTs[f].edges(data=True):
            if e[2]['turnstile'] == True:
                #print str(e[2])
                for i in range(f, len(flowMSTs)+1):
                    if (e[0], e[1]) in flowMSTs[i].edges():
                        flowMSTs[i].edge[e[0]][e[1]]['weight'] = flowMSTs[i].edge[e[0]][e[1]]['weight'] + 1
                G.edge[e[0]][e[1]]['weight'] = G.edge[e[0]][e[1]]['weight'] + 1

    tsCount = 0
    for f, flowG in flowMSTs.iteritems():
        for e in flowG.edges(data = True):
            if e[2]['turnstile'] == True:
                G[e[0]][e[1]]['turnstile'] = True
                tsCount = tsCount+1

    print "Printing for weightedMSTPerFlow:"
    print "Turnstiles: "+str(tsCount)
    for e in G.edges(data=True):
        print "Edge ("+ str(e[0])+", " + str(e[1]) + ") has status "+  str(e[2])

    #for f, flowG in flowMSTs.iteritems():
    #    print "Flow number " + str(f) + " has edges "+ str(flowG.edges(data = True))

def main():
    flows = [1,2]
    G = nx.Graph()
    #G.add_nodes_from([1,2,3,4,5,6])
    #G.add_edge(1, 2, weight=1, flows=[1, 2], turnstile = False)
    #G.add_edge(2, 3, weight=1, flows=[1], turnstile = False)
    #G.add_edge(2, 4, weight=1, flows=[2], turnstile = False)
    #G.add_edge(3, 5, weight=1, flows=[1], turnstile = False)
    #G.add_edge(4, 5, weight=1, flows=[2], turnstile = False)
    #G.add_edge(5, 6, weight=1, flows=[1, 2], turnstile = False)
    #G.add_edge(6, 1, weight=1, flows=[1, 2], turnstile = False)
    G.add_nodes_from([1,2,3,4,5,6,7,8])
    G.add_edge(1, 2, weight=1, flows=[1], turnstile=False)
    G.add_edge(1, 3, weight=1, flows=[1], turnstile=False)
    G.add_edge(2, 3, weight=1, flows=[1,2], turnstile=False)
    G.add_edge(2, 4, weight=1, flows=[2], turnstile=False)
    G.add_edge(3, 5, weight=1, flows=[2], turnstile=False)
    G.add_edge(4, 5, weight=1, flows=[2,3], turnstile=False)
    G.add_edge(4, 6, weight=1, flows=[3], turnstile=False)
    G.add_edge(5, 7, weight=1, flows=[3], turnstile=False)
    G.add_edge(6, 7, weight=1, flows=[3,4], turnstile=False)
    G.add_edge(6, 8, weight=1, flows=[4], turnstile=False)
    G.add_edge(7, 8, weight=1, flows=[4], turnstile=False)

    #print MST.nodes()
    #print G.edges(data=True)
    #for e in G.edges(data=True):
    #    print e[0]
    #MSTPerFlow(G, flows)
    #print "\n"
    #weightedMSTPerFlow(G, flows)
    #print "\n\n"
    G1 = nx.fast_gnp_random_graph(5, .8, seed=None, directed=False)
    for e in G1.edges(data=True):
        G1.edge[e[0]][e[1]]['flows'] = [1]
        G1.edge[e[0]][e[1]]['turnstile'] = False
        G1.edge[e[0]][e[1]]['weight'] = 1

    G2 = nx.fast_gnp_random_graph(5, .8, seed=None, directed=False)
    for e in G2.edges(data=True):
        G2.edge[e[0]][e[1]]['flows'] = [2]
        G2.edge[e[0]][e[1]]['turnstile'] = False
        G2.edge[e[0]][e[1]]['weight'] = 1

    merged = mergeGraphs(G1, G2)
    
    #for e in merged.edges(data=True):
    #    print str(e)
    MSTPerFlow(merged, flows)
    print "\n"
    weightedMSTPerFlow(merged, flows)

if __name__ == '__main__':main()

import networkx as nx
import random

#merges two graphs together
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
        if e not in MST.edges():
            G.edge[e[0]][e[1]]['turnstile'] = True
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
    #print "Printing for MSTPerFlow:"

    #print "FLOW MST LEN: "+str(len(flowMSTs))
    for f, flowG in flowMSTs.iteritems():
        for e in flowG.edges(data=True):
            flowG.edge[e[0]][e[1]]['weight'] = random.randint(1, 10)
        
        MST = nx.minimum_spanning_tree(flowG)
        flowMSTs[f] = placeTurnstiles(flowG, MST)
        #for e in flowMSTs[f].edges(data=True):
        #    print str(f) + " "+str(e)

    tsCount = 0
    for f, flowG in flowMSTs.iteritems():
        for e in flowG.edges(data = True):
            if e[2]['turnstile'] == True:
                if G.edge[e[0]][e[1]]['turnstile'] == False:
                    G.edge[e[0]][e[1]]['turnstile'] = True
                    tsCount = tsCount+1
    return tsCount

    
#finds MST for every flow with edge weights adjusted for number of flows on that edge
def weightedMSTPerFlow(input_graph, flows):
    G = input_graph.copy()
    flowMSTs = createSubGraphs(G, flows)
    #print "FLOW MST LEN: "+str(len(flowMSTs))
    for f, flowG in flowMSTs.iteritems():
        for e in flowG.edges(data=True):
            e[2]['weight'] = len(e[2]['flows'])
            G[e[0]][e[1]]['weight'] = len(e[2]['flows'])
    for f in range(1, len(flowMSTs) + 1):
        MST = nx.minimum_spanning_tree(flowMSTs[f], weight="weight")
        flowMSTs[f] = placeTurnstiles(flowMSTs[f], MST)
        for e in flowMSTs[f].edges(data=True):
            if e[2]['turnstile'] == True:
                for i in range(f, len(flowMSTs)+1):
                    if (e[0], e[1]) in flowMSTs[i].edges():
                        flowMSTs[i].edge[e[0]][e[1]]['weight'] = flowMSTs[i].edge[e[0]][e[1]]['weight'] + 1
                G.edge[e[0]][e[1]]['weight'] = G.edge[e[0]][e[1]]['weight'] + 1

    tsCount = 0
    for f, flowG in flowMSTs.iteritems():
        for e in flowG.edges(data = True):
            if e[2]['turnstile'] == True:
                if G.edge[e[0]][e[1]]['turnstile'] == False:
                    G.edge[e[0]][e[1]]['turnstile'] = True
                    tsCount = tsCount+1
    return tsCount

def main():
    ##############
    # PARAMETERS #
    ##############

    #Number of desired simulations
    number_of_simulations = 100

    #Graph parameters
    number_of_vertices = 10
    edge_probability = .5
    flows = [1,2,3]

    #Variables for averaging performance
    edge_sum = 0
    weighted_ts_sum = 0
    unweighted_ts_sum = 0

    for i in range(0, number_of_simulations):
        G1 = nx.fast_gnp_random_graph(number_of_vertices, edge_probability, seed=None, directed=False)
        for e in G1.edges(data=True):
            G1.edge[e[0]][e[1]]['flows'] = [1]
            G1.edge[e[0]][e[1]]['turnstile'] = False
            G1.edge[e[0]][e[1]]['weight'] = 1

        G2 = nx.fast_gnp_random_graph(number_of_vertices, edge_probability, seed=None, directed=False)
        for e in G2.edges(data=True):
            G2.edge[e[0]][e[1]]['flows'] = [2]
            G2.edge[e[0]][e[1]]['turnstile'] = False
            G2.edge[e[0]][e[1]]['weight'] = 1

        #G3 = nx.fast_gnp_random_graph(number_of_vertices, edge_probability, seed=None, directed=False)
        #for e in G3.edges(data=True):
        #    G3.edge[e[0]][e[1]]['flows'] = [3]
        #    G3.edge[e[0]][e[1]]['turnstile'] = False
        #    G3.edge[e[0]][e[1]]['weight'] = 1

        merged = mergeGraphs(G1, G2)
        #merged = mergeGraphs(merged, G3)
    
        unweighted_ts_sum += MSTPerFlow(merged, flows)
        weighted_ts_sum += weightedMSTPerFlow(merged, flows)
        edge_sum += len(merged.edges())

    #with open("simResults3Flows10Nodes.txt", "a") as f:
    print "Avg Number of Edges: "+str(edge_sum/number_of_simulations)+", Avg Number of TS Unweighted: "+str(unweighted_ts_sum/number_of_simulations) +", Avg Number of TS Weighted: "+str(weighted_ts_sum/number_of_simulations)

if __name__ == '__main__':main()

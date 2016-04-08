import networkx as nx

def main():
    G = nx.Graph()
    G.add_nodes_from([1,2,3])
    G.add_edge(1, 2, weight=1, flow=["red","blue"], turnstile = False)
    G.add_edge(1, 3, weight=2, flow=["red"], turnstile = False)
    G.add_edge(3, 2, weight=1, flow=["red"], turnstile = False)
    
    MST =  nx.minimum_spanning_tree(G)
    print MST.edges(data=True)
    
    for e in G.edges_iter():
        print e
        if e not in MST.edges_iter():
            G[e[0]][e[1]]['turnstile'] = True

    print G.edges(data=True)

if __name__ == '__main__':main()

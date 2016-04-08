import networkx as nx
def main():
    G = nx.DiGraph()
    G.add_nodes_from([1,2,3])
    G.add_edge(1, 2, weight=1, flow=["red","blue"])
    G.add_edge(1, 3, weight=2, flow=["red"])
    G.add_edge(3, 2, weight=1, flow=["red"])
    print G.edges(data=True)


if __name__ == '__main__':main()

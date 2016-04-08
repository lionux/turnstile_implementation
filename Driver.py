import Graph

def main():
    graph_init = {
        "a": ["b", "g"],
        "b": ["a", "c"],
        "c": ["a", "b"],
        "d": ["c"],
        "e": ["d"],
        "f": ["e"],
        "g": ["b"]
        }
    weights_init = {
        ("a", "b"): 1,
        ("a", "g"): 2,
        ("b", "c"): 1,
        ("b", "a"): 4, 
        ("c", "a"): 2,
        ("c", "b"): 1,
        ("d", "c"): 1,
        ("e", "d"): 4,
        ("f", "e"): 2, 
        ("g", "b"): 1
        }

    g = Graph.Graph(graph_init, weights_init)

    g.print_graph()



if __name__=='__main__':main()

# This program is the Graph class for the turnstile problem
# @author SAM MICKA

class Graph(object):
    def __init__(self, graph = {}, weights = {}):
        self.graph = graph
        self.weights = weights

    def vertices(self):
        return list(self.graph.keys())

    def edges(self):
        edges = []
        for vertex in self.graph:
            for neighbour in self.graph[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def weights(self):
        return self.weights

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def get_neighbors(self, vertex):
        return self.graph[vertex]
    
    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 in self.graph:
            self.graph[vertex1].append(vertex2)
        else:
            self.graph[vertex1] = [vertex2]
        if vertex2 not in self.graph:
            self.add_vertex(vertex2)
        self.weights[(vertex1, vertex2)] = weight

    def print_graph(self):
        for vertex in self.graph.keys():
            print "Vertex: "+vertex
            for neighbor in self.graph[vertex]:
                print "  Neighbor of "+vertex+": "+neighbor+" has weight "+str(self.weights[(vertex,neighbor)])



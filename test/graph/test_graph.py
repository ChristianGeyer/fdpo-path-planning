import pytest
from graph.graph import Graph, Edge

def test_simple_graph():
    # create graph object
    g = Graph()
    # known graph
    nodes = ["A", 0, 1, 2, 3, "B"]
    neighbors = {"A" : [0, 2],
                 0   : [1],
                 1   : [2, "B"],
                 2   : [1, 3],
                 3   : ["B"],
                 "B" : [3]}
    dist_AB = 4
    path_AB = ["A", 0, 1, "B"]
    # add edges to graph
    g.add_edge("A", 0, 1.0)
    g.add_edge("A", 2, 4.0)
    g.add_edge(0, 1, 1.0)
    g.add_edge(1, 2, 1.0)
    g.add_edge(1, "B", 2.0)
    g.add_edge(2, 1, 1.0)
    g.add_edge(2, 3, 1.0)
    g.add_edge(3, "B", 1.0)
    g.add_edge("B", 3, 1.0)
    # compute shortest distances from A
    dist, prev = g.shortest_distances("A")
    print(f"shortest distances {dist}")
    print(f"parent nodes {prev}")
    # compute shortest path from A to B
    path = g.shortest_path("A", "B", dist, prev)
    print(f"shortest path {path}")

    # check nodes
    assert set(g.nodes()) == set(nodes)
    # check neighbors
    for node in g.nodes():
        graph_edges = g.neighbors(node)
        graph_neighbors = [e.node_to for e in graph_edges]
        assert set(graph_neighbors) == set(neighbors[node])
    # check shortest distance
    assert dist["B"] == dist_AB
    # check shortest path
    assert path == path_AB

def test_unreachable_graph():
    # create graph object
    g = Graph()
    # known results
    dist_expected = {"A" : 0.0,
                     0   : 1,
                     1   : 2,
                     2   : 3}
    
    prev_expected = {"A" : None,
                     0   : "A",
                     1   : 0,
                     2   : 1}
    path_A2 = ["A", 0, 1, 2]
    
    # add edges to graph
    g.add_edge("A", 0, 1.0)
    g.add_edge("A", 2, 4.0)
    g.add_edge(0, 1, 1.0)
    g.add_edge(1, 2, 1.0)
    g.add_edge(3, 2, 1.0)
    g.add_edge(3, "B", 1.0)

    # compute shortest distances from A
    dist, prev = g.shortest_distances("A")

    assert dist == dist_expected
    assert prev == prev_expected

    # compute shortest path from A to B
    path = g.shortest_path("A", "B", dist, prev)

    assert path is None

    # compute shortest path from A to 2
    path = g.shortest_path("A", 2, dist, prev)

    assert path == path_A2



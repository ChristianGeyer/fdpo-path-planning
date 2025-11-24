from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, List, Tuple, Optional
import heapq

NodeId = Hashable  # alias for anything usable as a node key (str, int, etc.)


@dataclass
class Edge:
    node_to: NodeId
    weight: float


class Graph:
    
    # --- constructor -----------------------------------------------------
    def __init__(self) -> None:
        # save adjacency list as a dict (node -> list of outgoing edges)
        self._adj: Dict[NodeId, List[Edge]] = {}

    # --- add nodes and edges --------------------------------------------

    def add_node(self, node: NodeId) -> None:
        # add node to the dict (node -> list of outgoing edges)
        if node not in self._adj:
            self._adj[node] = [] # empty list of outgoing edges

    def add_edge(
        self,
        node_from: NodeId,
        node_to: NodeId,
        weight: float,
        bidirectional: bool = False,
    ) -> None:
        # ensure nodes are in the graph
        self.add_node(node_from)
        self.add_node(node_to)

        # add edge to the graph
        self._adj[node_from].append(Edge(node_to=node_to, weight=weight))

        if bidirectional:
            self._adj[node_to].append(Edge(node_to=node_from, weight=weight))
    
    # --- access neighbor and node lists ----------------------------------
    def neighbors(self, node: NodeId) -> List[Edge]:
        # return list of outgoing edges
        # return [] if node is not in the graph
        return self._adj.get(node, [])

    def nodes(self) -> List[NodeId]:
        # return list of all nodes
        return list(self._adj.keys())

    # --- shortest paths --------------------------------------------------

    def shortest_distances(self, 
                           source: NodeId) -> Tuple[Dict[NodeId, float], Dict[NodeId, Optional[NodeId]]]:
        # compute a dict with shortest distance from source to each node
        # all non-initialized distances are set to infinity
        dist: Dict[NodeId, float] = {source: 0.0}

        # save the predecessor node along the shortest path
        prev: Dict[NodeId, Optional[NodeId]] = {source: None} # source node has no predecessor
        
        # tiebreaker to avoid NodeId comparison
        counter = 0
        # heapq is a min-heap
        # it uses a python list as the underlying data structure 
        # we will save (distance, node) tuples and keep the shortest distance at the top
        pq: List[Tuple[float, int, NodeId]] = [(0.0, counter, source)]
        counter += 1

        while pq:
            # get the node (node_from) with the smallest distance (d)
            d_from, _, node_from = heapq.heappop(pq)
            # check if this node was already reached
            if d_from > dist.get(node_from, float("inf")):
                continue  # ignore outdated node

            # iterate all neighbors
            for edge in self.neighbors(node_from):
                node_to = edge.node_to # extract neighbor node
                d_to = d_from + edge.weight # compute total distance to neighbor
                # check if a shorter path to neighbor was found
                if d_to < dist.get(node_to, float("inf")): 
                    dist[node_to] = d_to # update distance
                    heapq.heappush(pq, (d_to, counter, node_to)) # add to priority queue
                    counter += 1
                    # save predecessor
                    prev[node_to] = node_from
        # return dict with shortest distances from source to all nodes
        # and dict with predecessors
        return dist, prev

    def shortest_path(
            self, 
            start_node: NodeId, 
            end_node: NodeId,
            dist: Dict[NodeId, float],
            prev: Dict[NodeId, Optional[NodeId]]) -> Optional[List[NodeId]]:
        
        # check inputs
        if dist is None or prev is None:
            return None
        # check if end_node is reachable from start_node
        if end_node not in dist:
            return None
        # check if start node has distance 0
        if dist[start_node] != 0:
            return None

        # rebuild path from end_node back to start_node
        path: List[NodeId] = []
        # start at end_node
        curr: NodeId = end_node
        while curr != start_node:
            path.append(curr)
            curr = prev[curr]
        path.append(start_node)
        path.reverse()
        return path
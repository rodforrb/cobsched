'''
Scheduling algorithm implementation
Ben Rodford
April 2019
'''

'''
node v1:
    data
    outbound edges
        (v2, capacity, flow)
    inbound edges
        (v0, capacity)?
        used for residual graph
'''


# https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm

import collections
 
# This class represents a directed graph using adjacency matrix representation
class Graph:
  
    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)
  
    def BFS(self, s, t, parent):
        '''Returns true if there is a path from source 's' to sink 't' in
        residual graph. Also fills parent[] to store the path '''

        # Mark all the vertices as not visited
        visited = [False] * (self.ROW)
         
        # Create a queue for BFS
        queue = collections.deque()
         
        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True
         
        # Standard BFS Loop
        while queue:
            u = queue.popleft()
         
            # Get all adjacent vertices's of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if (visited[ind] == False) and (val > 0):
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
 
        # If we reached sink in BFS starting from source, then return
        # true, else false
        return visited[t]
             
    # Returns the maximum flow from s to t in the given graph
    def EdmondsKarp(self, source, sink):
 
        # This array is filled by BFS and to store path
        parent = [-1] * (self.ROW)
 
        max_flow = 0 # There is no flow initially
 
        # Augment the flow while there is path from source to sink
        while self.BFS(source, sink, parent):
 
            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
 
            # Add path flow to overall flow
            max_flow += path_flow
 
            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
 
        return max_flow


def edges_to_graph(edges, size):
    
    graph = []
    for i in range(size):
        graph.append([0]*size)

    for u, v, c in edges:
        graph[u][v] = c

    return graph

def max_flow_edges(edges):
    # highest numbered node
    size = max(edges, key=lambda e: e[1])[1] + 1
    
    G = Graph(edges_to_graph(edges, size))

    G.EdmondsKarp(0, 3)
    residual = G.graph

    max_flow_edges = []
    for u,v,c in edges:
        max_flow_edges.append( (u, v, residual[v][u]) )

    return max_flow_edges



# (u, v, capacity)
edges = [ 
        (0, 1, 20),
        (0, 2, 10),
        (1, 2, 20),
        (1, 3, 10),
        (2, 3, 20)
        ]


print(max_flow_edges(edges))





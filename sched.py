'''
Scheduling algorithm implementation
Ben Rodford
April 2019
'''
import collections
import csv

# https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm

 
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

'''
expects a csv file
'''
def avail_from_file(filename):
    with open(filename, 'r') as filein:
        lines = csv.reader(filein)
        
        for line in lines:
            for i in line:
                print(i, type(i))


'''
avail should be a list of tuples formatted:
    (name, (locations,), (days,))
    where locations and days are tuples of (0 or 1) booleans
    days is made of 7 3-tuples representing availability for
        morning/daytime/evening for each day
'''
def avail_to_edges(avail):
    # a set of (u, v, capacity)
    # name becomes u
    # every timeslot becomes separate v
    # name -> slot capacities = 1 TODO number of hours?
    # source -> name capacities = max allocation per person
    # slot -> sink capacities = inf
    edges = []

    # source node is 0
    # sink node is 1
    # remaining nodes start at 2
    node_index = 2

    name_to_node = {}
    node_to_name = {}

    for name, locations, days in avail:
        if name not in name_to_node.keys():
            # person has no edges yet
            name_to_node[name] = node_index
            node_index += 1

            #edges.append(name_to_node[name], #TODO hours

        for l in locations:
            for d in days:
                for timeslot in d:
                    #TODO make node for d
                    #edges.append(u,v,c)
        edges.append()
        
    pass

# reverse the conversion
def edges_to_avail(edges):
    pass


# (u, v, capacity)
edges = [ 
        (0, 1, 20),
        (0, 2, 10),
        (1, 2, 20),
        (1, 3, 10),
        (2, 3, 20)
        ]



#print(max_flow_edges(edges))


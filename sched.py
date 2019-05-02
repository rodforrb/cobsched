'''
Scheduling algorithm implementation
Ben Rodford
April 2019
'''
import collections
import csv
from dataclasses import dataclass
from collections import defaultdict
from random import shuffle


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

@dataclass
class Avail:
    name : str
    hours : int
    timeslots : tuple

@dataclass
class Shift:
    # specific to time and location
    timeslot : str
    staff : int

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

    G.EdmondsKarp(0, 1)
    residual = G.graph

    max_flow_edges = []
    for u,v,c in edges:
        max_flow_edges.append( (u, v, residual[v][u]) )

    return max_flow_edges

'''
expects a csv file
'''
def avail_from_file(filename):
    avail = []
    with open(filename, 'r') as filein:
        lines = csv.reader(filein)

        titles = lines.__next__()
        for line in lines:

            ts = [] # timeslots
            for l, location in enumerate(line[2:5]):
                if location == "1":
                    for t, timeslot in enumerate(line[5:]):
                        if timeslot == "1":
                            ts.append(titles[l+2] + titles[t+5])
            shuffle(ts)
            avail.append(Avail(line[0],     # name
                           int(line[1]),    # hours
                           ts.copy()))      # randomized timeslots
    return avail

def shifts_from_file(filename):
    shifts = []

    with open(filename, 'r') as filein:
            lines = csv.reader(filein)
            titles = lines.__next__()[1:]

            for line in lines:
                for i, staff in enumerate(line[1:]):
                    shifts.append(Shift(line[0]+titles[i], staff))
    return shifts

'''
avail : Avail
    where locations and days are tuples of (0 or 1) booleans
    days is made of 7 3-tuples representing availability for
        morning/daytime/evening for each day
shifts : Shifts
returns schedule of type dict{str : list[shift]} ,
    contracts of type dict{shift : list[str]}
'''
def run_graph(avail, shifts):
    # edges is a list of (u, v, capacity) tuples, derived as follows:
    # name becomes u
    # every timeslot becomes a separate v
    # name -> slot capacities = 1 # TODO could do number of hours?
    # source -> name capacities = max allocation per person
    # slot -> sink capacities = inf
    edges = []

    # source node is 0
    # sink node is 1
    # remaining nodes start at 2
    node_index = 2

    name_to_node = {}
    node_to_name = {}
    node_to_shift = {}

    # reducing the problem to a flow diagram
    # adding shift nodes and edges
    for s in shifts:
        if s.timeslot not in name_to_node:
            name_to_node[s.timeslot] = node_index
            node_to_shift[node_index] = s.timeslot

        # attach timeslot to sink
        edges.append((name_to_node[s.timeslot], 1, int(s.staff)))

        node_index += 1 

    # adding person nodes and edges
    for person in avail:
        # person has no node yet so make them one
        name_to_node[person.name] = node_index
        node_to_name[node_index] = person.name
        # attach source to person
        edges.append((0, name_to_node[person.name], int(person.hours)))

        for ts in person.timeslots:
            # attach person to timeslot
            edges.append((node_index, name_to_node[ts], 1))

        node_index += 1

    # solve the flow network
    max_flow = max_flow_edges(edges)

    # un-reducing back to a schedule
    schedule = defaultdict(list) # {person : [shifts]}
    contracts = defaultdict(list) # {shift : [people]}
    for u,v,c in max_flow:
        # check if node is a person
        if u in node_to_name:
            # check if person is assigned to that shift
            if c > 0:
                contracts[node_to_name[u]].append(node_to_shift[v])
                schedule[node_to_shift[v]].append(node_to_name[u])
    
    return schedule, contracts

def schedule_to_file(schedule, filename):
    # minimum lines for times
    padding = (6, 6, 6)
    with open(filename, 'w') as fileout:
        # columns are going to be written horizontally, then transposed
        lines = []
        for location in ('Ald', 'Tans', 'Cent'):
            lines.append([location])
            for day in ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'):
                line = [day]
                for time in (1, 2, 3):
                    line.append(['Morning', 'Daytime', 'Evening'][time-1])

                    timeslot = location+str(time)+day
                    rows = 0
                    for person in schedule[timeslot]:
                        line.append(person)
                        rows += 1

                    while rows < padding[time-1]:
                        line.append('')
                        rows += 1

                    # minimum 1 empty line
                    line.append('')

                lines.append(line)

        # transpose the 2d list/matrix and write
        # the width becomes the number of lines
        width = len(max(lines, key=len))
        print("width:", width)

        for i in range(width):

            for j in range(len(lines)):
                # the row still has elements to add
                if i < len(lines[j]):
                    fileout.write(lines[j][i] + ',')
                else:
                    # otherwise we need to pad the column
                    fileout.write(',')


            fileout.write('\n')


avail = avail_from_file("avail.csv")
shifts = shifts_from_file("shifts.csv")

schedule, contracts = run_graph(avail, shifts)

print(schedule)

schedule_to_file(schedule, "schedule.csv")

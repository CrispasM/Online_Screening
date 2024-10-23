from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices (airports)
        self.graph = defaultdict(list)  # Default dictionary to store graph
        self.reverse_graph = defaultdict(list)  # To store reverse graph for SCC
        self.nodes = set()  # To store all nodes (airports)
    
    # Function to add a one-way flight (directed edge)
    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.reverse_graph[v].append(u)
        self.nodes.add(u)
        self.nodes.add(v)

    # Helper function for Kosaraju's algorithm (SCC detection)
    def _dfs(self, v, visited, stack=None):
        visited[v] = True
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                self._dfs(neighbor, visited, stack)
        if stack is not None:
            stack.append(v)

    # Reversed DFS for Kosaraju's second pass
    def _reverse_dfs(self, v, visited, component):
        visited[v] = True
        component.append(v)
        for neighbor in self.reverse_graph[v]:
            if not visited[neighbor]:
                self._reverse_dfs(neighbor, visited, component)

    # Function that finds and returns all SCCs in the graph
    def find_sccs(self):
        stack = []
        visited = {v: False for v in self.nodes}  # Initialize visited with all airports
        
        # First pass: Populate stack with finishing times
        for v in self.nodes:
            if not visited[v]:
                self._dfs(v, visited, stack)
        
        # Second pass: Reverse DFS based on stack order
        visited = {v: False for v in self.nodes}  # Reinitialize visited
        sccs = []
        
        while stack:
            v = stack.pop()
            if not visited[v]:
                component = []
                self._reverse_dfs(v, visited, component)
                sccs.append(component)
        
        return sccs

    # Function to find the minimum number of routes to add
    def min_routes_to_connect(self, start):
        sccs = self.find_sccs()
        
        # Build compressed graph from SCCs
        scc_graph = defaultdict(set)
        scc_map = {}  # Map each node to its SCC index
        
        for idx, component in enumerate(sccs):
            for node in component:
                scc_map[node] = idx
        
        # Create new SCC graph
        for u in self.graph:
            for v in self.graph[u]:
                if scc_map[u] != scc_map[v]:
                    scc_graph[scc_map[u]].add(scc_map[v])
        
        # Find SCCs with zero in-degree
        in_degree = {i: 0 for i in range(len(sccs))}
        for u in scc_graph:
            for v in scc_graph[u]:
                in_degree[v] += 1
        
        # Count number of SCCs with zero in-degree that are not the start SCC
        start_scc = scc_map[start]
        zero_in_degree_count = sum(1 for i in in_degree if in_degree[i] == 0 and i != start_scc)
        
        return zero_in_degree_count

# Sample instantiation using the image data:
g = Graph(vertices=15)  # Assuming the image shows 15 airports

# Adding edges as per the image (e.g., DSM -> ORD, ORD -> BGI, etc.)
g.add_edge('DSM', 'ORD')
g.add_edge('ORD', 'BGI')
g.add_edge('BGI', 'LGA')
g.add_edge('LGA', 'JFK')
g.add_edge('JFK', 'HND')
g.add_edge('HND', 'ICN')
g.add_edge('EWR', 'HND')
g.add_edge('SFO', 'SAN')
g.add_edge('SAN', 'EYW')
g.add_edge('EYW', 'SFO')
g.add_edge('SFO', 'LHR')
g.add_edge('LHR', 'EYW')
g.add_edge('CDG', 'BUD')
g.add_edge('DEL', 'DOH')
g.add_edge('TLV', 'DEL')
g.add_edge('DEL', 'CDG')
g.add_edge('SIN', 'CDG')
g.add_edge('SIN', 'DEL')

# Ensure all nodes are added even if they don't have outgoing edges
all_airports = ['DSM', 'ORD', 'BGI', 'LGA', 'JFK', 'HND', 'ICN', 'EWR', 'SFO', 'SAN', 'EYW', 'LHR', 'CDG', 'BUD', 'DOH', 'TLV', 'DEL', 'SIN']
for airport in all_airports:
    g.nodes.add(airport)

# Calculate minimum additional routes needed, starting from 'DSM'
start_airport = 'DSM'
print(g.min_routes_to_connect(start_airport))

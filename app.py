from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices  
        self.graph = defaultdict(list) 
        self.reverse_graph = defaultdict(list) 
        self.nodes = set()  
    
    # Function to add a one-way flight (directed edge)
    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.reverse_graph[v].append(u)
        self.nodes.add(u)
        self.nodes.add(v)

 
    def _dfs(self, v, visited, stack=None):
        visited[v] = True
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                self._dfs(neighbor, visited, stack)
        if stack is not None:
            stack.append(v)


    def _reverse_dfs(self, v, visited, component):
        visited[v] = True
        component.append(v)
        for neighbor in self.reverse_graph[v]:
            if not visited[neighbor]:
                self._reverse_dfs(neighbor, visited, component)

    # Function that finds and returns all SCCs in the graph
    def find_sccs(self):
        stack = []
        visited = {v: False for v in self.nodes}  
        

        for v in self.nodes:
            if not visited[v]:
                self._dfs(v, visited, stack)
        
       
        visited = {v: False for v in self.nodes}  
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
        
    
        scc_graph = defaultdict(set)
        scc_map = {} 
        
        for idx, component in enumerate(sccs):
            for node in component:
                scc_map[node] = idx
        

        for u in self.graph:
            for v in self.graph[u]:
                if scc_map[u] != scc_map[v]:
                    scc_graph[scc_map[u]].add(scc_map[v])
        
  
        in_degree = {i: 0 for i in range(len(sccs))}
        for u in scc_graph:
            for v in scc_graph[u]:
                in_degree[v] += 1
        
  
        start_scc = scc_map[start]
        zero_in_degree_count = sum(1 for i in in_degree if in_degree[i] == 0 and i != start_scc)
        
        return zero_in_degree_count


g = Graph(vertices=15) 

# Adding edges 
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


all_airports = ['DSM', 'ORD', 'BGI', 'LGA', 'JFK', 'HND', 'ICN', 'EWR', 'SFO', 'SAN', 'EYW', 'LHR', 'CDG', 'BUD', 'DOH', 'TLV', 'DEL', 'SIN']
for airport in all_airports:
    g.nodes.add(airport)

 
start_airport = 'DSM'
print(g.min_routes_to_connect(start_airport))

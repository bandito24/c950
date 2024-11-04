from collections import namedtuple

class DeliveryVertex:
    def __init__(self, address_label):
        self.address_label = address_label
        
class DeliveryGraph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}
        self.vertex_dict = {}
        
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []
        self.vertex_dict[new_vertex.address_label] = new_vertex
        
    def add_directed_edge(self, from_vertex, to_vertex, weight):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)
    
    def add_undirected_edge(self, from_vertex, to_vertex, weight):
        self.add_directed_edge(from_vertex, to_vertex, weight)
        self.add_directed_edge(to_vertex, from_vertex, weight)
        
    def find_vertex(self, address_label):
        for vertex in self.adjacency_list.keys():
            if vertex.address_label == address_label:
                return vertex
        raise ValueError(f"Vertex with address label '{address_label}' not found.")
    
    def nearest_neighbor_route(self, start_vertex, package_list, k=16):
        Delivery = namedtuple('Delivery', ['package', 'distance', 'address'])
        visited = set()
        current_vertex = start_vertex
        assigned_packages = []
        assignments = {}
        for package in package_list:
            if package.destination_vertex in assignments:
                assignments[package.destination_vertex].append(package)
            else:
                assignments[package.destination_vertex] = [package]
        all_destinations = list(assignments.keys())
        
        while current_vertex and k > len(assigned_packages):
            min_route = float('inf')
            next_vertex = None
            vertices = list(filter(lambda x: x in all_destinations, self.adjacency_list[current_vertex]))
            for vertex in vertices:
                direction_edge = self.edge_weights[(current_vertex, vertex)]
                if direction_edge < min_route and vertex not in visited:
                    min_route = direction_edge
                    next_vertex = vertex
            if next_vertex == None:
                return assigned_packages
            visited.add(next_vertex)
            next_package = assignments[next_vertex]
            assigned_packages.append(Delivery(package=next_package, distance=min_route, address=next_vertex.address_label))
            current_vertex = next_vertex
         

        return assigned_packages
            
             
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        # while current_vertex and (k is None or len(route) < k):
        #     visited.add(current_vertex)
        #     neighbors = self.adjacency_list[current_vertex]
        #     if not neighbors:
        #         break  # No more neighbors to visit

        #     # Find the nearest neighbor
        #     next_vertex = None
        #     min_distance = float('inf')

        #     for neighbor in neighbors:
        #         if neighbor not in visited:
        #             distance = self.edge_weights.get((current_vertex, neighbor), float('inf'))
        #             if distance < min_distance:
        #                 min_distance = distance
        #                 next_vertex = neighbor
            
        #     if next_vertex is None:
        #         break  # No unvisited neighbors left

        #     route.append(next_vertex.address_label)
        #     current_vertex = next_vertex

        # return route
        



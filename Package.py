#Contains all relevant data for delivery. Destination Vertex attribute
# references a vertex in the DeliveryGraph.
# status attribute is 'delivered', 'hold', or 'ready'
class Package:
    def __init__(self, id, address, city, state, zip_code, deadline, weight, status="ready", assigned_truck = None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.assigned_truck = assigned_truck
        self.deadline = deadline
        self.destination_vertex = None
        
    def __lt__(self, other):
        if self.deadline == 'EOD':
            return False if other.deadline == 'EOD' else True
        if other.deadline == 'EOD':
            return False
        return self.deadline < other.deadline
#Adds a package to priority list if the deadline is not 'EOD'. Priority list will
#always be the first destinations in delivery unless there are no ready packages here
class PackageList:
    def __init__(self):
        self.index = 0
        self.non_priority_list = {}
        self.priority_list = {}
    
    def add_package(self, order):
        if order.deadline != 'EOD':
            self.priority_list[order.id] = order
        else:
            self.non_priority_list[order.id] = order
            
    def set_ready(self, ids = []):
        if ids is None:
            self.set_all_ready
        else:
            all_packages = self.all_packages
            for id in ids:
                all_packages[id][status] = 'ready'  
    def set_all_ready(self):
        all_orders = list(self.priority_list.values()) + list(self.non_priority_list.values())
        for order in all_orders:
            if order.status != 'delivered':
                order.status = 'ready'
            
    def edit_package(self, id, **kwargs):
        all_packages = self.all_packages()
        if id in all_packages:  
            editing = all_packages[id]
            for key, value in kwargs.items():
                setattr(editing, key, value)
        else:
            print(f"No package found with id {id}")
    
    def all_packages(self):
        return {**self.priority_list, **self.non_priority_list}    
            
    def list_ready_priorities(self):
        priorities = [package for package in self.priority_list.values() if package.status == 'ready']
        return priorities
    def list_ready_non_priorities(self):
        non_priorities = [package for package in self.non_priority_list.values() if package.status == 'ready']
        return non_priorities 
            
    def list_ready_destinations(self):
        all_packages = self.all_packages()
        all_destinations = [package for package in all_packages.values() if package.status == 'ready']
        return all_destinations
        
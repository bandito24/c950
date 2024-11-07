from HashMap import HashMap

#Contains all relevant data for delivery. Destination Vertex attribute
# references a vertex in the DeliveryGraph.
# status attribute is 'delivered', 'hold', or 'ready'
class Package:
    def __init__(self, id, address, city, state, zip_code, deadline, weight, status="ready", delivering_truck = None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.delivering_truck = delivering_truck
        self.deadline = deadline
        #delivery_log will contain a tuple of truck departure time and package delivery time
        self.delivery_log = None
        self.destination_vertex = None
        
    def __lt__(self, other):
        if self.deadline == 'EOD':
            return False if other.deadline == 'EOD' else True
        if other.deadline == 'EOD':
            return False
        return self.deadline < other.deadline
    
    def __str__(self):
        message = "Package ID: {}, being delivered to {}, has a status of {}.".format(self.id, self.address, self.status)
        if self.status == 'delivered':
            message += " It was delivered by {} at {}".format(self.delivering_truck, self.delivery_log[1])
        return message
    
    
    
    
#Adds a package to priority list if the deadline is not 'EOD'. Priority list will
#always be the first destinations in delivery unless there are no ready packages here
class PackageList:
    def __init__(self):
        self.index = 0
        self.priority = HashMap(20)
        self.non_priority = HashMap(20)
#Adds the package to either the priority or non priority hash table depending on if
#there is a delivery requirement that is not the end of day
# runtime: O(n) due to possile resizing of hashmap  
    def add_package(self, order):
        if order.deadline != 'EOD':
            self.priority.insert(order.id, order)
        else:
            self.non_priority.insert(order.id, order)
            
#This is a useful function for setting all packages at a specific time ready
#runtime: O(n + m) where n represents priority list length and m represents non priority list length                
    def set_all_ready(self):
        all_buckets = self.priority.list + self.non_priority.list
        for bucket in all_buckets:
            for order in bucket:
                if order[1].status != 'delivered' and order[1].status != 'en route':
                    order[1].status = 'ready'
#Useful for function for updating a single package with new address or new status
#without needing to replace the entire instance
#runtime: O(k) where k represents number of keyword arguments to loop over. Lookup used on both lists is O(1)           
    def edit_package(self, id, **kwargs):
        success = self.priority.modify_item(id, **kwargs)
        if not success:
            success = self.non_priority.modify_item(id, **kwargs)
        if not success:
            print(f"No package found with id {id}")
#collects all ready packages from either the priority list or non priority list
# runtime: O(n) where n represents number of items in either priority or non priority list        
    def _list_ready(self, whichList):
        result = []
        for bucket in whichList.list: 
            for package in bucket:  
                if package[1].status == 'ready':  
                    result.append(package[1])
        return result 
            
    def list_ready_priorities(self):
        return self._list_ready(self.priority)
    
    def list_ready_non_priorities(self):
        return self._list_ready(self.non_priority)
#function used for lookup by users to see status of a package
#runtime: O(1)--locate function on both lists is O(1) and O(1 + 1) = O(1)    
    def locate_package(self, id):
        success = self.priority.locate(id)
        if success is None:
            success = self.non_priority.locate(id)  
        return success
    
    def find_status_at_time(self, start_time, end_time):
        found_packages = []
        all_packages = self.priority.list + self.non_priority.list
        for bucket in all_packages:
            for item in bucket:
                item = item[1]
                message = ""
                if item.delivery_log[0] >= start_time and item.delivery_log[0] <= end_time:
                    message += "Package ID: {} has a status of 'en route' after being loaded into {} at {}. ".format(item.id, item.delivering_truck, item.delivery_log[0]) 
                    message += "It will be delivered at {}".format(item.delivery_log[1])
                if message:
                    found_packages.append(message)
        if not found_packages:
            found_packages = ['No packages were loaded within this time frame']
        return found_packages
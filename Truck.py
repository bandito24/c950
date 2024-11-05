from datetime import time, datetime, timedelta

# packages attribute utilizes result from main.py generate_next_deliveries()
class Truck:
    average_mph = 18
    
    def __init__(self, name):
        self.packages = []
        self.departure_time = None
        self.total_miles = 0
        self.name = name
        self.packages_delivered = 0
        
    def add_delivery_packages(self, packages):
        self.packages.extend(packages)    
# Implements simple logging to report delivery status/time and updates the package reference to 'delivered'         
    def depart(self, time):
        self.departure_time = time
        return_distance = self.packages.pop()
        for package in self.packages:
            delivery = package['packages']
            minutes_driving = round((package['distance'] / self.average_mph) * 60)
            self.total_miles += package['distance']
            temp_datetime = datetime.combine(datetime.today(), self.departure_time) + timedelta(minutes=minutes_driving)
            self.departure_time = temp_datetime.time()
            for item in delivery:
                print(f'Package ID: {item.id} was delivered to {item.destination_vertex.address_label} at {self.departure_time} by {self.name}')
                item.status = 'delivered'
                self.packages_delivered += 1
        print(f'{self.packages_delivered} delivered total by {self.name}')
        time_to_return = round((return_distance / self.average_mph) * 60)
        self.total_miles += return_distance
        temp_datetime = datetime.combine(datetime.today(), self.departure_time) + timedelta(minutes=time_to_return)
        
        return_time = self.departure_time
        return return_time

        
    
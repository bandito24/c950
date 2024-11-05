import pandas as pd
from DeliveryMap import DeliveryGraph, DeliveryVertex
from Package import Package, PackageList
from Truck import Truck
from datetime import time

# Extracting the distances from the table and creating location
# vertexes from the distances to be used in graph edge weights for packages
df_distances = pd.read_excel("./distance_table.xlsx")
csv_distances = df_distances.values.tolist()[6:]
hubs = csv_distances[0][2:]
destinations = [i.split('\n')[1].strip() for i in hubs]

delivery_graph = DeliveryGraph()
for destination in destinations:
    vertex = DeliveryVertex(destination)
    delivery_graph.add_vertex(vertex)

all_distances = []
for i in range(1, len(csv_distances)):
    row = csv_distances[i]
    if not row[0]:
        break
    row[0], row[1] = row[1], row[0]
    row[1] = row[1].split('\n')[1].strip()
    row = row[1:]
    origin = row[0]
    j = 1
    while row[j]:
        origin_vertex = delivery_graph.vertex_dict[origin]
        destination_vertex = delivery_graph.vertex_dict[destinations[j - 1]]
        distance = row[j]
        delivery_graph.add_undirected_edge(origin_vertex, destination_vertex, distance)
        j += 1
#Extracting the package orders from the spreadsheet and creating
#Package instances with them, assigning each with a location vertex attribute and adding to Package List
df_orders = pd.read_excel("./package_table.xlsx")

csv_packages = df_orders.values.tolist()[7:]
orders = PackageList()
for package in csv_packages:
    order = Package(id=package[0], address=package[1], city=package[2], state=package[3], zip_code=package[4], deadline=package[5], weight=package[6])
    package[7] = package[7] if isinstance(package[7], str) else 'nan'
    if 'Delayed' in package[7] or 'truck 2' in package[7] or 'Wrong' in package[7]:
        order.status = 'hold'
    order.destination_vertex = delivery_graph.find_vertex(package[1])
    orders.add_package(order)
    
    
truck1 = Truck('truck1')
truck2 = Truck('truck2')
truck3 = Truck('truck3')

delivery_hub = delivery_graph.vertex_dict['4001 South 700 East,']

#Function for finding next appropriate delivery location based on
#Priority and closest next location
def generate_next_deliveries():
    priorities = orders.list_ready_priorities()
    first_deliveries = delivery_graph.nearest_neighbor_route(delivery_hub, priorities)
    if first_deliveries:
        last_endpoint = first_deliveries[-1].package[0].destination_vertex
    else:
        last_endpoint = delivery_hub
    non_priorities = orders.list_ready_non_priorities()
    second_deliveries = delivery_graph.nearest_neighbor_route(last_endpoint, non_priorities)    
    deliveries = first_deliveries + second_deliveries
    
    unique_locations = {}
    for delivery in deliveries:
        if delivery.address in unique_locations:
            unique_locations[delivery.address]['packages'].extend(delivery.package)
        else:
            unique_locations[delivery.address] = {'distance': delivery.distance, 'packages': delivery.package}
    deliveries = list(unique_locations.values())
    
    package_count = 0
    last_index = 0
    for index, grouping in enumerate(deliveries):
        package_count += len(grouping['packages'])
        if package_count <= 16:
            last_index = index
        else:
            break
    deliveries = deliveries[:last_index + 1]
    return_distance = delivery_graph.edge_weights[(deliveries[-1]['packages'][0].destination_vertex, delivery_hub)]
    deliveries.append(return_distance)
    return deliveries

#Sending trucks out with first ready packages at 8AM
first_deliveries = generate_next_deliveries()
truck1.add_delivery_packages(first_deliveries)
truck1_return_time = truck1.depart(time(8, 0))

#All but 1 package is now ready for delivery
orders.set_all_ready()
orders.edit_package(9, status='hold')

#Sending next truck out at 9:05
second_deliveries = generate_next_deliveries()
truck2.add_delivery_packages(second_deliveries)
truck2.depart(time(9, 5))

corrected_location = delivery_graph.vertex_dict['410 S State St']
orders.edit_package(9, destination_vertex=corrected_location, address='410 S State St', city='Salt Lake City', zip_code='84111', state='UT', status='ready')

# Sending last truck out with all remaining packages only after truck1 returns
third_deliveries = generate_next_deliveries()
truck3.add_delivery_packages(third_deliveries)
truck3.depart(truck1_return_time)

print(f'Total drive distance: {round(truck1.total_miles + truck2.total_miles + truck3.total_miles)} miles')
    
    

    


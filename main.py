import csv
import datetime

from Driver import Driver
from Package import Package
from Package import DeliveryStatus
from Package import DeliveryStatus
from Trucks import Truck
from HashTable import HashTable
from datetime import time, timedelta


#initialize the Hash Table
package_database= HashTable()


# Initializes the Truck objects and Drivers for their route
driver_1 = Driver(1, assigned_truck= 1)
driver_2 = Driver(2, assigned_truck= 2)

truck_1 = Truck(1, driver_1, datetime.timedelta(hours=8, minutes=0), None )
truck_2 = Truck(2, driver_2, datetime.timedelta(hours=9, minutes = 5), None )
truck_3 = Truck(3, None, datetime.timedelta(hours=0,minutes=0))

#trucks with special notes
packages_with_truck_restriction = [3,36,38]
grouped_packages = [13,14,15,16,19,20]
delayed_packages = [6,9,25,28,32]

fleet = [truck_1,truck_2, truck_3]




# import package data and initialize hash table
def import_packages(hash_table):

    # Open the package file
    with open("Data/Packages.csv") as file:
        # Read the file
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            delivery_deadline = row[5]
            package_weight = row[6]
            special_notes = row[7]
            delivery_status = DeliveryStatus.AT_THE_HUB
            loading_time = None
            time_delivered = None

            # Create the package object with the attributes extracted from the csv file
            package = Package(package_id,address,city,state,zip_code,delivery_deadline, package_weight,special_notes,delivery_status)

            # Import the package object into the hash table
            hash_table.insert(package_id,package)

    # Return the hash table
    return hash_table

def import_addresses():
    #Open The distance and addresses csv file
    with open("Data/Addresses.csv") as file:

        # Initializes an array to hold the addresses
        address_list = []
        csv_reader = csv.reader(file, delimiter=',')

        for row in csv_reader:
            #Split the full address into separate lines
            complete_address = row[0].split("\n")

            # Grabs the street address from the complete address and trim any trailing spaces and commas
            street_address = complete_address[1].strip().rstrip(",")

            #add the street address to the array
            address_list.append(street_address)

    # Return the address list
    return address_list

#import distance data
def initialize_distances():
    # initialize a 2D array to hold the distances between the 27 addresses
    address_distances = [[0.0 for x in range(27)] for y in range(27)]

    # Open the Distance package file
    with open("Data/Distances.csv") as file:

        csv_reader = csv.reader(file, delimiter=',')

        for row_id, row in enumerate(csv_reader):
            # Cleans up the row to only contain numeric strings ignoring any trailing empty values
            valid_address_distances = [value.strip() for value in row if value.strip() != '']

            # Loops through only the available values in the row
            for col_id, distance_str in enumerate(valid_address_distances):
                distance = float(distance_str)

                # 1. Assigns value to the lower triangular of the matrix
                address_distances[row_id][col_id] = distance

                # 2. Mirrors the values to the upper triangular portion of the matrix
                address_distances[col_id][row_id] = distance


        return address_distances

# helper function to get the distance between stops
def get_distance(point_a,point_b):
    #initilaize the address list and distance matrix
    address_list = import_addresses()
    distances = initialize_distances()

    # find the index of the given address on the address list
    index_1 = address_list.index(point_a)
    index_2 = address_list.index(point_b)

    # find the intersection between the two points and return the distance
    distance = distances[index_1][index_2]
    return distance


# assigns packages to trucks
def load_packages(hash_table, truck1, truck2, truck3):

# create a loop that goes through the truck list and takes that as an attribute
    for package_id in range(1,40 + 1):
        package = hash_table.get(package_id)
        #Debug
        if package is None:
            print(f"Warning: Package ID {package_id} returned None!")
            continue

        # loads packages with specific truck assignments
        if package_id in packages_with_truck_restriction:
            Package.add_package_to_truck(truck2, package, 2)

        # Checks if the packages need to be grouped
        elif package_id in grouped_packages:
            Package.add_package_to_truck(truck1, package, 2)

        # Checks for package delay
        elif package_id in delayed_packages:
            Package.add_package_to_truck(truck3, package, 4)

    # loads the remaining packages
    for  package_id in range(1,41):
        package = hash_table.get(package_id)

        # Checks if package is in either Truck 1 or 2 and skips if found
        if package in truck_1.packages or package in truck_2.packages or package in truck_3.packages:
            continue

        if "10:30" in package.delivery_deadline:
            if len(truck1.packages) < truck_1.capacity:
                Package.add_package_to_truck(truck1, package, 2)

            elif len(truck_2.packages) < truck_2.capacity:
                Package.add_package_to_truck(truck2, package, 2)

            elif len(truck_3.packages) < truck_3.capacity:
                Package.add_package_to_truck(truck3, package, 1)
        else:

            if len(truck_1.packages) < truck_1.capacity:
                Package.add_package_to_truck(truck1, package, 2)

            elif len(truck_2.packages) < truck_2.capacity:
                Package.add_package_to_truck(truck2, package, 2)

            elif len(truck_3.packages) < truck_3.capacity:
                 Package.add_package_to_truck(truck3, package, 1)



##### Delivery (Nearest Neighbor) Algorithm #######

def route_and_deliver(hash_table, truck):
  # Continues to loop until the truck is empty
    while len(truck.packages) > 0:
        #Set the shortest distance to infinity so any distance is smaller
        shortest_distance = float("inf")
        closest_package = None


        # Loops through all the packages to find the shortest distance
        for package in truck.packages:
            distance = get_distance(truck.location, package.address)
            if distance < shortest_distance:
                shortest_distance = distance
                closest_package = package


        # The truck drives to the closest delivery location
        if closest_package is not None:
          # Move the truck and calculate the mileage
            truck.location = closest_package.address
            truck.mileage += shortest_distance

            # Calculate the elapsed time of the trip
            elapsed_time = (shortest_distance / truck.speed) * 60

        #Update the Trucks clock and package delivery status
            truck.current_time += timedelta(minutes=elapsed_time)
            closest_package.delivery_time = truck.current_time
            closest_package.delivery_status = DeliveryStatus.DELIVERED

            #Remove/Deliver the package
        truck.packages.remove(closest_package)

    # Return the truck back to the hub once empty
    hub_address = "4001 South 700 East"
    distance_to_hub = get_distance(truck.location, hub_address)
    time_to_hub = (distance_to_hub / truck.speed) * 60
    truck.mileage += distance_to_hub
    truck.location = hub_address
    truck.current_time += timedelta(minutes=time_to_hub)



package_list = import_packages(package_database)

load_packages(package_list, truck_1, truck_2, truck_3)

# Deliver all packages
for truck in fleet:
    # Checks for truck 3
    if truck == truck_3:

        # Find the first truck to arrive and assign that driver to truck 3
        if truck_1.current_time <= truck_2.current_time:
            first_driver_return = truck_1.current_time
            truck_3.driver = driver_1
            truck_1.driver = None
        else:
            first_driver_return = truck_2.current_time
            truck_3.driver = driver_2
            truck_2.driver = None

        #Time package 9 address is corrected
        time_of_address_change = timedelta(hours=10,minutes=20 )

        # Set truck 3 departure time
        departure = max([time_of_address_change, first_driver_return])
        truck_3.departure_time = departure

        # Change address to package 9
        package_9 = package_database.get(9)
        package_9.address = "410 S State St"
        package_9.zip = "84111"

    # Deliver packages for the current truck in the loop
    route_and_deliver(package_database, truck)
















# 1. Total Mileage Check
total_mileage = truck_1.mileage + truck_2.mileage + truck_3.mileage
print("--- ALGORITHM METRICS ---")
print(f"Total Mileage: {total_mileage:.2f} miles")

# 2. Status Check
undelivered_count = 0
for i in range(1, 41):
    pkg = package_database.get(i)
    if pkg.delivery_status != "Delivered":
        undelivered_count += 1

print(f"Undelivered Packages remaining: {undelivered_count}")

print("=== DELAYED & DEADLINE VERIFICATION LOG ===")
all_passed = True

# Loop through all 40 packages in your database
for i in range(1, 41):
    package = package_database.get(i)

    # Extract the delivery time and the deadline string
    delivery_time = package.delivery_time
    deadline_str = package.delivery_deadline

    # Skip packages with "EOD" (End of Day) since they can't be late
    if "EOD" not in deadline_str:
        # Convert deadline string (e.g., "10:30 AM") to a timedelta for direct comparison
        # Stripping spaces and splitting hours/minutes
        time_parts = deadline_str.replace(" AM", "").split(":")
        deadline_hours = int(time_parts[0])
        deadline_minutes = int(time_parts[1])
        deadline_timedelta = timedelta(hours=deadline_hours, minutes=deadline_minutes)

        # Check if the package was delivered late
        if delivery_time > deadline_timedelta:
            print(f"❌ FAIL: Package {package.package_id} delivered LATE at {delivery_time} (Deadline: {deadline_str})")
            all_passed = False
        else:
            print(
                f"✅ PASS: Package {package.package_id} delivered on time at {delivery_time} (Deadline: {deadline_str})")

if all_passed:
    print("\n🎉 SUCCESS: All restricted deadline packages were delivered on time!")
else:
    print("\n⚠️ ALERT: Some package routing needs refinement to hit morning deadlines.")
























































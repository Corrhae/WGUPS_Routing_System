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
driver_1 = Driver(1)
driver_2 = Driver(2)

truck_1 = Truck(1, driver_1, datetime.timedelta(hours=8), None )
truck_2 = Truck(2, driver_2, datetime.timedelta(hours=9, minutes = 5), None )
truck_3 = Truck(3, None, [])

#trucks with special notes
packages_with_truck_restriction = [3,36,38]
grouped_packages = [13,14,15,16,19,20]
delayed_packages = [6,9,25,28,32]

truck_fleet = [truck_1,truck_2, truck_3]




# import package data and initialize hash table
def import_packages(hash_table):

    # Open the package file
    with open("Data/Packages.csv") as file:
        # Read the file
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            package_id = row[0]
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            delivery_deadline = row[5]
            package_weight = row[6]
            special_notes = row[7]
            delivery_status = DeliveryStatus(1)
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

        # Intializes an array to hold the addresses
        address_list = []
        csv_reader = csv.reader(file, delimiter=',')

        for row in csv_reader:
            #Split the full address into seperate lines
            complete_address = row[0].split("\n")

            # Obtain the address from the complete address and trim any trailing spaces and commas
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
    for package_id in range(len(hash_table)):
        package = hash_table.get(package_id)

        # if the truck has a truck requirement it is loaded to that truck
        if package_id in packages_with_truck_restriction:
            truck_2.packages.append(package)
            package.status = DeliveryStatus(1)

        # Checks if the packages need to be grouped
        elif package_id in grouped_packages:
            truck_1.packages.append(package)
            package.status = DeliveryStatus(1)

        # Checks for package delay
        elif package_id in delayed_packages:
            truck_2.packages.append(package)
            package.status = DeliveryStatus(4)

    # loads the remaining packages
    for  package_id in range(len(hash_table)):
        package = hash_table.get(package_id)

        # Checks if package is in either Truck 1 or 2 and skips if found
        if package in truck_1.packages or package in truck_2.packages:
            continue

        if "10:30" in package.deadline:
            if truck_1.packages.length < truck_1.capacity:
                truck_1.packages.append(package)

            elif truck_2.packages.length < truck_2.capacity:
                truck_2.packages.append(package)

            elif truck_3.packages.length < truck_3.capacity:
                truck_3.packages.append(package)
        else:

            if truck_1.packages.length < truck_1.capacity:
                truck_1.packages.append(package)

            elif truck_2.packages.length < truck_2.capacity:
                truck_2.packages.append(package)

            elif truck_3.packages.length < truck_3.capacity:
                 truck_3.packages.append(package)



##### Delivery (Nearest Neighbor) Algorithm #######

def route_and_deliver(hash_table, truck):
    shortest_distance = float("inf")

    for package in truck:
        distance = truck.location











#####print distances table#####
##table = initialize_distances()
#print("     " + "".join(f"{col:>5}" for col in range(27)))
#print("     " + "-" * (27 * 5))
#for row_idx, row in enumerate(table):
    #row_string = "".join(f"{dist:>5.1f}" for dist in row)
    #print(f"{row_idx:>3} |{row_string}")
























#print hash table
#import_packages(package_hash_table)
#for package_id in range(1,40):
  #  p = package_hash_table.get(str(package_id))
   # if p is not None:
      #  (p)


#adsressList = import_addresses()
###print(adsressList)






















import csv

from Package import Package
from Package import DeliveryStatus
from Trucks import Truck
from HashTable import HashTable

from datetime import datetime, timedelta

package_hash_table = HashTable()

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

#
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






















from datetime import timedelta,datetime
from Driver import Driver
from Trucks import Truck
from Package import Package, DeliveryStatus
from HashTable import HashTable

class LogisticsManager:
    def __init__(self, package_table, address_list, address_distances):
        self.package_table = package_table
        self.address_list = address_list
        self.address_distances = address_distances

        # State tracking variables
        self.fleet = []
        self.drivers = []
        self.total_mileage = 0.0

        # trucks with special notes
        self.packages_with_truck_restriction = [3, 36, 38]
        self.grouped_packages = [13, 14, 15, 16, 19, 20, 34]
        self.delayed_packages = [6, 9, 25, 28, 32]

    def setup_fleet(self):
        # Initializes the Truck objects and Drivers for their route
        driver_1 = Driver(1, assigned_truck=1)
        driver_2 = Driver(2, assigned_truck=2)

        truck_1 = Truck(1, driver_1, timedelta(hours=8, minutes=0), None)
        truck_2 = Truck(2, driver_2, timedelta(hours=9, minutes=5), None)
        truck_3 = Truck(3, None,timedelta(hours=0, minutes=0))

        self.fleet = [truck_1, truck_2, truck_3]
        self.drivers = [driver_1, driver_2]


    # assigns packages to trucks
    def load_packages(self):
        truck_1 = self.fleet[0]
        truck_2 = self.fleet[1]
        truck_3 = self.fleet[2]

        # create a loop that goes through the truck list and takes that as an attribute
        for package_id in range(1, 40 + 1):
            package = self.package_table.get(package_id)
            # Debug
            if package is None:
                print(f"Warning: Package ID {package_id} returned None!")
                continue

            # loads packages with specific truck assignments
            if package_id in self.packages_with_truck_restriction:
                Package.add_package_to_truck(truck_2, package, 2)

            # Checks if the packages need to be grouped
            elif package_id in self.grouped_packages:
                Package.add_package_to_truck(truck_1, package, 2)

            # Checks for package delay
            elif package_id in self.delayed_packages:
                Package.add_package_to_truck(truck_3, package, 4)

        # loads the remaining packages
        for package_id in range(1, 41):
            package = self.package_table.get(package_id)

            # Checks if package is in either Truck 1 or 2 and skips if found
            if package in truck_1.packages or package in truck_2.packages or package in truck_3.packages:
                continue

            if "10:30" in package.delivery_deadline:
                if len(truck_1.packages) < truck_1.capacity:
                    Package.add_package_to_truck(truck_1, package, 2)

                elif len(truck_2.packages) < truck_2.capacity:
                    Package.add_package_to_truck(truck_2, package, 2)

                elif len(truck_3.packages) < truck_3.capacity:
                    Package.add_package_to_truck(truck_3, package, 1)
            else:

                if len(truck_1.packages) < truck_1.capacity:
                    Package.add_package_to_truck(truck_1, package, 2)

                elif len(truck_2.packages) < truck_2.capacity:
                    Package.add_package_to_truck(truck_2, package, 2)

                elif len(truck_3.packages) < truck_3.capacity:
                    Package.add_package_to_truck(truck_3, package, 1)



    def get_distance(self,point_a,point_b):
        # find the index of the given address on the address list
        index_1 = self.address_list.index(point_a)
        index_2 = self.address_list.index(point_b)

        # find the intersection between the two points and return the distance
        distance = self.address_distances[index_1][index_2]

        return distance

    def route_and_deliver(self,truck):
      # Continues to loop until the truck is empty
        while len(truck.packages) > 0:
            #Set the shortest distance to infinity so any distance is smaller
            shortest_distance = float("inf")
            closest_package = None

            # Loops through all the packages to find the shortest distance
            for package in truck.packages:
                distance = self.get_distance(truck.location, package.address)
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
        distance_to_hub = self.get_distance(truck.location, hub_address)
        time_to_hub = (distance_to_hub / truck.speed) * 60
        truck.mileage += distance_to_hub
        truck.location = hub_address
        truck.current_time += timedelta(minutes=time_to_hub)

    def run_delivery(self):
        truck_1 = self.fleet[0]
        truck_2 = self.fleet[1]
        truck_3 = self.fleet[2]

        driver_1 = self.drivers[0]
        driver_2 = self.drivers[1]

        # Deliver all packages
        for truck in self.fleet:
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

                # Time package 9 address is corrected
                time_of_address_change = timedelta(hours=10, minutes=20)

                # Set truck 3 departure time
                departure = max([time_of_address_change, first_driver_return])
                truck_3.departure_time = departure
                truck_3.current_time = departure

                # Change address to package 9
                package_9 = self.package_table.get(9)
                package_9.address = "410 S State St"
                package_9.zip = "84111"

            # Deliver packages for the current truck in the loop
            self.route_and_deliver(truck)

            # Update mileage
            self.total_mileage += truck.mileage


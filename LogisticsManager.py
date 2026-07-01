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

        # Lists of package IDs used to enforce the delivery constraints
        # provided in the project requirements.
        # These constraints are checked before normal package assignment.
        self.packages_with_truck_restriction = [3, 36, 38,18]
        self.grouped_packages = [13, 14, 15, 16, 19, 20]
        self.delayed_packages = [6, 9, 25, 28, 32]

    def setup_fleet(self):
        # Create the available drivers and assign the initial trucks
        # that will leave the hub first.
        driver_1 = Driver(1, assigned_truck=1)
        driver_2 = Driver(2, assigned_truck=2)

        # Truck 3 initially has no driver because only two drivers
        # are available. It will depart after one of the first trucks
        # completes its route and returns to the hub.
        truck_1 = Truck(1, driver_1, timedelta(hours=8, minutes=0), None)
        truck_2 = Truck(2, driver_2, timedelta(hours=9, minutes=5), None)
        truck_3 = Truck(3, None,timedelta(hours=0, minutes=0), None)

        self.fleet = [truck_1, truck_2, truck_3]
        self.drivers = [driver_1, driver_2]


    # Assign packages to trucks while honoring all delivery constraints
    def load_packages(self): # <-- Time Complexity: O(1)
        truck_1 = self.fleet[0]
        truck_2 = self.fleet[1]
        truck_3 = self.fleet[2]

        # First pass:
        # Load every package with a special delivery constraint before
        # assigning the remaining packages. This guarantees that
        # required business rules are satisfied first.

        for package_id in range(1, 40 + 1):
            package = self.package_table.get(package_id)

            # Skip any package that could not be retrieved from the hash table.
            # This prevents runtime errors if package data is missing.
            if package is None:
                print(f"Warning: Package ID {package_id} returned None!")
                continue

            # Packages that are restricted to a specific truck must be
            # loaded there
            if package_id in self.packages_with_truck_restriction:
                Package.add_package_to_truck(truck_2, package, 2)

            # These packages must remain together and therefore are loaded
            # onto the same truck.
            elif package_id in self.grouped_packages:
                Package.add_package_to_truck(truck_1, package, 2)

           # Delayed packages are reserved for Truck 3 if deadline is EOD
           # otherwise it is placed on truck 2
            elif package_id in self.delayed_packages:
                # If it's delayed BUT has a tight 10:30 AM deadline
                if "10:30" in package.delivery_deadline:
                    Package.add_package_to_truck(truck_2, package, 2)
                else:
                    Package.add_package_to_truck(truck_3, package, 4)

        # Second pass:
        # Assign all remaining packages that do not have special
        # constraints while attempting to prioritize earlier deadlines.
        for package_id in range(1, 41):
            package = self.package_table.get(package_id)

            # Skip packages that were already assigned during the first pass
            if package in truck_1.packages or package in truck_2.packages or package in truck_3.packages:
                continue


            # Prioritize packages with a 10:30 AM deadline by placing
            # them on the earliest available truck with capacity.
            if ("9:00" in package.delivery_deadline) or ("10:30" in package.delivery_deadline):
                if len(truck_1.packages) < truck_1.capacity:
                    Package.add_package_to_truck(truck_1, package, 2)

                elif len(truck_2.packages) < truck_2.capacity:
                    Package.add_package_to_truck(truck_2, package, 2)


            # End-of-day packages are loaded after all priority deliveries
            # while respecting each truck's capacity.
        for package_id in range(1, 41):
            package = self.package_table.get(package_id)

            # Skip packages that were already assigned during the first pass
            if package in truck_1.packages or package in truck_2.packages or package in truck_3.packages:
                continue

            if len(truck_1.packages) < truck_1.capacity:
                Package.add_package_to_truck(truck_1, package, 2)

            elif len(truck_3.packages) < truck_3.capacity:
                Package.add_package_to_truck(truck_3, package, 1)

            elif len(truck_2.packages) < truck_2.capacity:
                Package.add_package_to_truck(truck_2, package, 2)


    def get_distance(self,point_a,point_b):
        # Find the index of the given address on the address list
        index_1 = self.address_list.index(point_a)
        index_2 = self.address_list.index(point_b)

        # Find the intersection between the two points and return the distance
        distance = self.address_distances[index_1][index_2]

        return distance

    # Deliver every package assigned to the truck using the
    # nearest-neighbor routing heuristic.
    # The truck repeatedly travels to the closest undelivered
    # package until its route is complete.
    def route_and_deliver(self,truck): # <--- Time Complexity: O(n^2)
        # Set the departure time for all packages on this truck before delivering
        for package in truck.packages:
            package.departure_time = truck.departure_time
      # Continues to loop until the truck is empty
        while len(truck.packages) > 0:

            # Start each search assuming no destination has been chosen.
            # Any valid distance found will be shorter than infinity.
            shortest_distance = float("inf")
            closest_package = None

            # Check if there are any urgent deadline packages left on the truck
            deadline_packages = [
                p for p in truck.packages if "EOD" not in p.delivery_deadline
            ]

            # If urgent packages exist, ONLY look through those.
            # Otherwise, open up the search to all remaining packages (EODs)
            search_list = (
                deadline_packages if deadline_packages else truck.packages
            )


            # Compare the truck's current location to our targeted search list
            for package in search_list:
                distance = self.get_distance(truck.location, package.address)
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_package = package

            # Travel to the nearest delivery location and update
            # the truck's position and accumulated mileage.
            if closest_package is not None:
                truck.location = closest_package.address
                truck.mileage += shortest_distance

                # Convert travel distance into travel time using the truck's constant speed.
                elapsed_time = (shortest_distance / truck.speed) * 60

                # Record the delivery timestamp and update the package's
                # status to indicate successful delivery.
                truck.current_time += timedelta(minutes=elapsed_time)
                closest_package.delivery_time = truck.current_time
                closest_package.delivery_status = DeliveryStatus.DELIVERED

            # Remove the delivered package so it will not be considered during the next nearest-neighbor search.
            truck.packages.remove(closest_package)



      # Once all assigned packages have been delivered,
      # return the truck to the hub so its completion time
      # accurately reflects when it becomes available again.
        hub_address = "4001 South 700 East"
        distance_to_hub = self.get_distance(truck.location, hub_address)
        time_to_hub = (distance_to_hub / truck.speed) * 60
        truck.mileage += distance_to_hub
        truck.location = hub_address
        truck.current_time += timedelta(minutes=time_to_hub)
        truck.completion_time = truck.current_time

    # Execute the complete delivery simulation for every truck
    def run_delivery(self): # <---- Time Complexity: O(n^2)
        truck_1 = self.fleet[0]
        truck_2 = self.fleet[1]
        truck_3 = self.fleet[2]

        driver_1 = self.drivers[0]
        driver_2 = self.drivers[1]

        # Deliver all packages in fleet
        for truck in self.fleet:

            # Truck 3 cannot leave until a driver returns from one
            # of the first two delivery routes.
            if truck == truck_3:

             # Reassign the first available driver to Truck 3.
             # This models the project requirement of only having
             # two available drivers.
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

                # Package 9 receives its corrected delivery address
                # at 10:20 AM
                package_9 = self.package_table.get(9)
                package_9.address = "410 S State St"
                package_9.zip = "84111"

            # Deliver every package assigned to the current truck
            # using the nearest-neighbor routing algorithm.
            self.route_and_deliver(truck)

            # Keep a running total of fleet mileage for reporting.
            self.total_mileage += truck.mileage


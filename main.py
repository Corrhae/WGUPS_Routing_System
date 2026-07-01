# Student ID# 011697724
from datetime import timedelta
from datetime import datetime
from HashTable import HashTable
from LogisticsManager import LogisticsManager
from DataReader import DataReader

class UserInterface: # Time Complexity: O(n)
    def __init__(self, simulation):
        self.simulation = simulation

    def start_menu(self):
        print("=" * 60)
        print("         WESTERN GOVERNORS UNIVERSITY")
        print("        PACKAGE ROUTING & DELIVERY SYSTEM")
        print("=" * 60)

        # Print menu options
        print()
        print("+------------------------------------------+")
        print("|               MAIN MENU                  |")
        print("+------------------------------------------+")
        print("| 1. View Full Package Report              |")
        print("| 2. Search Package by Time                |")
        print("| 3. View Fleet Mileage                    |")
        print("| 4. Exit                                  |")
        print("+------------------------------------------+")

        while True:
            # Get user input
            user_input = input("Pick an option(1-4):__ ")

            if user_input == "1":
                self.generate_full_report()

            elif user_input == "2":
               self.print_status()

            elif user_input == "3":
                self.show_mileage()

            elif user_input == "4":
               print("Program exiting...")
               break

            else:
                print("Invalid input. Please try again.")



    def print_status(self): # <--- Time Complexity: O(1)

        while True:
            try:
                package_id = input("Enter package ID (1-40): ").strip()
                input_time  =input("Enter time (HH:MM): ")
                package = self.simulation.package_table.get(package_id)

                parsed_time = datetime.strptime(input_time, "%H:%M")
                if parsed_time.hour < 7:
                    query_time = timedelta(hours=parsed_time.hour + 12, minutes=parsed_time.minute)
                else:
                    query_time = timedelta(hours=parsed_time.hour, minutes=parsed_time.minute)
                break;
            except ValueError:
                print("Invalid input. Please try again.")

        stripped_time = parsed_time.strftime("%H:%M")
        period = "AM" if 12 > parsed_time.hour >= 8 else "PM"

        print("=" * 195)
        print(f"                                                                         Status of package ID:{package_id} at {stripped_time} {period}")
        print("=" * 195)


        print(
            f"{'ID':<6} | "
            f"{'Street Address':<47} | "
            f"{'City':<33} | "
            f"{'ST':<10} | "
            f"{'Zip':<10} | "
            f"{'Truck#':<13} |"
            f"{'Status':<19} | "
            f"{'Deadline':<18} | " 
            f"{'Delivery Time'} ")

        print("-" * 195)

        self.print_package_status(package, query_time)
        print()

    def generate_full_report(self): # <--- Time complexity: O(n)

        time_input = input("Enter time (HH:MM, eg.. 09:30): ").strip()
        try:
            parsed_time = datetime.strptime(time_input, "%H:%M")

            if parsed_time.hour < 7:
                query_time = timedelta(hours=parsed_time.hour + 12, minutes=parsed_time.minute)
            else:
                query_time = timedelta(hours=parsed_time.hour, minutes=parsed_time.minute)



        except ValueError:
             print("invalid input. Please enter time in format HH:MM")
             return

        stripped_time = parsed_time.strftime("%H:%M")
        period = "AM" if 12 > parsed_time.hour >= 8 else "PM"

        print("=" * 195)
        print(f"                                                FLEET SNAPSHOT REPORT AT {stripped_time} {period} ")
        print("=" * 195)


        print(
            f"{'ID':<3} | "
            f"{'Street Address':<35} | "
            f"{'City':<21} | "
            f"{'ST':<3} | "
            f"{'Zip':<7} | "
            f"{'Truck#':<6} |"
            f"{'Status':<13} | "
            f"{'Deadline':<10} | " 
            f"{'Delivery Time':<9} ")

        print("-" * 195)

        for package_id in range(1,41):
            package = self.simulation.package_table.get(package_id)
            if package:
                self.print_package_status(package, query_time)

        print("=" * 195)


    def print_package_status(self, package, query_time):
        # Check for package 9 and show address depending on query time
        if package.package_id == 9 and query_time < timedelta(hours=10,minutes=20):
            address = "300 State St"
            zip = "84103"
        else:
            address = package.address
            zip = package.zip_code

        # Check if package is delivered already
        if query_time >= package.delivery_time:
            status = "Delivered"
            delivery_info = package.delivery_time

        elif package.departure_time <= query_time < package.delivery_time:
            status = "En Route"
            delivery_info = "No info yet"

        elif "Delayed" in package.special_notes and query_time < timedelta(hours=9, minutes=5):
            status = "Delayed"
            delivery_info = "Awaiting Arrival"

        else:
            status = "At the Hub"
            delivery_info = "No info yet"

        print(
            f" {package.package_id:<2} | "
            f"{address:<35} | "
            f" {package.city:<20} | "
            f"{package.state:<3} | "
            f" {zip:<6} | "
            f"{package.truck_id:<6} | "
            f"{status:<12} | "
            f"{package.delivery_deadline:<10} | "
            f" {str(delivery_info)}")


    def show_mileage(self): # Time Complexity: O(1)

        # prompt user for time
        time_input = input("Enter time in 24-hour format (HH:MM, e.g., 09:30 or 14:15): ").strip()
        try:
            parsed_time = datetime.strptime(time_input, "%H:%M")

            if parsed_time.hour < 7:
                query_time = timedelta(hours=parsed_time.hour + 12, minutes=parsed_time.minute)
            else:
                query_time = timedelta(hours=parsed_time.hour, minutes=parsed_time.minute)
        except ValueError:
            print("Invalid time format. Returning 0.0 mileage.")
            return 0.0


        total_mileage = 0.0

        stripped_time = parsed_time.strftime("%H:%M")
        period = "AM" if 12 > parsed_time.hour >= 8 else "PM"

        print(f"=====================================================================")
        print("                      FLEET MILEAGE REPORT")
        print(f"=====================================================================")
        print(f"SNAPSHOT TIME: {stripped_time} {period}")
        print("~" * 69)
        for truck in self.simulation.fleet:

            # If the truck hasn't left yet
            if query_time < truck.departure_time:
                print(f" 🚚 Truck {truck.truck_id} | Status: 🏠 AT HUB       | Mileage: 0.00 miles")
                continue

            # If the query time is after the route completion time
            elif query_time >= truck.completion_time:
                 total_mileage += truck.mileage
                 print(f" 🚚 Truck {truck.truck_id} | Status: ✅ COMPLETED    | Mileage: {truck.mileage:.2f} miles")
            else:
                # Calculate the total time driven
                time_spent_driving = query_time - truck.departure_time

                #convert the time delta to total hours
                hours_driven = time_spent_driving.total_seconds() / 3600

                # Calculate the miles driven
                estimated_mileage = 18 * hours_driven
                total_mileage += estimated_mileage
                print(f" 🚚 Truck {truck.truck_id} | Status: 💨 IN TRANSIT    | Mileage: {estimated_mileage:.2f} miles")

        print("~" * 69)

        print(f"📊 Total combined fleet mileage at {stripped_time} {period}: {total_mileage:.2f} miles\n")

        return total_mileage




            #



def main():

# Intitialize empty table
    package_database = HashTable()

# Parse Raw Data and insert into respective data structures
    addresses = DataReader.import_addresses("Data/Addresses.csv")
    distances = DataReader.initialize_distances("Data/Distances.csv")
    DataReader.import_packages(package_database,"Data/Packages.csv")

# Create a Delivery instance
    delivery_simulation = LogisticsManager(package_database, addresses, distances)

# 4. Run the Delivery simulation step-by-step
    delivery_simulation.setup_fleet()
    delivery_simulation.load_packages()
    delivery_simulation.run_delivery()
    ui = UserInterface(delivery_simulation)
    ui.start_menu()


    print(f"Simulation processed successfully. Total Mileage: {delivery_simulation.total_mileage:.2f} miles")

if __name__ == "__main__":
    main()




















































from HashTable import HashTable
from LogisticsManager import LogisticsManager
from DataReader import DataReader

def main():

# Intitialize empty table
    package_database = HashTable()

# Parse Raw Data and insert into respective data structures
    addresses = DataReader.import_addresses("Data/Addresses.csv")
    distances = DataReader.initialize_distances("Data/Distances.csv")
    DataReader.import_packages(package_database,"Data/Packages.csv")

# Create a Delivery instance
    sim = LogisticsManager(package_database, addresses, distances)

# 4. Run the Delivery simulation step-by-step
    sim.setup_fleet()
    sim.load_packages()
    sim.run_delivery()

    print(f"Simulation processed successfully. Total Mileage: {sim.total_mileage:.2f} miles")

if __name__ == "__main__":
    main()




















































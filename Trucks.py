from main import currentTime


class Truck:

#Constructor for Truck objects and attributes
    def __init__ (self,truck_id,driver, departure_time,packages = None ):
        self.truck_id = truck_id
        self.driver = driver
        self.capacity = 16
        self.speed = 18
        self.mileage = 0.0
        self.departure_time = departure_time
        self.current_time = departure_time
        self.location = "4001 South 700 East"

        # if pakages is not filled during initialization an empty array is created
        if packages is None:
            self.packages = []
        else:
            self.packages = packages





    #create a str() function to return the truck object
    def __str__(self):
        return "Truck #" + str(self.truck_id)





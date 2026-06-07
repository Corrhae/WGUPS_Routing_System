from enum import Enum
#An enumeration class to keep delivery status values constant
class DeliveryStatus(str,Enum):
    AT_THE_HUB = "At the Hub"
    EN_ROUTE = "En Route"
    DELIVERED = "Delivered"
    DELAYED = "Delayed"

class Package:
    def __init__ (self, package_id,address, city, state, zip_code, delivery_deadline, package_weight, special_notes,delivery_status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.package_weight = package_weight
        self.special_notes = special_notes
        self.required_truck = None
        self.delivery_status = DeliveryStatus.AT_THE_HUB
        self.departure_time = None
        self.delivery_time = None

# Adds packages to trucks and update delivery status
    def add_package_to_truck(truck, package, status_code):
        status_map ={
            1:DeliveryStatus.AT_THE_HUB,
            2:DeliveryStatus.EN_ROUTE,
            3:DeliveryStatus.DELIVERED,
            4:DeliveryStatus.DELAYED,
        }
        truck.packages.append(package)
        package.departure_time = truck.departure_time
        package.delivery_status = status_map[status_code]



    # print package object in human readable form 2. fix the typoin the return statement and have each attriute on its own line.
    def __str__(self):

        return f"{self.package_id:<5} | {self.address:<30} | {self.city:<16} | {self.state:<5} | {self.zip_code:<8} | {self.delivery_deadline:<12} | {self.package_weight:<5} | {self.delivery_status:<12} | {self.delivery_time}"











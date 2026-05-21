from enum import Enum
#An enumeration class to keep delivery status values constant
class DeliveryStatus(Enum):
    AT_THE_HUB = 1
    EN_ROUTE = 2
    DELIVERED = 3
    DELAYED = 4

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
        self.time_delivered = None




    # print package object in human readable form 2. fix the typoin the return statement and have each attriute on its own line.
    def __str__ (self):
        return (f"{str(self.package_id):<5}| {str(self.address): <30} | "
                f"{str(self.city): <15} | {str(self.state): <15} | "
                f" {str(self.zip_code): <15} | {str(self.delivery_deadline): <15} | "
                f"{str(self.package_weight):<5} | {str(self.special_notes):<30} | "
                f"{str(self.departure_time): <15} | {str(self.time_delivered): <15} "
                f" | {str(self.delivery_status): <20} ")


    #Debug
    def __repr__ (self):
        return (
            f"{self.package_id:<5}| {self.address: <30} | {self.city: <15} | {self.state: <15} | {self.zip_code: <15} | {self.delivery_deadline: <15} |"
            f"{self.package_weight:<5} | {self.special_notes:<30} | {self.loading_time: <15} | {self.time_delivered: <15} | {self.delivery_status: <20} ")








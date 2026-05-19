from enum import Enum
#An enumeration class to keep delivery status values constant
class DeliveryStatus(Enum):
    AT_THE_HUB = 1
    EN_ROUTE = 2
    DELIVERED = 3

class Package:
    def __init__ (self, package_id,address, city, state, zip_code, delivery_deadline, package_weight, special_notes, loading_time,time_delivered,delivery_status):
        self.package_id = package_id;
        self.address = address;
        self.city = city;
        self.state = state;
        self.zip = zip_code;
        self.delivery_deadline = delivery_deadline;
        self.package_weight = package_weight;
        self.special_notes = special_notes;
        self.loading_time = loading_time;
        self.delivery_status = DeliveryStatus.AT_THE_HUB;
        self.time_delivered = time_delivered;

    # print package object in human readable form 2. fix the typoin the return statement and have each attriute on its own line.
    def __str__ (self):
        return (f"{self.package_id:<5}| {self.address: <30} | {self.city: <15} | {self.state: <15} | {self.zip_code: <15} | {self.delivery_deadline: <15} |"
                f"{self.package_weight:<5} | {self.special_notes:<30} | {self.loading_time: <15} | {self.time_delivered: <15} | {self.delivery_status: <20} ")


    #Debug
    def __repr__ (self):
        return (
            f"{self.package_id:<5}| {self.address: <30} | {self.city: <15} | {self.state: <15} | {self.zip_code: <15} | {self.delivery_deadline: <15} |"
            f"{self.package_weight:<5} | {self.special_notes:<30} | {self.loading_time: <15} | {self.time_delivered: <15} | {self.delivery_status: <20} ")



    # create a method to update address errors at the stated time=


    #create a method to enure certain packages are on their required trucks



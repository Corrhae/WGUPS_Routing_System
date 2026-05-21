class HashTable:
    def __init__(self):
        self.size = 41
        self.table = [[] for _ in range(self.size)]

    # hash function
    def hash(self, key):
        return  int (key) % self.size

    # function to insert
    def insert(self, key, value):
        bucket_index = self.hash(key)

        bucket = self.table[bucket_index]
        key_exist = False

        str_key = str(key)

        for item in self.table[bucket_index]:
            if item[0] == str_key:
                item[1] = value
                key_exist = True
                break

        if not key_exist:
            self.table[bucket_index].append([str_key, value])
            return


    #function to get/lookup
    def get(self, key):
        bucket_index = self.hash(key)

        key_exist = False
        str_key = str(key)

        for item in self.table[bucket_index]:
            if item[0] == str_key:
                return item[1]

        print("Key not found")

        return None


    #function to delete
    def remove(self, key):
        bucket_index = self.hash(key)

        str_key = str(key)

        for item in self.table[bucket_index]:
            if item[0] == str_key:
                self.table[bucket_index].remove(item)
                print("Package removed")
                return

        print("key not found here")
        return


    #function to print table
    def print_table(self):
        for item in self.table:
            print(item)
        return




        #The packageID is the key and the package object the value
class HashTable:
    def __init__(self):
        self.size = 41
        self.table = [[] for _ in range(self.size)]

    # hash function
    def get_hash(self, key):
        return  int (key) % self.size

    # function to insert
    def insert(self, key, value):
        key = int(key)
        bucket_index = self.get_hash(key) % len(self.table)

        bucket = self.table[bucket_index]
        key_exist = False

        for item in self.table[bucket_index]:
            if item[0] == key:
                item[1] = value
                key_exist = True
                break

        if not key_exist:
            self.table[bucket_index].append([key, value])
            return


    #function to get/lookup
    def get(self, key):
        key = int(key)

        bucket_index = self.get_hash(key) % len(self.table)
        bucket = self.table[bucket_index]
        ##print("Inserting key:", type(key), key)

        ##print("Looking up key:", type(key), key)


        for item in self.table[bucket_index]:
            if item[0] == key:
                return item[1]

        print("Key not found")
        return None


    #function to delete
    def remove(self, key):
        bucket_index = self.get_hash(key)

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
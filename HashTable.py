class HashTable: # <--- AVG Time Complexity: O(1)
    def __init__(self):
        # Create a fixed-size hash table with 41 buckets.
        self.size = 41

        # Each bucket is initialized as an empty list to support
        # separate chaining when collisions occur.
        self.table = [[] for _ in range(self.size)]

    # hash function
    def get_hash(self, key):
        # Convert the package ID into a bucket index.
        return  int (key) % self.size

    # Insert a package into the hash table
    def insert(self, key, value):
        key = int(key)

        # Determine which bucket should store this package.
        bucket_index = self.get_hash(key)

        bucket = self.table[bucket_index]
        key_exist = False

        # Search the bucket to determine whether the key already exists.
        # If it does, replace the existing value instead of creating
        # a duplicate entry.
        for item in self.table[bucket_index]:
            if item[0] == key:
                item[1] = value
                key_exist = True
                break

        # If the key was not found, append the new key-value pair
        # to the bucket.
        if not key_exist:
            self.table[bucket_index].append([key, value])
            return


    #function to get/lookup using package ID
    def get(self, key):
        key = int(key)

        # Calculate the bucket that should contain the requested package.
        bucket_index = self.get_hash(key)
        bucket = self.table[bucket_index]

        # Search only within the appropriate bucket instead of
        # scanning the entire table
        for item in self.table[bucket_index]:
            if item[0] == key:
                return item[1]

        # Return None if the package ID is not stored.
        print("Key not found")
        return None


    # Search the bucket and remove the matching entry.
    def remove(self, key):
        # Locate the bucket where the package should exist.
        bucket_index = self.get_hash(key)

        str_key = str(key)

        # Search the bucket and remove the matching entry.
        for item in self.table[bucket_index]:
            if item[0] == str_key:
                self.table[bucket_index].remove(item)
                print("Package removed")
                return

        print("key not found here")
        return


    # Print all the buckets
    def print_table(self):
        for item in self.table:
            print(item)
        return





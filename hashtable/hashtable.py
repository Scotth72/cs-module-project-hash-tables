class HashTableEntry:
    """
    Linked List hash table key/value pair
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __str__(self):
        return f'Key: {self.key}, Value: {self.value}'


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        self.capacity = max(8, capacity)
        self.storage = [None] * max(8, capacity)
        self.storage_count = 0

    def __str__(self):
        return f'Hashtable Class {self.capacity}, {self.storage}'

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        print('total slots', self.capacity)
        return self.capacity

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # Your code here
        return self.stored_count / self.capacity

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        # Your code here
        hash = 5381
        for c in key:
            hash = (hash * 33) + ord(c)

        return hash

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # return self.fnv1(key) % self.capacity
        return self.djb2(key) % len(self.storage)

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Your code here
        index = self.hash_index(key)
        if self.storage[index] is not None:  # if there is a value at the index
            node = self.storage[index]

            while node.key != key and node.next is not None:
                node = node.next  # this will allow to loop and find the node w/ matching keys

            if node.key == key:  # updating new value to the existing key
                node.value = value

            else:  # if  no key this will add to tail
                node.next = HashTableEntry(key, value)
                self.storage_count += 1
                self.resize(self.capacity * 2)

        else:  # if there is no value at the index
            self.storage[index] = HashTableEntry(key, value)
            self.storage_count += 1

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here
        index = self.hash_index(key)

        if self.storage[index] is None:  # if the key in not in the hashtable
            return None

        # if only the head is present at the index
        elif self.storage[index].next is None:
            removed_value = self.storage[index].value
            self.storage[index] = None
            self.storage_count -= 1
            return removed_value

        else:  # tells more than the head
            node = self.storage[index]
            prev = None

            while node.key != key and node.next is not None:  # loop through the array to match
                prev = node
                node = node.next

            if node.key == key:  # if key's match the prev pointer to the next, return the removed value
                prev.next = node.next
                removed_value = node.value
                node = None
                self.storage_count -= 1
                return removed_value

            else:  # the key is not found
                return None

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Your code here
        index = self.hash_index(key)

        if self.storage[index] is None:  # if key is not in hashtable
            return None

        elif self.storage[index].next is not None:
            node = self.storage[index]

            while node.key != key and node.next is not None:  # going through to find key
                node = node.next

            if node.key == key:
                return node.value

            else:
                return None

        else:  # returns value at the hash index
            return self.storage[index].value

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        if self.get_load_factor() > 0.7:
            if new_capacity < self.capacity * 2:
                new_capacity = self.capacity * 2

            new_storage = [None] * new_capacity
            old_storage = self.storage

            self.capacity = new_capacity
            self.storage = new_storage

            for item in old_storage:
                if item is not None:
                    node = item
                    while node is not None:
                        self.put(node.key, node.key)
                        node = node.next


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")

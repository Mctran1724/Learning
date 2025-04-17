"""
The LRU Cache is a data structure that stores a fixed number of key-value pairs in memory in constant time.
The LRU (least recently used) policy is a strategy for determining the elements to delete from the cache when it is full.

The policy is as follows: Whenever a key is added or looked up, it becomes the most recently used element. 
If the cache is full, the least recently used element is deleted.

How do you come up with an LRU cache by yourself? First we must decide on data structure.
We know that we need a cache to store key-value pairs. A hashtable is most natural to handle the cacheing, because of constant time arbitrary lookups, insertions, and deletions.
Now how about the LRU policy?
LRU policy suggests 3 further requirements:
1) Keep track of elements in the order they are added so we can look up the least recently used in constant time.
2) Be able to operate on the end of the data structure in constant time to update the most recently used element.
3) Delete an arbitrary element from the data structure in constant time to perform a cache eviction.

Requirement 1 forces us into a sequential data structure.
Requirement 2 forces us into one of array, linked list, or queue.
Requirement 3 is satisfied ONLY by a linked list!

Thus, the key to the implementation is the combination of a linked list with a hashtable!
We can now start to design the classes.
We'll use a hashtable to map keys to linked list node pointers that hold the values.
The linked list holding the nodes will be our LRU cache, and updates itself to keep track of the most recently used elements.
"""


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
    
    def __repr__(self):
        return f'Node({self.key}, {self.value})'
    
    def __str__(self):
        return f"({self.key}: {self.value})"
    

class LinkedList:
    def __init__(self):
        self.head = Node(-1, -1) # Points to most recently used
        self.tail = Node(-1, -1) # Points to least recently used 
        self.head.next = self.tail 
        self.tail.prev = self.head
        self.size = 0
    
    def __repr__(self):
        result = []
        curr = self.head.next
        while curr != self.tail:
            result.append(str(curr))
            curr = curr.next
        return " <-> ".join(result)

    def push(self, node: Node) -> None:
        """ 
        Pushes a node to the front of the linked list at the most recently used position in constant time by rewiring pointers
        """

        MRU = self.head.next
        self.head.next = node
        node.next = MRU
        MRU.prev = node
        node.prev = self.head

        return
    
    def remove(self, node: Node) -> None:
        """
        Removes a node from the linked list in constant time by rewiring pointers
        """
        
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

        return
    
    def update(self, node: Node) -> None:
        """
        Updates a node in the linked list in constant time by rewiring pointers
        """
        self.remove(node)
        self.push(node)
        return

    def pop(self) -> Node:
        """
        Pops and returns the least recently used node from the linked list in constant time by rewiring pointers
        """
        LRU = self.tail.prev
        self.remove(LRU)
        return LRU
    
"""
The LRU cache itself will have 3 main operations:
get(key): Returns the value associated with the key if it exists in the cache, otherwise returns -1, then updates the key to be the most recently used element.
put(key, value): Adds the key-value pair to the cache if the key does not already exist there. If the cache is at capacity remove the least recently used element to make room for the new key-value pair.
remove(key): Removes the key if it is present in the cache, then updates the key to be the most recently used element.
"""

class LRU_cache:
    def __init__(self, capacity: int = 32):
        self.capacity = capacity
        self.cache = {}
        self.ll = LinkedList()
        self.size = 0

    def get(self, key):
        if key not in self.cache:
            return -1 
        else:
            node = self.cache[key]
            self.ll.update(node)
            result = node.value
            return result

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.ll.update(node)
        else:
            if self.size == self.capacity:
                LRU = self.ll.pop()
                del self.cache[LRU.key]
                self.size -= 1
            new_node = Node(key, value)
            self.cache[key] = new_node
            self.ll.push(new_node)
            self.size += 1

    def remove(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.ll.remove(node)
            del self.cache[key]
            self.size -= 1

    def evict(self):
        node = self.ll.pop()
        result = node.value
        del self.cache[node.key]
        self.size -= 1
        return result

if __name__=="__main__":
    cache = LRU_cache(4)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    cache.put("d", 4)
    cache.put("e", 5)
    print(cache.get("b"))
    print(cache.get("c"))
    cache.put("f", 6)
    print(cache.get("a"))
    print(cache.get("c"))
    print(cache.ll)
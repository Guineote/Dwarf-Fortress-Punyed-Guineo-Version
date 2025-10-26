class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def add(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1
    
    def remove(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                
                self.size -= 1
                return True
            current = current.next
        return False
    
    def remove_first(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return data
    
    def is_empty(self):
        return self.head is None
    
    def __len__(self):
        return self.size
    
    def iterate(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def find(self, condition):
        for item in self.iterate():
            if condition(item):
                return item
        return None


class Queue:
    def __init__(self):
        self.list = LinkedList()
    
    def enqueue(self, data):
        self.list.add(data)
    
    def dequeue(self):
        return self.list.remove_first()
    
    def is_empty(self):
        return self.list.is_empty()
    
    def size(self):
        return len(self.list)
    
    def iterate(self):
        return self.list.iterate()


class Deque:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def add_front(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
    
    def add_back(self, data):
        new_node = Node(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def remove_front(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return data
    
    def remove_back(self):
        if not self.tail:
            return None
        data = self.tail.data
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.size -= 1
        return data
    
    def is_empty(self):
        return self.head is None
    
    def __len__(self):
        return self.size
    
    def iterate(self):
        current = self.head
        while current:
            yield current.data
            current = current.next


class Heap:
    def __init__(self):
        self.elements = []
    
    def _parent(self, i):
        return (i - 1) // 2
    
    def _left_child(self, i):
        return 2 * i + 1
    
    def _right_child(self, i):
        return 2 * i + 2
    
    def _swap(self, i, j):
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]
    
    def _heapify_up(self, i):
        while i > 0:
            parent = self._parent(i)
            if self.elements[i][0] < self.elements[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break
    
    def _heapify_down(self, i):
        while True:
            smallest = i
            left = self._left_child(i)
            right = self._right_child(i)
            
            if left < len(self.elements) and self.elements[left][0] < self.elements[smallest][0]:
                smallest = left
            if right < len(self.elements) and self.elements[right][0] < self.elements[smallest][0]:
                smallest = right
            
            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break
    
    def insert(self, priority, data):
        self.elements.append((priority, data))
        self._heapify_up(len(self.elements) - 1)
    
    def extract_min(self):
        if not self.elements:
            return None
        if len(self.elements) == 1:
            return self.elements.pop()[1]
        
        minimum = self.elements[0][1]
        self.elements[0] = self.elements.pop()
        self._heapify_down(0)
        return minimum
    
    def is_empty(self):
        return len(self.elements) == 0
    
    def size(self):
        return len(self.elements)


class PriorityQueue:
    def __init__(self):
        self.heap = Heap()
    
    def enqueue(self, priority, data):
        self.heap.insert(priority, data)
    
    def dequeue(self):
        return self.heap.extract_min()
    
    def is_empty(self):
        return self.heap.is_empty()
    
    def size(self):
        return self.heap.size()


class HashTable:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.table = [LinkedList() for _ in range(capacity)]
        self.size = 0
    
    def _hash(self, key):
        return hash(key) % self.capacity
    
    def insert(self, key, value):
        index = self._hash(key)
        linked_list = self.table[index]
        
        for item in linked_list.iterate():
            if item[0] == key:
                item[1] = value
                return
        
        linked_list.add((key, value))
        self.size += 1
    
    def get(self, key):
        index = self._hash(key)
        linked_list = self.table[index]
        
        for item in linked_list.iterate():
            if item[0] == key:
                return item[1]
        return None
    
    def contains(self, key):
        return self.get(key) is not None
    
    def remove(self, key):
        index = self._hash(key)
        linked_list = self.table[index]
        
        for item in linked_list.iterate():
            if item[0] == key:
                linked_list.remove(item)
                self.size -= 1
                return True
        return False
    
    def keys(self):
        result = LinkedList()
        for linked_list in self.table:
            for item in linked_list.iterate():
                result.add(item[0])
        return result
    
    def values(self):
        result = LinkedList()
        for linked_list in self.table:
            for item in linked_list.iterate():
                result.add(item[1])
        return result
    
    def items(self):
        result = LinkedList()
        for linked_list in self.table:
            for item in linked_list.iterate():
                result.add(item)
        return result

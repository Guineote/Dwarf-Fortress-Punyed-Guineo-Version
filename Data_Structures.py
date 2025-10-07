class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class ListaEnlazada:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def remove_first(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self.size -= 1
        return data
    
    def is_empty(self):
        return self.head is None
    
    def __length__(self):
        return self.size
    
    def iterate(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

class Queue:
    def __init__(self):
        self.list = ListaEnlazada()
    
    def entailr(self, data):
        self.list.append(data)
    
    def desentailr(self):
        return self.list.remove_first()
    
    def is_empty(self):
        return self.list.is_empty()
    
    def len(self):
        return len(self.list)
    
    def iterate(self):
        return self.list.iterate()

class DeQue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def add_first(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
    
    def add_last(self, data):
        new_node = Node(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
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
    
    def remove_last(self):
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
            min = i
            left = self._left_child(i)
            right = self._right_child(i)
            
            if left < len(self.elements) and self.elements[left][0] < self.elements[min][0]:
                min = left
            if right < len(self.elements) and self.elements[right][0] < self.elements[min][0]:
                min = right
            
            if min != i:
                self._swap(i, min)
                i = min
            else:
                break
    
    def insert(self, priority, data):
        self.elements.append((priority, data))
        self._heapify_up(len(self.elements) - 1)
    
    def get_min(self):
        if not self.elements:
            return None
        if len(self.elements) == 1:
            return self.elements.pop()[1]
        
        min = self.elements[0][1]
        self.elements[0] = self.elements.pop()
        self._heapify_down(0)
        return min
    
    def is_empty(self):
        return len(self.elements) == 0
    
    def size(self):
        return len(self.elements)

class PriorityQueue:
    def __init__(self):
        self.heap = Heap()
    
    def entailr(self, priority, data):
        self.heap.insert(priority, data)
    
    def desentailr(self):
        return self.heap.get_min()
    
    def is_empty(self):
        return self.heap.is_empty()
    
    def size(self):
        return self.heap.size()

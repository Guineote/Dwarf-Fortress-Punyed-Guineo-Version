from data_structures import *
from enums import *

class JobManager:
    def __init__(self):
        self.pending_tasks = PriorityQueue()      
        self.active_tasks = HashTable()           
        self.completed_tasks = LinkedList()
        self.failed_tasks = LinkedList()
        self.task_buffer = Queue()              
    
    def add_task(self, task):
        self.task_buffer.enqueue(task)
    
    def process_buffer(self):
        while not self.task_buffer.is_empty():
            task = self.task_buffer.dequeue()
            priority_score = task.get_priority_score()
            self.pending_tasks.enqueue(priority_score, task)
    
    def get_next_task_for(self, character):
        if not self.pending_tasks.is_empty():
            task = self.pending_tasks.dequeue()
            if task.can_be_performed_by(character):
                return task
            else:
                self.pending_tasks.enqueue(task.get_priority_score(), task)
                return None
        return None
    
    def assign_task(self, task, character):
        task.assigned_to = character.name
        character.is_occupied = True
        character.current_activity = task.task_type
        
        self.active_tasks.insert(character.name, task)
    
    def update_active_tasks(self, time_units=1.0):
        completed_chars = LinkedList()
        
        for item in self.active_tasks.items().iterate():
            char_name, task = item
            task.advance_progress(time_units)
            
            if task.is_completed:
                completed_chars.add(char_name)
                self.completed_tasks.add(task)
        
        for char_name in completed_chars.iterate():
            self.active_tasks.remove(char_name)
    
    def get_statistics(self):
        stats = HashTable()
        stats.insert("pending", self.pending_tasks.size())
        stats.insert("active", self.active_tasks.size)
        stats.insert("completed", len(self.completed_tasks))
        stats.insert("failed", len(self.failed_tasks))
        return stats

#from data_structures import *
#from enums import *

from Classes.data_structures import *
from Classes.enums import *
import random

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
        character.is_busy = True
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
    
    def assign_best_dwarf(self, task, dwarves):
        best_dwarf = None
        best_score = -1

        for dwarf in dwarves:
            if dwarf.is_busy:
                continue  # saltar enanos ocupados

            # Calcular habilidad promedio
            stats = dwarf.stats
            stat_score = (stats['strength'] + stats['agility'] + stats['intelligence']) / 3

            # Ponderar si el oficio coincide con la tarea
            skill_match = 1.5 if task.required_skill and task.required_skill.lower() in dwarf.occupation.value.lower() else 1.0

            # Obtener felicidad (si aún no tienes un sistema de felicidad, puedes usar un valor aleatorio por ahora)
            happiness_score = getattr(dwarf, 'happiness', random.randint(40, 100))

            # Calcular puntaje total
            total_score = stat_score * skill_match + (happiness_score / 10)

            if total_score > best_score:
                best_score = total_score
                best_dwarf = dwarf

        if best_dwarf:
            best_dwarf.is_busy = True
            best_dwarf.current_activity = task.task_type
            task.assigned_to = best_dwarf.name
            print(f"🛠️ El enano {best_dwarf.name} ha sido asignado a {task.task_type.upper()} (Puntaje: {best_score:.2f})")
        else:
            print("⚠️ No hay enanos disponibles para esta tarea.")

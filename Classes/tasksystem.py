#from data_structures import *
#from enums import *
from Classes.data_structures import *
from Classes.enums import *

class TaskType:
    EAT = "eat"
    DRINK = "drink"
    SLEEP = "sleep"
    CHOP_TREE = "chop_tree"
    MINE_ORE = "mine_ore"
    COLLECT_WATER = "collect_water"
    HUNT_ANIMAL = "hunt_animal"
    BUILD = "Construir"
    SOCIALIZE = "socialize"
    ATTACK_DRAGON = "attack_dragon"
    RANDOM_EVENT = "random_event"
    ATTACK_MINOTAUR = "attack_minotaur"
    RANDOM_EVENT = "random_event"
    
class TaskPriority:
    CRITICAL = 0
    URGENT = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    IDLE = 5
    
    @staticmethod
    def get_name(value):
        names = {0: "CRITICAL", 1: "URGENT", 2: "HIGH", 3: "NORMAL", 4: "LOW", 5: "IDLE"}
        return names.get(value, "UNKNOWN")

class Task:
    def __init__(self, task_type, priority=3, duration=1.0, required_skill=None):
        self.task_type = task_type
        self.priority = priority
        self.duration = duration
        self.required_skill = required_skill
        self.assigned_to = None
        self.progress = 0.0
        self.is_completed = False
        self.created_time = 0
    
    def can_be_performed_by(self, character):
        if self.assigned_to and self.assigned_to != character.name:
            return False
        
        if character.is_busy:
            return False
        
        if self.required_skill:
            if hasattr(character, 'occupation'):
                if self.required_skill.lower() not in character.occupation.value.lower():
                    return False
        
        return True
    
    def advance_progress(self, amount):
        self.progress += amount
        if self.progress >= self.duration:
            self.is_completed = True
    
    def get_priority_score(self):
        base = self.priority * 100
        age_penalty = self.created_time * 0.1
        return base - age_penalty

    def process_buffer(self):
        if not self.task_buffer:
            return
        
        for task in self.task_buffer[:]:
            # Buscar un enano libre
            free_dwarf = next((d for d in self.colony.dwarves if not d.is_busy), None)
            if free_dwarf:
                free_dwarf.assign_task(task)
                print(f"🪓 Tarea '{task.task_type.name}' asignada a {free_dwarf.name}")
                self.task_buffer.remove(task)
            else:
                print("⚠️ No hay enanos libres para esta tarea.")
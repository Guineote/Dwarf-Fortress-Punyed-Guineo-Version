#from data_structures import *
#from enums import *
#from jobManager import *
#from needsystem import *
#from tasksystem import *

from Classes.data_structures import *
from Classes.enums import *
from Classes.jobManager import *
from Classes.needsystem import *
from Classes.tasksystem import *


class DecisionMaker:
    def __init__(self, colony):
        self.colony = colony
        self.job_manager = JobManager()
        self.decision_history = Deque()
        self.max_history = 50
    
    def evaluate_character_state(self, character):
        if not hasattr(character, 'needs_system'):
            character.needs_system = NeedsSystem()
        
        state = HashTable()
        state.insert("critical_needs", character.needs_system.get_critical_needs())
        state.insert("most_urgent_need", character.needs_system.get_most_urgent_need())
        state.insert("happiness", character.needs_system.get_overall_happiness())
        
        critical_count = len(state.get("critical_needs"))
        happiness = state.get("happiness")
        can_work = critical_count == 0 and happiness > 30
        state.insert("can_work", can_work)
        
        return state
    
    def generate_need_based_task(self, character, need_type):
        if need_type == NeedType.HUNGER:
            return Task(TaskType.EAT, TaskPriority.CRITICAL, duration=0.5)
        elif need_type == NeedType.THIRST:
            return Task(TaskType.DRINK, TaskPriority.CRITICAL, duration=0.3)
        elif need_type == NeedType.SLEEP:
            return Task(TaskType.SLEEP, TaskPriority.URGENT, duration=2.0)
        elif need_type == NeedType.SOCIAL:
            return Task(TaskType.SOCIALIZE, TaskPriority.LOW, duration=1.0)
        elif need_type == NeedType.SAFETY:
            return Task(TaskType.DEFEND_COLONY, TaskPriority.CRITICAL, duration=1.0)
        else:
            return Task(TaskType.IDLE, TaskPriority.IDLE)
    
    def generate_colony_tasks(self, colony_state):
        water = colony_state.get("water") or 0
        water_needed = colony_state.get("water_needed") or 50
        
        if water < water_needed:
            for _ in range(2):
                task = Task(TaskType.COLLECT_WATER, TaskPriority.HIGH,
                            duration=2.0, required_skill="fisherman")
                self.job_manager.add_task(task)
        
        food = colony_state.get("food") or 0
        food_needed = colony_state.get("food_needed") or 50
        
        if food < food_needed:
            task = Task(TaskType.HUNT_ANIMAL, TaskPriority.HIGH,
                        duration=3.0, required_skill="hunter")
            self.job_manager.add_task(task)
            
            task = Task(TaskType.FISH, TaskPriority.HIGH,
                        duration=2.5, required_skill="fisherman")
            self.job_manager.add_task(task)
        
        wood = colony_state.get("wood") or 0
        wood_needed = colony_state.get("wood_needed") or 30
        
        if wood < wood_needed:
            for _ in range(2):
                task = Task(TaskType.CHOP_TREE, TaskPriority.NORMAL,
                            duration=3.0, required_skill="lumberjack")
                self.job_manager.add_task(task)
        
        under_attack = colony_state.get("under_attack") or False
        if under_attack:
            for _ in range(3):
                task = Task(TaskType.DEFEND_COLONY, TaskPriority.CRITICAL,
                            duration=2.0, required_skill="warrior")
                self.job_manager.add_task(task)
        
        self.job_manager.process_buffer()

        if self.colony.event_system.active_events:
            for _ in range(2):  # Ej. 2 tasks para warriors
                task = Task(TaskType.RANDOM_EVENT, TaskPriority.CRITICAL, duration=5.0, required_skill="warrior")
                self.job_manager.add_task(task)
        
    def make_decision(self, character):
        state = self.evaluate_character_state(character)
        
        critical_needs = state.get("critical_needs")
        if len(critical_needs) > 0:
            first_critical = None
            for need in critical_needs.iterate():
                first_critical = need
                break
            
            if first_critical:
                task = self.generate_need_based_task(character, first_critical.need_type)
                self._record_decision(character.name, "satisfy_critical_need", task.task_type)
                return task
        
        if not state.get("can_work"):
            urgent_need = state.get("most_urgent_need")
            task = self.generate_need_based_task(character, urgent_need)
            self._record_decision(character.name, "satisfy_urgent_need", task.task_type)
            return task
        
        task = self.job_manager.get_next_task_for(character)
        if task:
            self._record_decision(character.name, "perform_colony_task", task.task_type)
            return task
        
        import random
        idle_types = [TaskType.SOCIALIZE, TaskType.TRAIN_COMBAT, TaskType.IDLE]
        chosen = random.choice(idle_types)
        task = Task(chosen, TaskPriority.LOW, duration=1.0)
        self._record_decision(character.name, "idle_activity", task.task_type)
        return task
    
    def _record_decision(self, char_name, decision_type, task_type):
        decision = HashTable()
        decision.insert("character", char_name)
        decision.insert("decision", decision_type)
        decision.insert("task", task_type)
        
        self.decision_history.add_back(decision)
        
        if len(self.decision_history) > self.max_history:
            self.decision_history.remove_front()
    
    def execute_decision(self, character, task):
        if task.task_type in [TaskType.EAT, TaskType.DRINK, TaskType.SLEEP]:
            self._execute_personal_task(character, task)
        else:
            self.job_manager.assign_task(task, character)
    
    def _execute_personal_task(self, character, task):
        if task.task_type == TaskType.EAT:
            character.needs_system.satisfy_need(NeedType.HUNGER, 50)
        elif task.task_type == TaskType.DRINK:
            character.needs_system.satisfy_need(NeedType.THIRST, 60)
        elif task.task_type == TaskType.SLEEP:
            character.needs_system.satisfy_need(NeedType.SLEEP, 80)
            character.needs_system.satisfy_need(NeedType.COMFORT, 30)
        
        character.is_occupied = False
        character.current_activity = None
    
    def update_all_characters(self, characters_list, time_units=1.0):
        for character in characters_list.iterate():
            if not hasattr(character, 'needs_system'):
                character.needs_system = NeedsSystem()
            
            character.needs_system.update(time_units)
        
        self.job_manager.update_active_tasks(time_units)
        
        for character in characters_list.iterate():
            if not character.is_occupied:
                task = self.make_decision(character)
                if task:
                    self.execute_decision(character, task)
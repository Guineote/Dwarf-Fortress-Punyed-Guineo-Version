#from data_structures import *
#from enums import *

from Classes.data_structures import *
from Classes.enums import *


class NeedType:
    HUNGER = "hunger"
    THIRST = "thirst"
    SLEEP = "sleep"
    SAFETY = "safety"
    SOCIAL = "social"
    WORK_SATISFACTION = "work_satisfaction"
    COMFORT = "comfort"
    BELONGING = "belonging"
    
    @staticmethod
    def all_types():
        return [
            NeedType.HUNGER, NeedType.THIRST, NeedType.SLEEP,
            NeedType.SAFETY, NeedType.SOCIAL, NeedType.WORK_SATISFACTION,
            NeedType.COMFORT, NeedType.BELONGING
        ]


class Need:
    def __init__(self, need_type, value=100.0):
        self.need_type = need_type
        self.value = value
        self.max_value = 100.0
        self.decay_rate = self._get_decay_rate()
    
    def _get_decay_rate(self):
        if self.need_type == NeedType.HUNGER:
            return 2.0
        elif self.need_type == NeedType.THIRST:
            return 3.0
        elif self.need_type == NeedType.SLEEP:
            return 1.5
        elif self.need_type == NeedType.SOCIAL:
            return 0.5
        elif self.need_type == NeedType.WORK_SATISFACTION:
            return 0.3
        elif self.need_type == NeedType.COMFORT:
            return 0.2
        elif self.need_type == NeedType.BELONGING:
            return 0.1
        else:
            return 0.0
    
    def decay(self, time_units=1.0):
        self.value = max(0, self.value - (self.decay_rate * time_units))
    
    def satisfy(self, amount):
        self.value = min(self.max_value, self.value + amount)
    
    def get_urgency(self):
        return 100 - self.value
    
    def is_critical(self):
        return self.value < 20.0
    
    def is_urgent(self):
        return self.value < 50.0


class NeedsSystem:
    def __init__(self):
        self.needs = HashTable(capacity=20)
        self._initialize_needs()
    
    def _initialize_needs(self):
        for need_type in NeedType.all_types():
            self.needs.insert(need_type, Need(need_type))
    
    def update(self, time_units=1.0):
        for item in self.needs.items().iterate():
            need_type, need = item
            need.decay(time_units)
    
    def get_most_urgent_need(self):
        most_urgent = None
        highest_urgency = -1
        
        for item in self.needs.items().iterate():
            need_type, need = item
            urgency = need.get_urgency()
            if urgency > highest_urgency:
                highest_urgency = urgency
                most_urgent = need_type
        
        return most_urgent
    
    def get_critical_needs(self):
        critical = LinkedList()
        for item in self.needs.items().iterate():
            need_type, need = item
            if need.is_critical():
                critical.add(need)
        return critical
    
    def satisfy_need(self, need_type, amount):
        need = self.needs.get(need_type)
        if need:
            need.satisfy(amount)
    
    def get_overall_happiness(self):
        total = 0.0
        count = 0
        for item in self.needs.items().iterate():
            need_type, need = item
            total += need.value
            count += 1
        return total / count if count > 0 else 0
class Stats:
    def __init__(self):
        self.strength: float = 10.0
        self.health: float = 100.0
        self.max_health: float = 100.0
        self.endurance: float = 10.0
        self.dexterity: float = 10.0
        self.intelligence: float = 10.0
        self.charisma: float = 10.0
        self.accuracy: float = 50.0  # Percentage
        self.luck: float = 10.0
        self.speed: float = 10.0
        self.crit_chance: float = 5.0  # Percentage
        self.armor: float = 0.0
    
    def apply_modifier(self, stat_name: str, value: float):
        if hasattr(self, stat_name):
            current_value = getattr(self, stat_name)
            setattr(self, stat_name, current_value + value)
    
    def get_stat(self, stat_name: str) -> float:
        return getattr(self, stat_name, 0.0)
    
    def __str__(self):
        return f"STR:{self.strength:.0f} HP:{self.health:.0f}/{self.max_health:.0f} DEX:{self.dexterity:.0f} INT:{self.intelligence:.0f}"
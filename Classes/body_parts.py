from typing import Optional
#from enums import BodyPart
#from equipment import Armor
from Classes.enums import BodyPart
from Classes.equipment import Armor


class BodyPartStatus:
    def __init__(self, part: BodyPart):
        self.part = part
        self.health = 100.0
        self.armor: Optional[Armor] = None
        self.is_crippled = False
        self.is_bleeding = False
    
    def take_damage(self, damage: float, ignore_armor: bool = False) -> float:
        effective_damage = damage
        
        if not ignore_armor and self.armor:
            armor_reduction = self.armor.get_effective_defense()
            effective_damage = max(0, damage - armor_reduction)
            self.armor.durability -= damage * 0.1
        
        self.health -= effective_damage
        
        if self.health <= 0:
            self.health = 0
            self.is_crippled = True
        
        return effective_damage
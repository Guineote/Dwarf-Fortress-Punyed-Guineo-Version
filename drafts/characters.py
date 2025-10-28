from typing import Dict, List, Optional
from enums import Gender, Race, Occupation, WeaponType, BodyPart, ArmorType
from stats import Stats
from equipment import Weapon, Armor, Amulet
from body_parts import BodyPartStatus

class SentientBeing:
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        self.name = name
        self.age = age
        self.gender = gender
        self.race = race
        self.level = 1
        self.experience = 0
        self.height = 170.0
        
        self.stats = Stats()
        
        self.body_parts: Dict[BodyPart, BodyPartStatus] = self._initialize_body_parts()
        self.weapons: List[Weapon] = []
        self.weapon_mastery: Dict[WeaponType, float] = {}  # Percentage 0-100

        #Needs to be further finishes
        self.traits: List[str] = []
        
        self.is_occupied = False
        self.is_alive = True
        self.current_activity: Optional[str] = None
        self.morale = 80.0
        
        self._apply_race_modifiers()
    
    def _initialize_body_parts(self) -> Dict[BodyPart, BodyPartStatus]:
        return {part: BodyPartStatus(part) for part in BodyPart}
    
    def _apply_race_modifiers(self):
        race_modifiers = {
            Race.DWARF: {"dexterity": 1, "strength": 2, "health": 10, "max_health": 10},
            Race.WIZARD: {"intelligence": 4, "accuracy": 1, "luck": 1, "strength": -1, "health": -10, "max_health": -10},
            Race.ELF: {"intelligence": 2, "charisma": 2},
            Race.ORC: {"strength": 3, "health": 30, "max_health": 30, "intelligence": -1, "charisma": -1},
            Race.OGRE: {"strength": 4, "health": 40, "max_health": 40, "intelligence": -2, "charisma": -2},
            Race.GOBLIN: {"strength": 2, "speed": 3, "health": 10, "max_health": 10, "intelligence": -1, "charisma": -1},
            Race.HUMAN: {"intelligence": 1, "strength": 1, "health": 10, "max_health": 10, "luck": 1},
            Race.TROLL: {"strength": 2, "health": 20, "max_health": 20, "armor": 2, "intelligence": -2}
        }
        
        if self.race in race_modifiers:
            for stat, value in race_modifiers[self.race].items():
                self.stats.apply_modifier(stat, value)
    
    def equip_weapon(self, weapon: Weapon):
        if weapon.two_handed and len(self.weapons) > 0:
            self.weapons.clear()
        elif not weapon.two_handed and len(self.weapons) >= 2:
            self.weapons.pop(0)
        
        self.weapons.append(weapon)
    
    def equip_armor(self, armor: Armor):
        if armor.body_part and armor.body_part in self.body_parts:
            self.body_parts[armor.body_part].armor = armor
            
            # Apply amulet stat bonuses
            if isinstance(armor, Amulet) and hasattr(armor, 'stat_bonuses'):
                for stat, bonus in armor.stat_bonuses.items():
                    self.stats.apply_modifier(stat, bonus)
            
            # Also equip to mirrored body part if applicable
            mirror_parts = {
                BodyPart.LEFT_ARM: BodyPart.RIGHT_ARM,
                BodyPart.RIGHT_ARM: BodyPart.LEFT_ARM,
                BodyPart.LEFT_HAND: BodyPart.RIGHT_HAND,
                BodyPart.RIGHT_HAND: BodyPart.LEFT_HAND,
                BodyPart.LEFT_LEG: BodyPart.RIGHT_LEG,
                BodyPart.RIGHT_LEG: BodyPart.LEFT_LEG,
                BodyPart.LEFT_FOOT: BodyPart.RIGHT_FOOT,
                BodyPart.RIGHT_FOOT: BodyPart.LEFT_FOOT
            }
            if armor.body_part in mirror_parts:
                self.body_parts[mirror_parts[armor.body_part]].armor = armor
    
    def calculate_total_armor(self) -> float:
        total = self.stats.armor
        for body_part_status in self.body_parts.values():
            if body_part_status.armor:
                total += body_part_status.armor.get_effective_defense()
        return total
    
    def take_damage(self, damage: float, is_crit: bool = False, target_part: Optional[BodyPart] = None) -> float:
        if not self.is_alive:
            return 0
        
        if is_crit and target_part:
            actual_damage = self.body_parts[target_part].take_damage(damage, ignore_armor=True)
        elif target_part:
            actual_damage = self.body_parts[target_part].take_damage(damage, ignore_armor=False)
        else:
            armor_reduction = self.calculate_total_armor() * 0.1
            actual_damage = max(0, damage - armor_reduction)
        
        self.stats.health -= actual_damage
        
        if self.stats.health <= 0:
            self.stats.health = 0
            self.is_alive = False
        
        return actual_damage
    
    def heal(self, amount: float, healer_intelligence: float = 0):
        intelligence_bonus = 1 + (healer_intelligence * 0.01)
        actual_heal = amount * intelligence_bonus
        
        self.stats.health = min(self.stats.max_health, self.stats.health + actual_heal)
        return actual_heal
    
    def gain_experience(self, exp: float):
        self.experience += exp
        exp_needed = 100 * self.level
        
        if self.experience >= exp_needed:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.experience = 0
        
        self.stats.max_health += 10
        self.stats.health = self.stats.max_health
        self.stats.strength += 1
        self.stats.dexterity += 0.5
        self.stats.endurance += 0.5
        
        self.morale += 10
    
    def improve_weapon_mastery(self, weapon_type: WeaponType, amount: float):
        current = self.weapon_mastery.get(weapon_type, 0)
        self.weapon_mastery[weapon_type] = min(100, current + amount)
    
    def get_attack_power(self) -> float:
        base_damage = self.stats.strength
        
        if self.weapons:
            weapon = self.weapons[0]
            weapon_damage = weapon.get_effective_damage()
            mastery_bonus = self.weapon_mastery.get(weapon.weapon_type, 0) / 100
            base_damage += weapon_damage * (1 + mastery_bonus)
        
        return base_damage
    
    def get_hit_chance(self) -> float:
        base_accuracy = self.stats.accuracy
        
        if self.weapons:
            weapon = self.weapons[0]
            base_accuracy += weapon.accuracy_bonus
        
        luck_bonus = self.stats.luck * 0.5
        return min(95, base_accuracy + luck_bonus)
    
    def get_dodge_chance(self) -> float: #Needs to be revised
        return min(50, (self.stats.speed * 2) + (self.stats.luck * 0.5))
    
    def get_crit_chance(self) -> float:
        base_crit = self.stats.crit_chance
        
        if self.weapons:
            weapon = self.weapons[0]
            base_crit += weapon.crit_bonus
        
        luck_bonus = self.stats.luck * 0.3
        return min(50, base_crit + luck_bonus)
    
    def __str__(self):
        status = "ALIVE" if self.is_alive else "DEAD"
        return f"{self.name} | {self.race.value} Lv{self.level} | {status} | {self.stats}"
    
#Clases

class Lumberjack(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("strength", 2)
        self.stats.apply_modifier("dexterity", 2)
        self.occupation = Occupation.LUMBERJACK

class Fisherman(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("strength", 1)
        self.stats.apply_modifier("dexterity", 1)
        self.stats.apply_modifier("luck", 2)
        self.occupation = Occupation.FISHERMAN

class Hunter(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("strength", 1)
        self.stats.apply_modifier("luck", 1)
        self.stats.apply_modifier("speed", 1)
        self.stats.apply_modifier("accuracy", 1)
        self.occupation = Occupation.HUNTER

class Builder(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("strength", 2)
        self.stats.apply_modifier("endurance", 1)
        self.stats.apply_modifier("dexterity", 1)
        self.occupation = Occupation.BUILDER

class Farmer(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("strength", 1)
        self.stats.apply_modifier("endurance", 1)
        self.stats.apply_modifier("luck", 1)
        self.stats.apply_modifier("dexterity", 1)
        self.occupation = Occupation.FARMER

class Medic(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("intelligence", 2)
        self.stats.apply_modifier("luck", 1)
        self.stats.apply_modifier("dexterity", 3)
        self.occupation = Occupation.MEDIC
    
    def heal_target(self, target: SentientBeing, base_amount: float) -> float:
        return target.heal(base_amount, self.stats.intelligence)

class Brewer(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("luck", 3)
        self.stats.apply_modifier("intelligence", 1)
        self.occupation = Occupation.BREWER

class Blacksmith(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("dexterity", 2)
        self.stats.apply_modifier("strength", 1)
        self.stats.apply_modifier("luck", 1)
        self.occupation = Occupation.BLACKSMITH

class Warrior(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("health", 20)
        self.stats.apply_modifier("max_health", 20)
        self.stats.apply_modifier("strength", 2)
        self.stats.apply_modifier("dexterity", 1)
        self.occupation = Occupation.WARRIOR

class Archer(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("speed", 2)
        self.stats.apply_modifier("accuracy", 2)
        self.occupation = Occupation.ARCHER

class Merchant(SentientBeing):
    def __init__(self, name: str, age: int, gender: Gender, race: Race):
        super().__init__(name, age, gender, race)
        self.stats.apply_modifier("charisma", 2)
        self.stats.apply_modifier("intelligence", 1)
        self.stats.apply_modifier("luck", 1)
        self.occupation = Occupation.MERCHANT
        self.inventory: Dict[str, int] = {}
        self.gold = 100
    
    def get_trade_modifier(self) -> float:
        return 1 + (self.stats.charisma * 0.02)

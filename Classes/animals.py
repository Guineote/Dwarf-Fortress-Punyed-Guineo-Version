import random
from typing import Dict
#from enums import AnimalType
from Classes.enums import AnimalType

class Animal:
    def __init__(self, animal_type: AnimalType, health: float, speed: float = 10.0):
        self.animal_type = animal_type
        self.health = health
        self.max_health = health
        self.speed = speed
        self.is_alive = True
        self.is_aggressive = False
        self.is_passive = True
        self.is_territorial = False
        self.is_occupied = False
        
        self.drops: Dict[str, tuple] = {}
        
        self.can_be_tamed = False
        self.can_carry_load = False
        self.can_be_ridden = False
        self.can_produce_resources = False
        self.resource_production: Dict[str, float] = {}
    
    def take_damage(self, damage: float) -> float:
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
        return damage
    
    def get_drops(self) -> Dict[str, int]:
        if not self.is_alive:
            result = {}
            for item, (min_qty, max_qty) in self.drops.items():
                result[item] = random.randint(min_qty, max_qty)
            return result
        return {}
    
    def produce_daily_resource(self) -> Dict[str, float]:
        if self.is_alive and self.can_produce_resources:
            return self.resource_production.copy()
        return {}
    
    def __str__(self):
        status = "ALIVE" if self.is_alive else "DEAD"
        return f"{self.animal_type.value.capitalize()} | HP:{self.health:.0f}/{self.max_health:.0f} | {status}"

class Squirrel(Animal):
    def __init__(self):
        super().__init__(AnimalType.SQUIRREL, health=15, speed=25)
        self.drops = {
            "nuts": (1, 3),
            "wheat_seeds": (0, 1),
            "barley_seeds": (0, 1),
            "corn_seeds": (0, 1),
            "squirrel_tail": (1, 1)
        }
        self.damage = 2
        self.accuracy = 45

class Rabbit(Animal):
    def __init__(self):
        super().__init__(AnimalType.RABBIT, health=20, speed=30)
        self.drops = {
            "hide": (1, 1),
            "meat": (1, 2),
            "rabbit_foot": (0, 1)
        }

class Chicken(Animal):
    def __init__(self):
        super().__init__(AnimalType.CHICKEN, health=10, speed=15)
        self.drops = {
            "meat": (1, 2),
            "bones": (1, 3),
            "feathers": (2, 5)
        }
        self.can_produce_resources = True
        self.resource_production = {"eggs": 1.0}

class Frog(Animal):
    def __init__(self):
        super().__init__(AnimalType.FROG, health=8, speed=12)
        self.drops = {
            "meat": (1, 1),
            "frog_skin": (1, 1),
            "poison": (0, 1)
        }

class Sheep(Animal):
    def __init__(self):
        super().__init__(AnimalType.SHEEP, health=40, speed=12)
        self.drops = {
            "wool": (2, 4),
            "meat": (3, 5),
            "bones": (2, 4)
        }
        self.can_be_tamed = True
        self.can_produce_resources = True
        self.resource_production = {"wool": 0.5}

class Pig(Animal):
    def __init__(self):
        super().__init__(AnimalType.PIG, health=45, speed=10)
        self.drops = {
            "meat": (4, 6),
            "fat": (2, 3),
            "bones": (2, 4),
            "leather": (1, 2)
        }

class Cow(Animal):
    def __init__(self):
        super().__init__(AnimalType.COW, health=60, speed=8)
        self.drops = {
            "meat": (6, 10),
            "leather": (2, 4),
            "bones": (3, 6)
        }
        self.can_produce_resources = True
        self.resource_production = {"milk": 1.0}

class Ox(Animal): #buey
    def __init__(self):
        super().__init__(AnimalType.OX, health=70, speed=7)
        self.drops = {
            "meat": (7, 12),
            "bones": (4, 7),
            "leather": (2, 4),
            "horn": (1, 2)
        }
        self.can_carry_load = True
        self.can_be_tamed = True

class Goat(Animal):
    def __init__(self):
        super().__init__(AnimalType.GOAT, health=50, speed=15)
        self.is_territorial = True
        self.damage = 15
        self.drops = {
            "meat": (3, 5),
            "leather": (1, 2),
            "horn": (1, 2)
        }
        self.can_produce_resources = True
        self.resource_production = {"milk": 0.8}

#Agresivosa

class Bull(Animal):
    def __init__(self):
        super().__init__(AnimalType.BULL, health=80, speed=18)
        self.is_aggressive = False
        self.is_passive = False
        self.damage = 35
        self.accuracy = 75
        self.drops = {
            "meat": (8, 14),
            "bones": (5, 8),
            "leather": (3, 5),
            "horn": (2, 2)
        }

class Boar(Animal):
    def __init__(self):
        super().__init__(AnimalType.BOAR, health=55, speed=20)
        self.is_aggressive = True
        self.is_passive = False
        self.damage = 30
        self.accuracy = 70
        self.bleeding_chance = 50
        self.drops = {
            "meat": (5, 8),
            "thick_hide": (2, 3),
            "tusks": (2, 2)
        }

class Bear(Animal):
    def __init__(self):
        super().__init__(AnimalType.BEAR, health=150, speed=15)
        self.is_aggressive = True
        self.is_passive = False
        self.damage = 50
        self.claw_attack = 45
        self.drops = {
            "meat": (10, 15),
            "quality_hide": (3, 5),
            "claws": (4, 4)
        }

class Snake(Animal):
    def __init__(self):
        super().__init__(AnimalType.SNAKE, health=12, speed=15)
        self.is_aggressive = True
        self.is_passive = False
        self.damage = 10
        self.is_venomous = True
        self.drops = {
            "poison": (1, 2),
            "snake_skin": (1, 1),
            "fangs": (2, 2)
        }

class Bee(Animal):
    def __init__(self):
        super().__init__(AnimalType.BEE, health=1, speed=25)
        self.is_aggressive = True
        self.is_passive = False
        self.damage = 5
        self.is_venomous = True
        self.swarm_size = random.randint(5, 20)
        self.drops = {
            "honey": (1, 3),
            "wax": (1, 2)
        }

class Leech(Animal):
    def __init__(self):
        super().__init__(AnimalType.LEECH, health=3, speed=5)
        self.is_parasite = True
        self.damage_per_turn = 2
        self.is_venomous = True
        self.drops = {
            "leech_spit": (1, 1)
        }

class Horse(Animal):
    def __init__(self):
        super().__init__(AnimalType.HORSE, health=70, speed=35)
        self.drops = {
            "leather": (2, 4),
            "bones": (3, 6),
            "meat": (3, 5)
        }
        self.can_be_ridden = True
        self.can_carry_load = True
        self.can_be_tamed = True

class Dog(Animal):
    def __init__(self):
        super().__init__(AnimalType.DOG, health=40, speed=22)
        self.can_be_tamed = True
        self.is_loyal = True
        self.damage = 20
        self.can_guard = True

class Cat(Animal):
    def __init__(self):
        super().__init__(AnimalType.CAT, health=15, speed=20)
        self.can_be_tamed = True
        self.damage = 5
        self.luck_bonus = 5

class Bird(Animal):
    def __init__(self):
        super().__init__(AnimalType.BIRD, health=8, speed=40)
        self.drops = {
            "meat": (1, 1),
            "feathers": (2, 4)
        }
        self.can_be_tamed = True

class Piranha(Animal):
    def __init__(self):
        super().__init__(AnimalType.PIRANHA, health=10, speed=25)
        self.is_aggressive = True
        self.is_passive = False
        self.swarm_size = random.randint(8, 20)
        self.damage = 8
        self.drops = {
            "meat": (1, 1),
            "sharp_teeth": (1, 2)
        }

class Shark(Animal):
    def __init__(self):
        super().__init__(AnimalType.SHARK, health=120, speed=30)
        self.is_aggressive = random.choice([True, False])
        self.is_passive = not self.is_aggressive
        self.damage = 45
        self.attracted_to_blood = True
        self.drops = {
            "meat": (8, 12),
            "shark_teeth": (5, 10)
        }

class Whale(Animal):
    def __init__(self):
        super().__init__(AnimalType.WHALE, health=300, speed=15)
        self.is_passive = True
        self.swallow_chance = 30
        self.drops = {
            "meat": (20, 35),
            "bones": (10, 15),
            "whale_fat": (15, 25)
        }

#BOSS

class Minotaur(Animal):
    def __init__(self):
        super().__init__(AnimalType.MINOTAUR, health=500, speed=12)
        self.is_aggressive = True
        self.is_passive = False
        self.is_boss = True
        self.axe_damage = 80
        self.charge_damage = 60
        self.accuracy = 70
        self.drops = {
            "meat": (15, 25),
            "minotaur_horns": (2, 2),
            "resistant_hide": (5, 8),
            "minotaur_axe": (0, 1),
            "leather": (8, 12)
        }

class Dragon(Animal):
    def __init__(self):
        super().__init__(AnimalType.DRAGON, health=1000, speed=20)
        self.is_aggressive = True
        self.is_passive = False
        self.is_boss = True
        self.fire_breath_damage = 100
        self.claw_damage = 70
        self.bite_damage = 60
        self.armor = 50
        self.can_speak = True
        self.drops = {
            "dragon_heart": (1, 1),
            "dragon_scales": (10, 20),
            "gold": (100, 500),
            "bones": (15, 25),
            "dragon_fangs": (4, 4)
        }

class Cyclops(Animal):
    def __init__(self):
        super().__init__(AnimalType.CYCLOPS, health=700, speed=10)
        self.is_aggressive = True
        self.is_passive = False
        self.is_boss = True
        self.club_damage = 90
        self.rock_throw_damage = 70
        self.accuracy = 60
        self.drops = {
            "meat": (20, 30),
            "bones": (12, 18),
            "thick_hide": (8, 12),
            "cyclops_tears": (0, 2)
        }

class Siren(Animal):
    def __init__(self):
        super().__init__(AnimalType.SIREN, health=250, speed=18)
        self.is_aggressive = True
        self.is_passive = False
        self.is_boss = True
        self.hypnotic_song = True
        self.trident_damage = 55
        self.drops = {
            "scales": (5, 10),
            "magical_hair": (3, 5),
            "pearls": (2, 8),
            "trident": (0, 1)
        }
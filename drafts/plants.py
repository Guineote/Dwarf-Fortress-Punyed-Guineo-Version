import random
from typing import Dict, Optional
from enums import TreeType, PlantType

class Tree:
    def __init__(self, tree_type: TreeType, wood_quality: str, wood_amount: tuple):
        self.tree_type = tree_type
        self.wood_quality = wood_quality
        self.wood_amount = wood_amount
        self.is_standing = True
        self.age = random.randint(10, 100)
        self.height = random.uniform(5, 30)
        self.is_occupied = False
        
        self.drops: Dict[str, tuple] = {
            "wood": wood_amount
        }
        
        self.produces_fruit = False
        self.fruit_type: Optional[str] = None
        self.fruit_amount = (0, 0)
        
        self.has_special_bark = False
        self.bark_properties = []
        
        self.produces_resin = False
        self.resin_amount = (0, 0)
        
        self.stores_water = False
        self.water_amount = 0
    
    def chop_down(self) -> Dict[str, int]:
        if self.is_standing:
            self.is_standing = False
            result = {}
            
            for resource, (min_qty, max_qty) in self.drops.items():
                result[resource] = random.randint(min_qty, max_qty)
            
            result["leaves"] = random.randint(5, 15)
            
            if self.produces_fruit and self.fruit_type:
                result[self.fruit_type] = random.randint(*self.fruit_amount)
            
            if self.has_special_bark:
                result["special_bark"] = random.randint(1, 3)
            
            if self.produces_resin:
                result["resin"] = random.randint(*self.resin_amount)
            
            return result
        return {}
    
    def get_water(self) -> int:
        #solo baobab
        if self.stores_water and self.is_standing:
            return self.water_amount
        return 0
    
    def __str__(self):
        status = "Standing" if self.is_standing else "Chopped"
        return f"{self.tree_type.value.capitalize()} Tree | {self.wood_quality} wood | Age:{self.age}y | {status}"

class Oak(Tree):
    def __init__(self):
        super().__init__(TreeType.OAK, wood_quality="hard", wood_amount=(8, 15))
        self.drops["acorns"] = (5, 12)

class Walnut(Tree):
    def __init__(self):
        super().__init__(TreeType.WALNUT, wood_quality="normal", wood_amount=(7, 12))
        self.drops["walnuts"] = (8, 15)
        self.has_special_bark = True
        self.bark_properties = ["medicinal", "magical"]

class Mahogany(Tree):
    def __init__(self):
        super().__init__(TreeType.MAHOGANY, wood_quality="fine", wood_amount=(10, 18))
        self.drops["large_leaves"] = (10, 20)

class Pine(Tree):
    def __init__(self):
        super().__init__(TreeType.PINE, wood_quality="normal", wood_amount=(8, 14))
        self.produces_resin = True
        self.resin_amount = (2, 5)

class Baobab(Tree):
    def __init__(self):
        super().__init__(TreeType.BAOBAB, wood_quality="poor", wood_amount=(5, 10))
        self.stores_water = True
        self.water_amount = random.randint(20, 50)
        self.has_special_bark = True
        self.bark_properties = ["medicinal", "magical"]

class AppleTree(Tree):
    def __init__(self):
        super().__init__(TreeType.APPLE, wood_quality="normal", wood_amount=(6, 10))
        self.produces_fruit = True
        self.fruit_type = "apples"
        self.fruit_amount = (10, 25)

class Olive(Tree):
    def __init__(self):
        super().__init__(TreeType.OLIVE, wood_quality="good", wood_amount=(7, 12))
        self.produces_fruit = True
        self.fruit_type = "olives"
        self.fruit_amount = (15, 30)
        self.drops["olive_oil"] = (1, 3)

class Almond(Tree):
    def __init__(self):
        super().__init__(TreeType.ALMOND, wood_quality="fine", wood_amount=(7, 11))
        self.produces_fruit = True
        self.fruit_type = "almonds"
        self.fruit_amount = (12, 25)

class Plant:
    def __init__(self, plant_type: PlantType, growth_days: int):
        self.plant_type = plant_type
        self.growth_days = growth_days
        self.current_day = 0
        self.is_mature = False
        self.is_harvested = False
        self.is_occupied = False
        self.can_replant = True
        
        self.harvest_yields: Dict[str, tuple] = {}
        
        self.needs_fertile_soil = True
        self.water_requirement = 1.0
    
    def grow(self, days: int = 1):
        if not self.is_mature and not self.is_harvested:
            self.current_day += days
            if self.current_day >= self.growth_days:
                self.is_mature = True
    
    def harvest(self) -> Dict[str, int]:
        if self.is_mature and not self.is_harvested:
            self.is_harvested = True
            result = {}
            
            for resource, (min_qty, max_qty) in self.harvest_yields.items():
                result[resource] = random.randint(min_qty, max_qty)
            
            return result
        return {}
    
    def replant(self):
        if self.can_replant and self.is_harvested:
            self.is_harvested = False
            self.is_mature = False
            self.current_day = 0
            return True
        return False
    
    def __str__(self):
        if self.is_harvested:
            status = "Harvested"
        elif self.is_mature:
            status = "Mature"
        else:
            status = f"Growing ({self.current_day}/{self.growth_days} days)"
        return f"{self.plant_type.value.capitalize()} | {status}"

class Grape(Plant):
    def __init__(self):
        super().__init__(PlantType.GRAPE, growth_days=120)
        self.harvest_yields = {"grapes": (15, 30)}

class Potato(Plant):
    def __init__(self):
        super().__init__(PlantType.POTATO, growth_days=90)
        self.harvest_yields = {"potatoes": (8, 15)}

class Carrot(Plant):
    def __init__(self):
        super().__init__(PlantType.CARROT, growth_days=70)
        self.harvest_yields = {"carrots": (10, 20)}

class Cotton(Plant):
    def __init__(self):
        super().__init__(PlantType.COTTON, growth_days=150)
        self.harvest_yields = {"cotton": (12, 25)}

class Barley(Plant):
    def __init__(self):
        super().__init__(PlantType.BARLEY, growth_days=100)
        self.harvest_yields = {
            "barley_grains": (20, 40),
            "straw": (10, 20)
        }

class Wheat(Plant):
    def __init__(self):
        super().__init__(PlantType.WHEAT, growth_days=110)
        self.harvest_yields = {
            "wheat_grains": (25, 45),
            "straw": (12, 22)
        }

class Sugarcane(Plant):
    def __init__(self):
        super().__init__(PlantType.SUGARCANE, growth_days=365)
        self.harvest_yields = {"sugarcane": (15, 30)}

class Corn(Plant):
    def __init__(self):
        super().__init__(PlantType.CORN, growth_days=85)
        self.harvest_yields = {"corn": (12, 24)}

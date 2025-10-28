from typing import Dict, Optional, List
#from enums import *
from Classes.enums import *


class Structure:
    def __init__(self, name: str, structure_type: StructureType, materials_required: Dict[str, int], capacity: int = 0):
        self.name = name
        self.structure_type = structure_type
        self.materials_required = materials_required
        self.capacity = capacity
        self.is_built = False
        self.durability = 100.0
        self.max_durability = 100.0
        self.workers: List[str] = []
        self.stored_resources: Dict[str, int] = {}
        self.efficiency = 100.0
    
    def construct(self, available_materials: Dict[str, int]) -> bool:
        for material, amount in self.materials_required.items():
            if available_materials.get(material, 0) < amount:
                return False
        
        for material, amount in self.materials_required.items():
            available_materials[material] -= amount
        self.is_built = True
        return True
    
    def take_damage(self, damage: float):
        self.durability -= damage
        if self.durability < 0:
            self.durability = 0
        
        self.efficiency = (self.durability / self.max_durability) * 100
    
    def repair(self, amount: float):
        self.durability = min(self.max_durability, self.durability + amount)
        self.efficiency = (self.durability / self.max_durability) * 100
    
    def __str__(self):
        status = "Built" if self.is_built else "Not Built"
        return f"{self.name} ({self.structure_type.value}) - {status} | Durability: {self.durability:.0f}% | Efficiency: {self.efficiency:.0f}%"    
    
class StorageCenter(Structure):
    def __init__(self):
        materials = {
            "wood": 30,
            "stone": 40,
            "metal_ore": 10
        }
        super().__init__("Storage Center", StructureType.STORAGE_CENTER, materials, capacity=1000)
        self.storage_slots: Dict[str, int] = {}
    
    def add_resource(self, resource: str, amount: int) -> bool:
        total_stored = sum(self.storage_slots.values())
        
        if total_stored + amount <= self.capacity:
            self.storage_slots[resource] = self.storage_slots.get(resource, 0) + amount
            return True
        return False
    
    def remove_resource(self, resource: str, amount: int) -> int:
        available = self.storage_slots.get(resource, 0)
        removed = min(available, amount)
        
        if removed > 0:
            self.storage_slots[resource] -= removed
            if self.storage_slots[resource] == 0:
                del self.storage_slots[resource]
        
        return removed
    
    def get_stored_resources(self) -> Dict[str, int]:
        return self.storage_slots.copy()

class House(Structure):
    def __init__(self, house_id: int):
        materials = {
            "wood": 20,
            "stone": 15,
            "nails": 5
        }
        name = f"House #{house_id}"
        super().__init__(name, StructureType.HOUSE, materials, capacity=4)
        self.inhabitants: List[str] = []
        self.comfort_level = 50.0
    
    def add_inhabitant(self, inhabitant_name: str) -> bool:
        if len(self.inhabitants) < self.capacity:
            self.inhabitants.append(inhabitant_name)
            return True
        return False
    
    def remove_inhabitant(self, inhabitant_name: str) -> bool:
        if inhabitant_name in self.inhabitants:
            self.inhabitants.remove(inhabitant_name)
            return True
        return False
    
    def improve_comfort(self, amount: float):
        self.comfort_level = min(100, self.comfort_level + amount)
    
    def __str__(self):
        return super().__str__() + f" | Inhabitants: {len(self.inhabitants)}/{self.capacity} | Comfort: {self.comfort_level:.0f}%"

class Well(Structure):
    def __init__(self):
        materials = {
            "stone": 25,
            "wood": 10,
            "bucket": 1
        }
        super().__init__("Well", StructureType.WELL, materials)
        self.water_level = 100.0
        self.max_water = 500.0
        self.refill_rate = 2.0  # Per day
    
    def extract_water(self, amount: float) -> float:
        extracted = min(self.water_level, amount)
        self.water_level -= extracted
        return extracted
    
    def refill(self):
        self.water_level = min(self.max_water, self.water_level + self.refill_rate)
    
    def is_dry(self) -> bool:
        return self.water_level <= 0
    
    def __str__(self):
        return super().__str__() + f" | Water Level: {self.water_level:.0f}/{self.max_water:.0f}"

class Barracks(Structure):
    def __init__(self):
        materials = {
            "wood": 40,
            "stone": 50,
            "metal_ore": 20
        }
        super().__init__("Barracks", StructureType.BARRACKS, materials, capacity=20)
        self.soldiers: List[str] = []
        self.morale_bonus = 10.0
    
    def add_soldier(self, soldier_name: str) -> bool:
        if len(self.soldiers) < self.capacity:
            self.soldiers.append(soldier_name)
            return True
        return False
    
    def __str__(self):
        return super().__str__() + f" | Soldiers: {len(self.soldiers)}/{self.capacity} | Morale Bonus: {self.morale_bonus:.0f}%"

class TrainingGround(Structure):
    def __init__(self):
        materials = {
            "wood": 25,
            "stone": 30,
            "metal_ore": 10
        }
        super().__init__("Training Ground", StructureType.TRAINING_GROUND, materials)
        self.training_level = 1
        self.experience_bonus = 1.5
    
    def increase_training_level(self):
        self.training_level += 1
        self.experience_bonus += 0.2

class Farm(Structure):
    def __init__(self):
        materials = {
            "wood": 20,
            "stone": 15,
            "seed": 10
        }
        super().__init__("Farm", StructureType.FARM, materials, capacity=100)
        self.crop_type: Optional[str] = None
        self.growth_progress = 0.0
        self.harvest_ready = False
    
    def plant_crop(self, crop_type: str):
        self.crop_type = crop_type
        self.growth_progress = 0.0
        self.harvest_ready = False
    
    def advance_growth(self, days: int = 1):
        if self.crop_type and not self.harvest_ready:
            self.growth_progress += days * self.efficiency / 100
            
            if self.growth_progress >= 100:
                self.harvest_ready = True
    
    def harvest(self) -> int:
        if self.harvest_ready:
            harvest_amount = int(self.capacity * (self.efficiency / 100))
            self.harvest_ready = False
            self.crop_type = None
            self.growth_progress = 0.0
            return harvest_amount
        return 0

class Mine(Structure):
    def __init__(self):
        materials = {
            "wood": 35,
            "stone": 40,
            "metal_ore": 15
        }
        super().__init__("Mine", StructureType.MINE, materials)
        self.mining_level = 1
        self.extraction_rate = 2.0
    
    def extract_resources(self) -> Dict[str, int]:
        resources = {
            "metal_ore": int(5 * self.extraction_rate * (self.efficiency / 100)),
            "stone": int(3 * self.extraction_rate * (self.efficiency / 100)),
            "coal": int(2 * self.extraction_rate * (self.efficiency / 100))
        }
        return resources
    
    def upgrade_mining(self):
        self.mining_level += 1
        self.extraction_rate += 0.5

class Forge(Structure):
    def __init__(self):
        materials = {
            "stone": 50,
            "metal_ore": 30,
            "wood": 20
        }
        super().__init__("Forge", StructureType.FORGE, materials)
        self.crafting_level = 1
        self.crafting_speed = 1.0
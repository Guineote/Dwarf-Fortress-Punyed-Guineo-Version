from typing import Dict, Optional
from enums import WeaponType, WeaponMaterial, ArmorType, ArmorMaterial, BodyPart

#Weapons
class Weapon:
    def __init__(self, name: str, weapon_type: WeaponType, material: WeaponMaterial,base_damage: float, accuracy_bonus: float = 0, crit_bonus: float = 0, two_handed: bool = False):
        self.name = name
        self.weapon_type = weapon_type
        self.material = material
        self.base_damage = base_damage
        self.damage = base_damage
        self.accuracy_bonus = accuracy_bonus
        self.crit_bonus = crit_bonus
        self.two_handed = two_handed
        self.durability = 100.0
        self._apply_material_modifiers()
    
    def _apply_material_modifiers(self):
        material_multipliers = {
            WeaponMaterial.WOOD: 0.5,
            WeaponMaterial.STONE: 0.7,
            WeaponMaterial.BRONZE: 1.0,
            WeaponMaterial.IRON: 1.3,
            WeaponMaterial.STEEL: 1.7,
            WeaponMaterial.GOLD: 1.2,
            WeaponMaterial.DIAMOND: 2.5,
            WeaponMaterial.MYTHRIL: 2.2,
            WeaponMaterial.DRAGON_BONE: 2.8
        }
        multiplier = material_multipliers.get(self.material, 1.0)
        self.damage = self.base_damage * multiplier
    
    def get_effective_damage(self) -> float:
        return self.damage * (self.durability / 100)
    
    def __str__(self):
        return f"{self.material.value.capitalize()} {self.name} ({self.weapon_type.value}) DMG:{self.damage:.1f}"

class Sword(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Sword"
        super().__init__(name, WeaponType.SWORD, material, base_damage=25, accuracy_bonus=5, crit_bonus=3, two_handed=False)

class GreatSword(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Great Sword"
        super().__init__(name, WeaponType.GREAT_SWORD, material, base_damage=45, accuracy_bonus=0, crit_bonus=5, two_handed=True)

class Axe(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Axe"
        super().__init__(name, WeaponType.AXE, material, base_damage=30, accuracy_bonus=0, crit_bonus=8, two_handed=False)

class GreatAxe(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Great Axe"
        super().__init__(name, WeaponType.GREAT_AXE, material, base_damage=50, accuracy_bonus=-5, crit_bonus=12, two_handed=True)

class Bow(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Bow"
        super().__init__(name, WeaponType.BOW, material, base_damage=20, accuracy_bonus=10, crit_bonus=5, two_handed=True)

class Crossbow(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Crossbow"
        super().__init__(name, WeaponType.CROSSBOW, material, base_damage=28, accuracy_bonus=15, crit_bonus=3, two_handed=True)

class Spear(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Spear"
        super().__init__(name, WeaponType.SPEAR, material, base_damage=22, accuracy_bonus=8, crit_bonus=4, two_handed=False)

class Dagger(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Dagger"
        super().__init__(name, WeaponType.DAGGER, material, base_damage=15, accuracy_bonus=12, crit_bonus=15, two_handed=False)

class Staff(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Staff"
        super().__init__(name, WeaponType.STAFF, material, base_damage=18, accuracy_bonus=5, crit_bonus=2, two_handed=True)

class Mace(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Mace"
        super().__init__(name, WeaponType.MACE, material, base_damage=28, accuracy_bonus=3, crit_bonus=4, two_handed=False)

class Hammer(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "Hammer"
        super().__init__(name, WeaponType.HAMMER, material, base_damage=26, accuracy_bonus=2, crit_bonus=6, two_handed=False)

class WarHammer(Weapon):
    def __init__(self, material: WeaponMaterial):
        name = "War Hammer"
        super().__init__(name, WeaponType.WAR_HAMMER, material, base_damage=48, accuracy_bonus=-3, crit_bonus=10, two_handed=True)

#Armors

class Armor:
    def __init__(self, name: str, armor_type: ArmorType, material: ArmorMaterial, base_defense: float, body_part: Optional[BodyPart] = None):
        self.name = name
        self.armor_type = armor_type
        self.material = material
        self.base_defense = base_defense
        self.defense = base_defense
        self.body_part = body_part
        self.durability = 100.0
        self.enchantments: Dict[str, float] = {}
        self._apply_material_modifiers()
    
    def _apply_material_modifiers(self):
        material_multipliers = {
            ArmorMaterial.CLOTH: 0.3,
            ArmorMaterial.LEATHER: 1.0,
            ArmorMaterial.WOOD: 0.6,
            ArmorMaterial.STONE: 0.8,
            ArmorMaterial.BRONZE: 1.2,
            ArmorMaterial.IRON: 1.5,
            ArmorMaterial.STEEL: 2.0,
            ArmorMaterial.GOLD: 1.3,
            ArmorMaterial.DIAMOND: 3.0,
            ArmorMaterial.DRAGON_SCALE: 3.5,
            ArmorMaterial.MYTHRIL: 2.8
        }
        multiplier = material_multipliers.get(self.material, 1.0)
        self.defense = self.base_defense * multiplier
    
    def get_effective_defense(self) -> float:
        return self.defense * (self.durability / 100)
    
    def __str__(self):
        return f"{self.material.value.capitalize()} {self.name} DEF:{self.defense:.1f}"

class Helmet(Armor):
    def __init__(self, material: ArmorMaterial):
        name = "Helmet"
        super().__init__(name, ArmorType.HELMET, material, base_defense=15, body_part=BodyPart.HEAD)

class Chestplate(Armor):
    def __init__(self, material: ArmorMaterial):
        name = "Chestplate"
        super().__init__(name, ArmorType.CHESTPLATE, material, base_defense=30, body_part=BodyPart.CHEST)

class DragonScaleChestplate(Chestplate):
    def __init__(self):
        super().__init__(ArmorMaterial.DRAGON_SCALE)
        self.enchantments["fire_resistance"] = 50

class Greaves(Armor):
    def __init__(self, material: ArmorMaterial):
        name = "Greaves"
        super().__init__(name, ArmorType.GREAVES, material, base_defense=20, body_part=BodyPart.LEFT_LEG)

class Sabaton(Armor):
    def __init__(self, material: ArmorMaterial):
        name = "Sabaton"
        super().__init__(name, ArmorType.SABATON, material, base_defense=10, body_part=BodyPart.LEFT_FOOT)

class Gauntlets(Armor):
    def __init__(self, material: ArmorMaterial):
        name = "Gauntlets"
        super().__init__(name, ArmorType.GAUNTLETS, material, base_defense=12, body_part=BodyPart.LEFT_HAND)

class Armguard(Armor):
    def __init__(self, material: ArmorMaterial):
        name = "Armguard"
        super().__init__(name, ArmorType.ARMGUARD, material, base_defense=8, body_part=BodyPart.LEFT_ARM)

class Amulet(Armor):
    def __init__(self, name: str, material: ArmorMaterial, base_defense: float = 5):
        super().__init__(name, ArmorType.AMULET, material, base_defense, body_part=BodyPart.NECK)
        # Amulets have special enchantments
        self.stat_bonuses: Dict[str, float] = {}

class AgilityAmulet(Amulet):
    def __init__(self):
        super().__init__("Amulet of Agility", ArmorMaterial.LEATHER, base_defense=3)
        self.stat_bonuses = {"speed": 5, "dexterity": 3}

class LuckAmulet(Amulet):
    def __init__(self):
        super().__init__("Amulet of Luck", ArmorMaterial.GOLD, base_defense=2)
        self.stat_bonuses = {"luck": 10}

class StrengthAmulet(Amulet):
    def __init__(self):
        super().__init__("Amulet of Strength", ArmorMaterial.IRON, base_defense=4)
        self.stat_bonuses = {"strength": 5}

class DragonHeartAmulet(Amulet):
    def __init__(self):
        super().__init__("Dragon Heart Amulet", ArmorMaterial.DRAGON_SCALE, base_defense=8)
        self.stat_bonuses = {"strength": 10, "health": 50, "fire_resistance": 75}
        self.enchantments["fire_immunity"] = 100

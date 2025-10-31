#from enums import Occupation, AnimalType, BossType, TreeType, PlantType, Gender, Race
#from enums import WeaponType, WeaponMaterial, ArmorMaterial
#from characters import *
#from animals import *
#from plants import *
#from equipment import *

from Classes.enums import Occupation, AnimalType, BossType, TreeType, PlantType, Gender, Race
from Classes.enums import WeaponType, WeaponMaterial, ArmorMaterial
from Classes.characters import *
from Classes.animals import *
from Classes.plants import *
from Classes.equipment import *


def create_character(occupation: Occupation, name: str, age: int, gender: Gender, race: Race) -> SentientBeing:
    occupation_classes = {
        Occupation.LUMBERJACK: Lumberjack,
        Occupation.FISHERMAN: Fisherman,
        Occupation.HUNTER: Hunter,
        Occupation.BUILDER: Builder,
        Occupation.FARMER: Farmer,
        Occupation.MEDIC: Medic,
        Occupation.BREWER: Brewer,
        Occupation.BLACKSMITH: Blacksmith,
        Occupation.WARRIOR: Warrior,
        Occupation.ARCHER: Archer,
        Occupation.MERCHANT: Merchant
    }
    
    char_class = occupation_classes.get(occupation, SentientBeing)
    return char_class(name, age, gender, race)

def create_animal(animal_type: AnimalType) -> Animal:
    animal_classes = {
        AnimalType.SQUIRREL: Squirrel,
        AnimalType.SHEEP: Sheep,
        AnimalType.PIG: Pig,
        AnimalType.OX: Ox,
        AnimalType.BULL: Bull,
        AnimalType.CHICKEN: Chicken,
        AnimalType.HORSE: Horse,
        AnimalType.BOAR: Boar,
        AnimalType.RABBIT: Rabbit,
        AnimalType.BEAR: Bear,
        AnimalType.COW: Cow,
        AnimalType.PIRANHA: Piranha,
        AnimalType.SHARK: Shark,
        AnimalType.WHALE: Whale,
        AnimalType.GOAT: Goat,
        AnimalType.BEE: Bee,
        AnimalType.BIRD: Bird,
        AnimalType.DOG: Dog,
        AnimalType.CAT: Cat,
        AnimalType.FROG: Frog,
        AnimalType.LEECH: Leech,
        AnimalType.SNAKE: Snake
    }
    
    animal_class = animal_classes.get(animal_type, Animal)
    return animal_class()

def create_boss(boss_type: BossType) -> Animal:
    boss_classes = {
        BossType.MINOTAUR: Minotaur,
        BossType.DRAGON: Dragon,
        BossType.CYCLOPS: Cyclops,
        BossType.SIREN: Siren
    }
    
    boss_class = boss_classes.get(boss_type, Animal)
    return boss_class()

def create_tree(tree_type: TreeType) -> Tree:
    tree_classes = {
        TreeType.OAK: Oak,
        TreeType.WALNUT: Walnut,
        TreeType.MAHOGANY: Mahogany,
        TreeType.PINE: Pine,
        TreeType.BAOBAB: Baobab,
        TreeType.APPLE: AppleTree,
        TreeType.OLIVE: Olive,
        TreeType.ALMOND: Almond
    }
    
    tree_class = tree_classes.get(tree_type, Tree)
    return tree_class()

def create_plant(plant_type: PlantType) -> Plant:
    plant_classes = {
        PlantType.GRAPE: Grape,
        PlantType.POTATO: Potato,
        PlantType.CARROT: Carrot,
        PlantType.COTTON: Cotton,
        PlantType.BARLEY: Barley,
        PlantType.WHEAT: Wheat,
        PlantType.SUGARCANE: Sugarcane,
        PlantType.CORN: Corn
    }
    
    plant_class = plant_classes.get(plant_type, Plant)
    return plant_class()

def create_weapon(weapon_type: WeaponType, material: WeaponMaterial) -> Weapon:
    weapon_classes = {
        WeaponType.SWORD: Sword,
        WeaponType.GREAT_SWORD: GreatSword,
        WeaponType.AXE: Axe,
        WeaponType.GREAT_AXE: GreatAxe,
        WeaponType.BOW: Bow,
        WeaponType.CROSSBOW: Crossbow,
        WeaponType.SPEAR: Spear,
        WeaponType.DAGGER: Dagger,
        WeaponType.STAFF: Staff,
        WeaponType.MACE: Mace,
        WeaponType.HAMMER: Hammer,
        WeaponType.WAR_HAMMER: WarHammer
    }
    
    weapon_class = weapon_classes.get(weapon_type, Weapon)
    return weapon_class(material)

def create_armor(armor_type: ArmorType, material: ArmorMaterial) -> Armor:
    armor_classes = {
        ArmorType.HELMET: Helmet,
        ArmorType.CHESTPLATE: Chestplate,
        ArmorType.GREAVES: Greaves,
        ArmorType.SABATON: Sabaton,
        ArmorType.GAUNTLETS: Gauntlets,
        ArmorType.ARMGUARD: Armguard
    }
    
    armor_class = armor_classes.get(armor_type, Armor)
    return armor_class(material)

def create_amulet(amulet_type: str) -> Amulet:
    amulet_classes = {
        "agility": AgilityAmulet,
        "luck": LuckAmulet,
        "strength": StrengthAmulet,
        "dragon_heart": DragonHeartAmulet
    }
    
    amulet_class = amulet_classes.get(amulet_type, Amulet)
    if amulet_class == Amulet:
        return Amulet("Generic Amulet", ArmorMaterial.LEATHER)
    return amulet_class()
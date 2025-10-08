from enums import *
from stats import Stats
from equipment import *
from body_parts import BodyPartStatus
from characters import *
from animals import *
from plants import *
from entity_Creation import *

#Should change the max_health with the stats so that it is the same amount as the stats given...

#Small Demo on how to create the entities v1
if __name__ == "__main__":
    
    dwarf_warrior = create_character(Occupation.WARRIOR, "Thorin", 120, Gender.MALE, Race.DWARF)
    print(f"{dwarf_warrior}")

    elf_archer = create_character(Occupation.ARCHER, "Legolas", 500, Gender.MALE, Race.ELF)

    human_medic = create_character(Occupation.MEDIC, "Clara", 35, Gender.FEMALE, Race.HUMAN)
    
    orc_lumberjack = create_character(Occupation.LUMBERJACK, "Grommash", 45, Gender.MALE, Race.ORC)
    
    # Weapon & ArmorCreation
    steel_sword = create_weapon(WeaponType.SWORD, WeaponMaterial.STEEL)
    print(f"{steel_sword}")

    diamond_great_sword = create_weapon(WeaponType.GREAT_SWORD, WeaponMaterial.DIAMOND)
    
    mythril_bow = create_weapon(WeaponType.BOW, WeaponMaterial.MYTHRIL)
    
    dragon_bone_axe = create_weapon(WeaponType.AXE, WeaponMaterial.DRAGON_BONE)
    
    iron_crossbow = create_weapon(WeaponType.CROSSBOW, WeaponMaterial.IRON)
    
    diamond_helmet = create_armor(ArmorType.HELMET, ArmorMaterial.DIAMOND)
    diamond_chestplate = create_armor(ArmorType.CHESTPLATE, ArmorMaterial.DIAMOND)
    steel_greaves = create_armor(ArmorType.GREAVES, ArmorMaterial.STEEL)
    leather_sabaton = create_armor(ArmorType.SABATON, ArmorMaterial.LEATHER)
    iron_gauntlets = create_armor(ArmorType.GAUNTLETS, ArmorMaterial.IRON)
    agility_amulet = create_amulet("agility")
    luck_amulet = create_amulet("luck")
    dragon_heart = create_amulet("dragon_heart")

    print(f"{agility_amulet}")
    print(f"    Stats bonuses: {agility_amulet.stat_bonuses}")
    
    print(f"{luck_amulet}")
    print(f"    Stats bonuses: {luck_amulet.stat_bonuses}")
    
    print(f"{dragon_heart}")
    print(f"    Stats bonuses: {dragon_heart.stat_bonuses}")
    print(f"    Enchantments: {dragon_heart.enchantments}")
    

    print("\nEquip:")

    print(f"\n{dwarf_warrior.name}'s Stats Before Equipment:")
    print(f"  {dwarf_warrior.stats}")

    dwarf_warrior.equip_weapon(steel_sword)
    print(f"\n{dwarf_warrior.name} equipped {steel_sword.name} and so on...") #And So onm
    dwarf_warrior.equip_armor(diamond_helmet)
    dwarf_warrior.equip_armor(diamond_chestplate)
    dwarf_warrior.equip_armor(steel_greaves)
    dwarf_warrior.equip_armor(leather_sabaton)
    dwarf_warrior.equip_armor(dragon_heart)
    

    print(f"\n{dwarf_warrior.name}'s Stats After Equipment:")
    print(f"  {dwarf_warrior.stats}")
    print(f"  Total Armor: {dwarf_warrior.calculate_total_armor():.1f}")
    
    print("\nCOMBAT STATS:")
    
    print(f"{dwarf_warrior.name}'s Combat Stats:")
    print(f"  Attack Power: {dwarf_warrior.get_attack_power():.1f}")
    print(f"  Hit Chance: {dwarf_warrior.get_hit_chance():.1f}%")
    print(f"  Crit Chance: {dwarf_warrior.get_crit_chance():.1f}%")
    print(f"  Dodge Chance: {dwarf_warrior.get_dodge_chance():.1f}%")
    
    # Animals
    print("\nAnimals")

    bear = create_animal(AnimalType.BEAR)
    print(f"{bear}")
    
    cow = create_animal(AnimalType.COW)
    print(f"{cow}")
    print(f"    Daily production: {cow.produce_daily_resource()}")
    
    horse = create_animal(AnimalType.HORSE)
    print(f"{horse}")
    print(f"  Can be ridden: {horse.can_be_ridden}")
    print(f"  Can carry load: {horse.can_carry_load}")
    
    # Boss
    print("\nBoss")

    dragon = create_boss(BossType.DRAGON)
    print(f"{dragon}")
    print(f"    Boss with {dragon.armor} armor")
    print(f"    Can speak: {dragon.can_speak}")
    print(f"    Fire breath damage: {dragon.fire_breath_damage}")
    
    minotaur = create_boss(BossType.MINOTAUR)
    print(f"Minotaur Boss")
    print(f"    HP: {minotaur.health}, Axe DMG: {minotaur.axe_damage}")
    
    cyclops = create_boss(BossType.CYCLOPS)
    print(f"Cyclops Boss")
    print(f"    HP: {cyclops.health}, Accuracy: {cyclops.accuracy}% (1 eye)")
    
    siren = create_boss(BossType.SIREN)
    print(f"Siren Boss")
    print(f"  HP: {siren.health}, Hypnotic song: {siren.hypnotic_song}")
    
    # Hunting
    print("\nHunting")

    rabbit = create_animal(AnimalType.RABBIT)
    print(f"Hunting: {rabbit}")
    damage = elf_archer.get_attack_power()
    rabbit.take_damage(damage)
    print(f"  {elf_archer.name} dealt {damage:.1f} damage")
    print(f"  {rabbit}")
    
    if not rabbit.is_alive:
        drops = rabbit.get_drops()
        print(f"  Drops: {drops}")
    

    # Trees
    print("\nTrees")

    oak = create_tree(TreeType.OAK)
    print(f"{oak}")
    
    apple_tree = create_tree(TreeType.APPLE)
    print(f"{apple_tree}")
    
    pine = create_tree(TreeType.PINE)
    print(f"{pine}")
    print(f"  Produces resin: {pine.produces_resin}")
    
    baobab = create_tree(TreeType.BAOBAB)
    print(f"{baobab}")
    print(f"  Water stored: {baobab.water_amount}")
    
    # Felling \ cutting down trees
    print("\n Cutting Trees")
    
    print(f"{orc_lumberjack.name} chops down the {oak.tree_type.value} tree:")
    resources = oak.chop_down()
    print(f"  Resources obtained: {resources}")
    
    # Plants
    print("\nPlants")

    wheat = create_plant(PlantType.WHEAT)
    print(f"{wheat}")
    
    corn = create_plant(PlantType.CORN)
    print(f"{corn}")
    
    print("\nPlant Growth Simulation:")
    print("-"*80)
    
    print(f"Day 0: {wheat}")
    for day in [50, 110]:
        wheat.grow(day)
        print(f"Day {wheat.current_day}: {wheat}")
    
    if wheat.is_mature:
        harvest = wheat.harvest()
        print(f"\n Harvested: {harvest}")
    
    # Healing
    print("\nHealing")
    print("-"*80)
    
    dwarf_warrior.take_damage(50)
    print(f"{dwarf_warrior.name} took 50 damage")
    print(f"  HP: {dwarf_warrior.stats.health:.0f}/{dwarf_warrior.stats.max_health:.0f}")
    
    healed = human_medic.heal_target(dwarf_warrior, 30)
    print(f"\n{human_medic.name} healed {dwarf_warrior.name} for {healed:.1f} HP")
    print(f"  HP: {dwarf_warrior.stats.health:.0f}/{dwarf_warrior.stats.max_health:.0f}")
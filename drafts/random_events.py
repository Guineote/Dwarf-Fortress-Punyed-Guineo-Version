import random
from typing import Dict, List, Optional, Tuple
from biome_system import *
from enums import *

class RaceRelationship:
    def __init__(self):
        self.relations: Dict[Tuple[str, str], RaceRelation] = {}
        self._initialize_default_relations()
    
    def _initialize_default_relations(self):
        default_relations = {
            ("dwarf", "dwarf"): RaceRelation.ALLIED,
            ("dwarf", "human"): RaceRelation.FRIENDLY,
            ("dwarf", "elf"): RaceRelation.NEUTRAL,
            ("dwarf", "orc"): RaceRelation.HOSTILE,
            ("dwarf", "goblin"): RaceRelation.HOSTILE,
            ("human", "human"): RaceRelation.ALLIED,
            ("human", "elf"): RaceRelation.FRIENDLY,
            ("human", "orc"): RaceRelation.HOSTILE,
            ("human", "goblin"): RaceRelation.HOSTILE,
            ("elf", "elf"): RaceRelation.ALLIED,
            ("elf", "orc"): RaceRelation.HOSTILE,
            ("elf", "goblin"): RaceRelation.HOSTILE,
            ("orc", "orc"): RaceRelation.ALLIED,
            ("orc", "goblin"): RaceRelation.FRIENDLY,
            ("goblin", "goblin"): RaceRelation.ALLIED,
            ("orc", "troll"): RaceRelation.FRIENDLY,
            ("troll", "troll"): RaceRelation.ALLIED,
        }
        
        for (race1, race2), relation in default_relations.items():
            self.set_relation(race1, race2, relation)
    
    def set_relation(self, race1: str, race2: str, relation: RaceRelation):
        self.relations[(race1.lower(), race2.lower())] = relation
        self.relations[(race2.lower(), race1.lower())] = relation
    
    def get_relation(self, race1: str, race2: str) -> RaceRelation:
        key = (race1.lower(), race2.lower())
        return self.relations.get(key, RaceRelation.NEUTRAL)
    
    def are_friendly(self, race1: str, race2: str) -> bool:
        relation = self.get_relation(race1, race2)
        return relation in [RaceRelation.FRIENDLY, RaceRelation.ALLIED]

class RandomEventSystem:
    def __init__(self):
        self.race_relations = RaceRelationship()
        self.active_events: List[Dict] = []
    
    def invasion_event(self, defending_race: str, attacking_race: str, 
                      settlement_population: int, military_strength: float) -> Dict:

        relation = self.race_relations.get_relation(defending_race, attacking_race)
        
        if self.race_relations.are_friendly(defending_race, attacking_race):
            return {
                "type": EventType.INVASION,
                "occurred": False,
                "reason": f"{attacking_race.capitalize()} and {defending_race.capitalize()} are {relation.value}. No invasion possible."
            }
        base_probability = 50.0
        
        relation_modifiers = {
            RaceRelation.HOSTILE: 15.0,   
            RaceRelation.NEUTRAL: 5.0,      
            RaceRelation.FRIENDLY: -50.0   
        }
        
        relation_mod = relation_modifiers.get(relation, 0.0)
        
        military_mod = -military_strength * 0.5
        
        attacker_advantage = max(0, settlement_population * 0.3 - military_strength * 10)
        
        invasion_probability = base_probability + relation_mod + military_mod + (attacker_advantage * 0.2)
        invasion_probability = max(0, min(100, invasion_probability))
        
        invades = random.random() * 100 < invasion_probability
        
        event = {
            "type": EventType.INVASION,
            "occurred": invades,
            "defending_race": defending_race,
            "attacking_race": attacking_race,
            "relation": relation.value,
            "invasion_probability": invasion_probability,
            "settlement_population": settlement_population,
            "military_strength": military_strength,
            "damage": 0
        }
        
        if invades:
            defense_factor = military_strength / (settlement_population * 0.1 + 1)
            base_damage = random.randint(20, 50)
            actual_damage = max(5, base_damage - (defense_factor * 20))
            
            event["damage"] = int(actual_damage)
            event["casualties"] = int(settlement_population * (actual_damage / 100))
            event["description"] = f"{attacking_race.capitalize()}s invaded Damage: {actual_damage:.0f}%"
        else:
            event["description"] = f"{attacking_race.capitalize()}s attempted invasion but were repelled"
        
        self.active_events.append(event)
        return event
    
    
    def natural_disaster_event(self, biome: Biome, population: int, settlement_durability: float) -> Dict:
        biome_system = BiomeSystem(biome)
        
        possible_disasters = []
        
        if biome == Biome.FOREST:
            possible_disasters = [
                (DisasterType.TORRENTIAL_RAIN, 35.0),
                (DisasterType.FIRE, 45.0),
                (DisasterType.TORNADO, 20.0)
            ]
        
        elif biome == Biome.TUNDRA:
            possible_disasters = [
                (DisasterType.AVALANCHE, 50.0),
                (DisasterType.BLIZZARD, 60.0),
                (DisasterType.FLOOD, 25.0)
            ]
        
        elif biome == Biome.MOUNTAIN:
            possible_disasters = [
                (DisasterType.AVALANCHE, 55.0),
                (DisasterType.EARTHQUAKE, 40.0),
                (DisasterType.VOLCANIC_ERUPTION, 30.0)
            ]
        
        elif biome == Biome.AQUATIC:
            possible_disasters = [
                (DisasterType.FLOOD, 50.0),
                (DisasterType.TORNADO, 35.0),
                (DisasterType.EARTHQUAKE, 25.0)
            ]
        
        elif biome == Biome.DESERT:
            possible_disasters = [
                (DisasterType.TORNADO, 40.0),
                (DisasterType.FIRE, 35.0),
                (DisasterType.EARTHQUAKE, 20.0)
            ]
        
        elif biome == Biome.SWAMP:
            possible_disasters = [
                (DisasterType.FLOOD, 60.0),
                (DisasterType.DISEASE, 50.0)
            ]
        
        elif biome == Biome.UNDERGROUND:
            possible_disasters = [
                (DisasterType.EARTHQUAKE, 45.0),
                (DisasterType.FLOOD, 40.0)
            ]
        
        else:
            possible_disasters = [
                (DisasterType.FIRE, 25.0),
                (DisasterType.TORNADO, 30.0)
            ]
        
        total_probability = sum(prob for _, prob in possible_disasters)
        roll = random.random() * total_probability
        
        current = 0
        selected_disaster = possible_disasters[0][0]
        
        for disaster, prob in possible_disasters:
            current += prob
            if roll < current:
                selected_disaster = disaster
                break
        occurs = random.random() < 0.5
        
        event = {
            "type": EventType.NATURAL_DISASTER,
            "biome": biome.value,
            "occurred": occurs,
            "disaster_type": selected_disaster.value,
            "population": population,
            "settlement_durability": settlement_durability,
            "damage": 0,
            "casualties": 0
        }
        
        if occurs:
            damage_multipliers = {
                DisasterType.TORRENTIAL_RAIN: 20.0,
                DisasterType.FIRE: 40.0,
                DisasterType.AVALANCHE: 45.0,
                DisasterType.EARTHQUAKE: 50.0,
                DisasterType.FLOOD: 35.0,
                DisasterType.BLIZZARD: 30.0,
                DisasterType.VOLCANIC_ERUPTION: 60.0,
                DisasterType.TORNADO: 35.0,
                DisasterType.DISEASE: 15.0
            }
            
            base_damage = damage_multipliers.get(selected_disaster, 25.0)
            durability_factor = (100 - settlement_durability) / 100
            actual_damage = base_damage * (0.5 + durability_factor)
            
            event["damage"] = int(actual_damage)
            event["casualties"] = int(population * (actual_damage / 100))
            event["structural_damage"] = int(50 * durability_factor)
            
            descriptions = {
                DisasterType.TORRENTIAL_RAIN: f"Torrential rain causes {actual_damage:.0f}% damage!",
                DisasterType.FIRE: f"Forest fire spreads! {actual_damage:.0f}% damage!",
                DisasterType.AVALANCHE: f"Avalanche! {actual_damage:.0f}% damage!",
                DisasterType.EARTHQUAKE: f"Earthquake strikes! {actual_damage:.0f}% damage!",
                DisasterType.FLOOD: f"Flood! {actual_damage:.0f}% damage!",
                DisasterType.BLIZZARD: f"Severe blizzard! {actual_damage:.0f}% damage!",
                DisasterType.VOLCANIC_ERUPTION: f"Volcanic eruption! {actual_damage:.0f}% damage!",
                DisasterType.TORNADO: f"Tornado! {actual_damage:.0f}% damage!",
                DisasterType.DISEASE: f"Disease outbreak! {actual_damage:.0f}% affected!"
            }
            
            event["description"] = descriptions.get(selected_disaster, f"Disaster strikes! {actual_damage:.0f}% damage!")
        else:
            event["description"] = f"{selected_disaster.value} avoided!"
        
        self.active_events.append(event)
        return event
    
    def get_active_events(self) -> List[Dict]:
        return self.active_events.copy()
    
    def clear_events(self):
        self.active_events.clear()

from typing import List
from enums import *

class BiomeSystem:
    def __init__(self, biome: Biome):
        self.biome = biome
        self.temperature = self._get_temperature()
        self.humidity = self._get_humidity()
        self.danger_level = self._get_danger_level()
        self.natural_resources = self._get_natural_resources()
    
    def _get_temperature(self) -> float:
        temps = {
            Biome.AQUATIC: 15.0,
            Biome.FOREST: 18.0,
            Biome.TUNDRA: -20.0,
            Biome.MOUNTAIN: 5.0,
            Biome.GRASSLAND: 22.0,
            Biome.DESERT: 35.0,
            Biome.SWAMP: 25.0,
            Biome.UNDERGROUND: 12.0
        }
        return temps.get(self.biome, 20.0)
    
    def _get_humidity(self) -> float:
        humidity = {
            Biome.AQUATIC: 95.0,
            Biome.FOREST: 80.0,
            Biome.TUNDRA: 30.0,
            Biome.MOUNTAIN: 40.0,
            Biome.GRASSLAND: 50.0,
            Biome.DESERT: 10.0,
            Biome.SWAMP: 90.0,
            Biome.UNDERGROUND: 60.0
        }
        return humidity.get(self.biome, 50.0)
    
    def _get_danger_level(self) -> float:
        danger = {
            Biome.AQUATIC: 60.0,
            Biome.FOREST: 40.0,
            Biome.TUNDRA: 70.0,
            Biome.MOUNTAIN: 75.0,
            Biome.GRASSLAND: 20.0,
            Biome.DESERT: 50.0,
            Biome.SWAMP: 65.0,
            Biome.UNDERGROUND: 80.0
        }
        return danger.get(self.biome, 40.0)
    
    def _get_natural_resources(self) -> List[str]:
        resources = {
            Biome.AQUATIC: ["fish", "shells", "pearls", "seaweed"],
            Biome.FOREST: ["wood", "berries", "herbs", "mushrooms"],
            Biome.TUNDRA: ["ice", "bone", "fur", "fish"],
            Biome.MOUNTAIN: ["stone", "metal_ore", "gems", "coal"],
            Biome.GRASSLAND: ["wheat", "hay", "herbs", "wild_animals"],
            Biome.DESERT: ["sand", "salt", "cactus", "gems"],
            Biome.SWAMP: ["mud", "herbs", "reeds", "insects"],
            Biome.UNDERGROUND: ["metal_ore", "gems", "coal", "crystals"]
        }
        return resources.get(self.biome, [])
    
    def get_disaster_probability(self, disaster_type: DisasterType) -> float:
        disaster_probs = {
            Biome.FOREST: {
                DisasterType.TORRENTIAL_RAIN: 35.0,
                DisasterType.FIRE: 45.0,
                DisasterType.TORNADO: 20.0
            },
            Biome.TUNDRA: {
                DisasterType.AVALANCHE: 50.0,
                DisasterType.BLIZZARD: 60.0,
                DisasterType.FLOOD: 25.0
            },
            Biome.MOUNTAIN: {
                DisasterType.AVALANCHE: 55.0,
                DisasterType.EARTHQUAKE: 40.0,
                DisasterType.VOLCANIC_ERUPTION: 30.0
            },
            Biome.AQUATIC: {
                DisasterType.FLOOD: 50.0,
                DisasterType.TORNADO: 35.0,
                DisasterType.EARTHQUAKE: 25.0
            },
            Biome.DESERT: {
                DisasterType.TORNADO: 40.0,
                DisasterType.FIRE: 35.0,
                DisasterType.EARTHQUAKE: 20.0
            },
            Biome.SWAMP: {
                DisasterType.FLOOD: 60.0,
                DisasterType.DISEASE: 50.0
            }
        }
        
        if self.biome in disaster_probs:
            return disaster_probs[self.biome].get(disaster_type, 0.0)
        return 0.0
    
    def __str__(self):
        return f"Biome: {self.biome.value} | Temp: {self.temperature}°C | Humidity: {self.humidity:.0f}% | Danger: {self.danger_level:.0f}%"

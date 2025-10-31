import random
from typing import Dict, List, Optional
#from enums import *
from Classes.enums import *


class NameStyle(Enum):
    DWARF = "dwarf"
    ELF = "elf"
    HUMAN = "human"
    ORC = "orc"
    GOBLIN = "goblin"
    TROLL = "troll"
    WIZARD = "wizard"
    FANTASY = "fantasy"

class NameComponents:
    DWARF_MALE_PREFIXES = ["Thor", "Dw", "Kal", "Bro", "Grim", "Oin", "Duar", "Tur", "Bal", "Gil"]
    DWARF_MALE_SUFFIXES = ["in", "din", "or", "ar", "an", "ak", "ix", "us", "un", "ir"]
    
    DWARF_FEMALE_PREFIXES = ["Bar", "Dis", "Fro", "Gis", "Hy", "Dis", "Ber", "Mis", "Dor"]
    DWARF_FEMALE_SUFFIXES = ["nis", "dis", "na", "lis", "tra", "gal", "ild", "da"]
    
    ELF_MALE_PREFIXES = ["Leg", "Ar", "Gal", "Aer", "El", "Tha", "Ara", "Cel", "Lore", "Mel"]
    ELF_MALE_SUFFIXES = ["as", "ion", "eth", "iel", "rin", "dor", "wen", "ian", "en"]
    
    ELF_FEMALE_PREFIXES = ["Ara", "Gal", "Mir", "Nim", "Nor", "Tir", "Aur", "Lar", "Sel"]
    ELF_FEMALE_SUFFIXES = ["eth", "iel", "wen", "ann", "ia", "ara", "aen", "ala", "ith"]
    
    HUMAN_MALE_NAMES = [
        "John", "James", "Robert", "Michael", "William", "Richard", "Joseph", "Charles",
        "Thomas", "David", "Edward", "Henry", "Peter", "Paul", "Marcus", "Julius",
        "Adrian", "Anthony", "Alexander", "Benjamin", "Christopher", "Daniel", "Samuel"
    ]
    
    HUMAN_FEMALE_NAMES = [
        "Mary", "Elizabeth", "Anna", "Margaret", "Sarah", "Catherine", "Victoria", "Rebecca",
        "Clara", "Rose", "Alice", "Margaret", "Helen", "Charlotte", "Jane", "Julia",
        "Grace", "Emma", "Eleanor", "Sophia", "Victoria", "Laura", "Isabella"
    ]
    
    ORC_MALE_PREFIXES = ["Grom", "Dro", "Thro", "Mog", "Gor", "Gar", "Bru", "Ska", "Tho", "Kru"]
    ORC_MALE_SUFFIXES = ["mash", "thar", "gul", "karn", "bog", "jar", "ash", "zur", "mor"]
    
    ORC_FEMALE_PREFIXES = ["Dra", "Gol", "Mo", "Pha", "Thru", "Ska", "Ga", "Bra", "Ka"]
    ORC_FEMALE_SUFFIXES = ["sha", "thia", "ga", "rla", "sha", "nia", "ka", "ra"]
    
    GOBLIN_PREFIXES = ["Snik", "Snag", "Grok", "Grim", "Gug", "Zig", "Zap", "Jab", "Gib", "Skr"]
    GOBLIN_SUFFIXES = ["it", "ket", "ag", "ug", "og", "ik", "ek", "ak", "ot", "ut"]
    
    TROLL_PREFIXES = ["Trog", "Grrul", "Bru", "Thrr", "Mor", "Gul", "Kra", "Vul", "Kur"]
    TROLL_SUFFIXES = ["tak", "thak", "gul", "og", "ak", "ur", "uk", "or", "ar"]
    
    WIZARD_PREFIXES = ["Mer", "Gand", "Sar", "Thur", "Aur", "Mor", "Eld", "Sal", "Az", "Zar"]
    WIZARD_SUFFIXES = ["lin", "dor", "mir", "oth", "and", "eth", "ial", "wyn", "us"]
    
    FANTASY_SYLLABLES = ["Al", "An", "Ar", "Az", "Ba", "Be", "Bi", "Bo", "Br", "Bu",
                        "Ca", "Ce", "Ci", "Co", "Cr", "Cu", "Da", "De", "Di", "Do",
                        "Dr", "Du", "Ea", "Ec", "Ed", "El", "En", "Er", "Es", "Et",
                        "Fa", "Fe", "Fi", "Fo", "Fr", "Fu", "Ga", "Ge", "Gi", "Go",
                        "Gr", "Gu", "Ha", "He", "Hi", "Ho", "Hr", "Hu", "Ja", "Je",
                        "Jo", "Ju", "Ka", "Ke", "Ki", "Ko", "Kr", "La", "Le", "Li",
                        "Lo", "Ma", "Me", "Mi", "Mo", "Na", "Ne", "Ni", "No", "Nu",
                        "Pa", "Pe", "Pi", "Po", "Pr", "Ra", "Re", "Ri", "Ro", "Ru",
                        "Sa", "Se", "Si", "So", "Su", "Ta", "Te", "Ti", "To", "Tu",
                        "Va", "Ve", "Vi", "Vo", "Wa", "We", "Wi", "Wo", "Ya", "Ye",
                        "Za", "Ze", "Zi", "Zo"]
class NameGenerator:  
    def __init__(self):
        self.generated_names: Dict[str, set] = {}
        self._initialize_name_sets()
    
    def _initialize_name_sets(self):
        self.generated_names = {
            "dwarf_male": set(),
            "dwarf_female": set(),
            "elf_male": set(),
            "elf_female": set(),
            "human_male": set(),
            "human_female": set(),
            "orc_male": set(),
            "orc_female": set(),
            "goblin": set(),
            "troll": set(),
            "wizard": set(),
            "animal": set(),
            "generic": set()
        }
    
    def generate_dwarf_name(self, gender: str = "male", ensure_unique: bool = True) -> str:
        gender = gender.lower()
        key = f"dwarf_{gender}"
        
        while True:
            if gender == "male":
                prefix = random.choice(NameComponents.DWARF_MALE_PREFIXES)
                suffix = random.choice(NameComponents.DWARF_MALE_SUFFIXES)
            else:
                prefix = random.choice(NameComponents.DWARF_FEMALE_PREFIXES)
                suffix = random.choice(NameComponents.DWARF_FEMALE_SUFFIXES)
            
            name = prefix + suffix
            
            if not ensure_unique or name not in self.generated_names[key]:
                self.generated_names[key].add(name)
                return name
    
    def generate_elf_name(self, gender: str = "male", ensure_unique: bool = True) -> str:
        gender = gender.lower()
        key = f"elf_{gender}"
        
        while True:
            if gender == "male":
                prefix = random.choice(NameComponents.ELF_MALE_PREFIXES)
                suffix = random.choice(NameComponents.ELF_MALE_SUFFIXES)
            else:
                prefix = random.choice(NameComponents.ELF_FEMALE_PREFIXES)
                suffix = random.choice(NameComponents.ELF_FEMALE_SUFFIXES)
            
            name = prefix + suffix
            
            if not ensure_unique or name not in self.generated_names[key]:
                self.generated_names[key].add(name)
                return name
    
    def generate_human_name(self, gender: str = "male", ensure_unique: bool = True) -> str:
        gender = gender.lower()
        key = f"human_{gender}"
        
        if gender == "male":
            names = NameComponents.HUMAN_MALE_NAMES
        else:
            names = NameComponents.HUMAN_FEMALE_NAMES
        
        while True:
            name = random.choice(names)
            
            if not ensure_unique or name not in self.generated_names[key]:
                self.generated_names[key].add(name)
                return name
    
    def generate_orc_name(self, gender: str = "male", ensure_unique: bool = True) -> str:
        gender = gender.lower()
        key = f"orc_{gender}"
        
        while True:
            if gender == "male":
                prefix = random.choice(NameComponents.ORC_MALE_PREFIXES)
                suffix = random.choice(NameComponents.ORC_MALE_SUFFIXES)
            else:
                prefix = random.choice(NameComponents.ORC_FEMALE_PREFIXES)
                suffix = random.choice(NameComponents.ORC_FEMALE_SUFFIXES)
            
            name = prefix + suffix
            
            if not ensure_unique or name not in self.generated_names[key]:
                self.generated_names[key].add(name)
                return name
            
    def generate_goblin_name(self, ensure_unique: bool = True) -> str:
        while True:
            prefix = random.choice(NameComponents.GOBLIN_PREFIXES)
            suffix = random.choice(NameComponents.GOBLIN_SUFFIXES)
            name = prefix + suffix
            
            if not ensure_unique or name not in self.generated_names["goblin"]:
                self.generated_names["goblin"].add(name)
                return name
    
    def generate_troll_name(self, ensure_unique: bool = True) -> str:
        while True:
            prefix = random.choice(NameComponents.TROLL_PREFIXES)
            suffix = random.choice(NameComponents.TROLL_SUFFIXES)
            name = prefix + suffix
            
            if not ensure_unique or name not in self.generated_names["troll"]:
                self.generated_names["troll"].add(name)
                return name
    
    def generate_wizard_name(self, ensure_unique: bool = True) -> str:
        while True:
            prefix = random.choice(NameComponents.WIZARD_PREFIXES)
            suffix = random.choice(NameComponents.WIZARD_SUFFIXES)
            name = prefix + suffix
            
            if not ensure_unique or name not in self.generated_names["wizard"]:
                self.generated_names["wizard"].add(name)
                return name
    
    def generate_animal_name(self, animal_type: str = "generic", ensure_unique: bool = True) -> str:
        animal_names = {
            "squirrel": ["Nutkin", "Acorn", "Bushy", "Whisker", "Dart", "Scamper", "Twitch", "Zippy"],
            "rabbit": ["Hoppy", "Fluff", "Cotton", "Clover", "Nibbles", "Hopper", "Dash", "Pepper"],
            "chicken": ["Bawk", "Cluck", "Hennie", "Rooster", "Eggy", "Rusty", "Goldie", "Red"],
            "frog": ["Croak", "Ribbit", "Lily", "Taddy", "Hop", "Splash", "Bumpy", "Green"],
            "sheep": ["Wool", "Fluffy", "Baa", "Daisy", "Cloud", "Cottony", "Soft", "Cream"],
            "pig": ["Oink", "Truffle", "Muddy", "Porky", "Pink", "Snout", "Piggy", "Curly"],
            "cow": ["Bessie", "Moo", "Daisy", "Buttercup", "Lily", "Patches", "Molly", "Maggie"],
            "ox": ["Strong", "Bull", "Ox", "Tank", "Sturdy", "Mighty", "Horns", "Taurus"],
            "goat": ["Billy", "Nanny", "Bleater", "Cliff", "Horn", "Butt", "Jumpy", "Rebel"],
            "bull": ["Brutus", "Furor", "Rampage", "Horned", "Charge", "Toro", "Beast", "Thunder"],
            "boar": ["Tusks", "Savage", "Grinder", "Wild", "Bristle", "Rampage", "Tusker", "Gore"],
            "bear": ["Bruno", "Grizzly", "Bear", "Furious", "Ursus", "Honey", "Paws", "Roar"],
            "snake": ["Sssss", "Slither", "Venom", "Fang", "Scales", "Hiss", "Serpent", "Cobra"],
            "bee": ["Buzzy", "Sting", "Honey", "Zoom", "Bee", "Swarm", "Flutter", "Pollinator"],
            "horse": ["Thunderstrike", "Spirit", "Midnight", "Storm", "Shadow", "Swift", "Lightning", "Charge"],
            "dog": ["Rex", "Fido", "Scout", "Buddy", "Max", "Duke", "Barkley", "Rover"],
            "cat": ["Whiskers", "Mittens", "Paws", "Shadow", "Smokey", "Tiger", "Luna", "Socks"],
            "bird": ["Tweet", "Chirp", "Sky", "Feather", "Wing", "Soar", "Robin", "Sparrow"],
            "shark": ["Jaws", "Bite", "Predator", "Fins", "Razortooth", "Reef", "Blue", "Hunter"],
            "whale": ["Leviathan", "Mighty", "Depths", "Spout", "Blue", "Orca", "Whale", "Giant"],
            "generic": ["Shadow", "Swift", "Hunter", "Whisper", "Echo", "Storm", "Flame", "Frost"]
        }
        
        names_list = animal_names.get(animal_type.lower(), animal_names["generic"])
        
        while True:
            name = random.choice(names_list)
            if not ensure_unique or name not in self.generated_names["animal"]:
                self.generated_names["animal"].add(name)
                return name
    
    
    def generate_generic_name(self, syllables: int = 2, ensure_unique: bool = True) -> str:
        syllables = max(1, min(syllables, 4))
        
        while True:
            name = ""
            for _ in range(syllables):
                name += random.choice(NameComponents.FANTASY_SYLLABLES)
            
            name = name[0].upper() + name[1:].lower()
            
            if not ensure_unique or name not in self.generated_names["generic"]:
                self.generated_names["generic"].add(name)
                return name
    
    def generate_race_name(self, race: str, gender: str = "male", ensure_unique: bool = True) -> str:
        race = race.lower()
        
        if race == "dwarf":
            return self.generate_dwarf_name(gender, ensure_unique)
        elif race == "elf":
            return self.generate_elf_name(gender, ensure_unique)
        elif race == "human":
            return self.generate_human_name(gender, ensure_unique)
        elif race == "orc":
            return self.generate_orc_name(gender, ensure_unique)
        elif race == "goblin":
            return self.generate_goblin_name(ensure_unique)
        elif race == "troll":
            return self.generate_troll_name(ensure_unique)
        elif race == "wizard":
            return self.generate_wizard_name(ensure_unique)
        else:
            return self.generate_generic_name(ensure_unique=ensure_unique)
    
    def generate_names_batch(self, count: int, race: str, gender: str = "male") -> List[str]:
        names = []
        for _ in range(count):
            name = self.generate_race_name(race, gender, ensure_unique=True)
            names.append(name)
        return names
    
    def get_name_statistics(self) -> Dict[str, int]:
        stats = {}
        for key, names in self.generated_names.items():
            stats[key] = len(names)
        return stats
    
    def clear_generated_names(self):
        self._initialize_name_sets()
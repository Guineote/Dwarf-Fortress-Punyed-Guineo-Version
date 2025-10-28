import random
from Classes.enums import Occupation
from Classes.GameObjects import Dwarf
from Classes.name_generator import NameGenerator  


class DwarfData:
    def __init__(self, name, gender, occupation, stats=None):
        self.name = name
        self.gender = gender  
        self.occupation = occupation
        self.is_occupied = False
        self.current_activity = "Idle"
        self.stats = stats or {
            "strength": random.randint(3, 10),
            "agility": random.randint(3, 10),
            "intelligence": random.randint(3, 10)
        }
        self.sprite = None

    def __repr__(self):
        return f"{self.name} ({self.gender}, {self.occupation.value}) - {self.current_activity}"


class ColonyDwarves:
    def __init__(self, colony):
        self.colony = colony
        self.dwarves = []
        self.name_generator = NameGenerator()  
        self._generate_initial_dwarves()

    def _generate_initial_dwarves(self):
        total_dwarves = random.randint(6, 12)
        for _ in range(total_dwarves):
            # 50% probabilidad de género
            gender = random.choice(["male", "female"])
            name = self.name_generator.generate_dwarf_name(gender=gender, ensure_unique=True)
            occupation = random.choice(list(Occupation))
            dwarf = DwarfData(name, gender, occupation)
            self.dwarves.append(dwarf)

    def create_visuals(self, base_pos):
        """Genera los sprites de los enanos y los guarda en cada DwarfData."""
        dwarves_visuals = []
        start_x, start_y = base_pos
        offset = 60
        for i, dwarf_data in enumerate(self.dwarves):
            pos = (start_x + i * offset - (len(self.dwarves) * offset // 2), start_y)
            dwarf_sprite = Dwarf(pos)
            dwarf_data.sprite = dwarf_sprite
            dwarves_visuals.append(dwarf_sprite)
        return dwarves_visuals

    def list_dwarves(self):
        print("\n=== Enanos en la colonia ===")
        for dwarf in self.dwarves:
            s = dwarf.stats
            print(
                f"• {dwarf.name} | {dwarf.gender.capitalize()} | {dwarf.occupation.value} | "
                f"Fuerza: {s['strength']} | Agilidad: {s['agility']} | "
                f"Inteligencia: {s['intelligence']} | Estado: {dwarf.current_activity}"
            )

    def get_idle_dwarves(self):
        return [d for d in self.dwarves if not d.is_occupied]
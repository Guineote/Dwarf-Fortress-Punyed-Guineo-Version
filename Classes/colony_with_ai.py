from Classes.data_structures import *
from Classes.enums import *
from Classes.characters import *
from Classes.decisionMaker import DecisionMaker
from Classes.needsystem import NeedsSystem
from Classes.tasksystem import Task, TaskType, TaskPriority
from Classes.name_generator import NameGenerator
from Classes.random_events import RandomEventSystem
from Classes.biome_system import BiomeSystem
import random

class Colony:
    def __init__(self, biome: Biome = Biome.FOREST):
        self.population = LinkedList()
        self.resources = {
            "water": 0,
            "wood": 0,
            "meat": 0,
            "fish": 0,
            "ore": 0,
            "stone": 0
        }
        
        self.buildings = {"General Warehouse": 1}
        self.time_days = 0
        self.general_morale = 75.0
        self.active_event = None
        
        self.decision_maker = DecisionMaker(self)
        self.name_generator = NameGenerator()
        self.event_system = RandomEventSystem()
        
        self.biome = biome
        self.biome_system = BiomeSystem(biome)
        
        self.resource_history = Deque()
        self.max_history = 20
        
        self._create_initial_population()
    
    def _create_initial_population(self):
        
        self.population.add(Fisherman(self.name_generator.generate_dwarf_name("male"),
            random.randint(80, 150), Gender.MALE, Race.DWARF))
        self.population.add(Fisherman(
            self.name_generator.generate_dwarf_name("female"),
            random.randint(80, 150), Gender.FEMALE, Race.DWARF))
        
        self.population.add(Lumberjack(
            self.name_generator.generate_orc_name("male"),
            random.randint(30, 60), Gender.MALE, Race.ORC))
        self.population.add(Lumberjack(
            self.name_generator.generate_dwarf_name("male"),
            random.randint(80, 150), Gender.MALE, Race.DWARF))
        
        self.population.add(Hunter(
            self.name_generator.generate_elf_name("male"),
            random.randint(200, 600), Gender.MALE, Race.ELF))
        self.population.add(Hunter(
            self.name_generator.generate_human_name("female"),
            random.randint(25, 50), Gender.FEMALE, Race.HUMAN))
        
        self.population.add(Builder(
            self.name_generator.generate_dwarf_name("male"),
            random.randint(80, 150), Gender.MALE, Race.DWARF))
        self.population.add(Builder(
            self.name_generator.generate_dwarf_name("male"),
            random.randint(80, 150), Gender.MALE, Race.DWARF))
        
        self.population.add(Builder(
            self.name_generator.generate_human_name("male"),
            random.randint(25, 50), Gender.MALE, Race.HUMAN))
        self.population.add(Builder(
            self.name_generator.generate_dwarf_name("female"),
            random.randint(80, 150), Gender.FEMALE, Race.DWARF))
        
        self.population.add(Warrior(
            self.name_generator.generate_dwarf_name("male"),
            random.randint(80, 150), Gender.MALE, Race.DWARF))
        self.population.add(Warrior(
            self.name_generator.generate_orc_name("male"),
            random.randint(30, 60), Gender.MALE, Race.ORC))
        self.population.add(Warrior(
            self.name_generator.generate_human_name("male"),
            random.randint(25, 50), Gender.MALE, Race.HUMAN))
        
        for dwarf in self.population.iterate():
            dwarf.needs_system = NeedsSystem()
    
    def count_population(self) -> int:
        return len(self.population)
    
    def count_available_workers(self) -> int:
        count = 0
        for dwarf in self.population.iterate():
            if not dwarf.is_occupied and dwarf.is_alive:
                count += 1
        return count
    
    def analyze_colony_state(self):
        state = HashTable()
        
        total_pop = self.count_population()
        available = self.count_available_workers()
        
        state.insert("total_population", total_pop)
        state.insert("available_workers", available)
        
        state.insert("water", self.resources.get("water", 0))
        state.insert("water_needed", total_pop * 5)
        
        food_total = self.resources.get("meat", 0) + self.resources.get("fish", 0)
        state.insert("food", food_total)
        state.insert("food_needed", total_pop * 3)
        
        state.insert("wood", self.resources.get("wood", 0))
        state.insert("wood_needed", 50)
        
        state.insert("ore", self.resources.get("ore", 0))
        state.insert("ore_needed", 30)
        
        state.insert("under_attack", self.active_event == "attack")
        
        houses_needed = total_pop > len(self.buildings) * 4
        state.insert("needs_housing", houses_needed)
        
        return state
    
    def consume_daily_resources(self):
        total_population = self.count_population()
        
        water_use = total_population * 2
        self.resources["water"] = max(0, self.resources["water"] - water_use)
        
        food_use = total_population * 1.5
        available_food = self.resources["meat"] + self.resources["fish"]
        
        if available_food >= food_use:
            if self.resources["fish"] >= food_use:
                self.resources["fish"] -= food_use
            else:
                self.resources["fish"] = 0
                self.resources["meat"] -= (food_use - self.resources["fish"])
        else:
            self.general_morale -= 5
            self.resources["meat"] = 0
            self.resources["fish"] = 0
    
    def update_morale(self):
        total_morale = 0.0
        counter = 0
        
        for dwarf in self.population.iterate():
            if hasattr(dwarf, 'needs_system'):
                happiness = dwarf.needs_system.get_overall_happiness()
                total_morale += happiness
                counter += 1
                
                if self.resources["water"] > 30 and (self.resources["meat"] + self.resources["fish"]) > 40:
                    dwarf.needs_system.satisfy_need("comfort", 5)
        
        if counter > 0:
            self.general_morale = total_morale / counter
    
    def rest_dwarves(self):
        for dwarf in self.population.iterate():
            if hasattr(dwarf, 'needs_system'):
                sleep_need = dwarf.needs_system.needs.get("sleep")
                if sleep_need and sleep_need.value < 30:
                    dwarf.is_occupied = False
    
    def generate_random_event(self):
        if random.random() < 0.15:  
            events = [
                ("goblin_attack", 10),
                ("storm", 8),
                ("discovery", 5)
            ]
            
            event_type, _ = random.choice(events)
            
            if event_type == "goblin_attack":
                print("\nGoblin attack!")
                self.active_event = "attack"
                
                for _ in range(3):
                    task = Task(TaskType.DEFEND_COLONY, TaskPriority.CRITICAL, duration=2.0, required_skill="warrior")
                    self.decision_maker.job_manager.add_task(task)
                self.decision_maker.job_manager.process_buffer()
            
            elif event_type == "storm":
                print("\nStorm! Resources damaged.")
                self.resources["wood"] = max(0, self.resources["wood"] - 5)
                self.general_morale -= 5
            
            elif event_type == "discovery":
                print("\nDiscovery! A mineral vein was found.")
                self.resources["ore"] += 15
                self.general_morale += 5
    
    def apply_completed_tasks(self):
        completed = self.decision_maker.job_manager.completed_tasks
        
        for task in completed.iterate():
            t_type = task.task_type
            
            if t_type == TaskType.COLLECT_WATER:
                self.resources["water"] += random.randint(5, 10)
            elif t_type == TaskType.CHOP_TREE:
                self.resources["wood"] += random.randint(5, 12)
            elif t_type == TaskType.HUNT_ANIMAL:
                self.resources["meat"] += random.randint(8, 15)
            elif t_type == TaskType.FISH:
                self.resources["fish"] += random.randint(6, 12)
            elif t_type == TaskType.MINE_ORE:
                self.resources["ore"] += random.randint(5, 10)
            elif t_type == TaskType.MINE_STONE:
                self.resources["stone"] += random.randint(5, 10)
            elif t_type == TaskType.BUILD_STRUCTURE:
                building_name = task.metadata.obtener("building", "House")
                self.buildings[building_name] = self.buildings.get(building_name, 0) + 1
            elif t_type == TaskType.DEFEND_COLONY:
                self.active_event = None
                self.general_morale += 3
            elif t_type == TaskType.SOCIALIZE:
                self.general_morale += 1
        
        completed.vaciar()

    def store_resource_history(self):
        snapshot = HashTable()
        for key, value in self.resources.items():
            snapshot.insert(key, value)
        
        self.resource_history.add_back(snapshot)
        
        if len(self.resource_history) > self.max_history:
            self.resource_history.remove_front()

    def analyze_trends(self):
        if len(self.resource_history) < 2:
            return HashTable()
        
        latest = self.resource_history[-1]
        previous = self.resource_history[-2]
        
        trends = HashTable()
        for key in self.resources.keys():
            diff = latest.obtener(key) - previous.obtener(key)
            trends.insert(key, diff)
        
        return trends

    def predict_shortage(self, resource_name, turns_ahead=5):
        if len(self.resource_history) < 2:
            return False
    
        states = []
        for state in self.resource_history.iterate():
            states.append(state)
    
        if len(states) >= 2:
            last = states[-1].get(resource_name)
            prev = states[-2].get(resource_name)

            if last is not None and prev is not None:
                consumption = max(0, prev - last)
                stimated = last - (consumption * turns_ahead)
                return stimated < 10
    
        return False


    def ai_turn(self):
        self.time_days += 1
        colony_state = self.analyze_colony_state()
    
        print("\n Colony Analysis:")
        print(f"  Population: {colony_state.get('total_population')}")
        print(f"  Available Workers: {colony_state.get('available_workers')}")
        print(f"  Water: {colony_state.get('water')}/{colony_state.get('water_needed')}")
        print(f"  Food: {colony_state.get('food')}/{colony_state.get('food_needed')}")
        print(f"  Wood: {colony_state.get('wood')}/{colony_state.get('wood_needed')}")
        print(f"  Ore: {colony_state.get('ore')}/{colony_state.get('ore_needed')}")

        self.decision_maker.generate_colony_tasks(colony_state)
        self.decision_maker.update_all_characters(self.population, time_units=1.0)

        self.apply_completed_tasks()

        self.consume_daily_resources()

        self.update_morale()

        self.rest_dwarves()

        self.generate_random_event()

        self.record_historic_state(colony_state)

        stats = self.decision_maker.job_manager.get_statistics()
        print(f"\n Tasks: Pending:{stats.get('pending')} | Active:{stats.get('active')} | Completed:{stats.get('completed')}")
    
        print(f"\n Current Activities:")
        active_count = 0
        for dwarf in self.population.iterate():
            if dwarf.is_occupied and dwarf.current_activity:
                print(f"  • {dwarf.name}: {dwarf.current_activity}")
                active_count += 1
                if active_count >= 5:
                    break
    
        if active_count == 0:
            print("  (No active work)")
    
        return colony_state


    def show_state(self):
    
        print("\nRESOURCES:")
        for resource, amount in self.resources.items():
            emoji = {"water": "💧", "wood": "🪵", "meat": "🥩", "fish": "🐟", "ore": "⚒️", "stone": "🪨"}
        
            trend = self.get_resource_trend(resource)
            trend_emoji = {"INCREASING": "📈", "DECREASING": "📉", "STABLE": "➡️"}
        
            print(f"  {emoji.get(resource, '📦')} {resource.capitalize()}: {amount} {trend_emoji.get(trend, '')}")
    
        print("\n POPULATION:")
        for dwarf in self.population.iterate():
            status = "🔵 Working" if dwarf.is_occupied else "⚪ Available"
        
            happiness = "???"
            if hasattr(dwarf, 'needs_system'):
                happiness = f"{dwarf.needs_system.get_overall_happiness():.0f}%"
        
            print(f"  {status} | {dwarf.name} ({dwarf.occupation.value}) | Happiness: {happiness}")
    
        print(f"\nBUILDINGS: {len(self.buildings)}")
        for building, count in self.buildings.items():
            print(f"  {building}: {count}")
    
        print(f"\nBIOME: {self.biome.value.capitalize()}")
        print(f"  Temperature: {self.biome_system.temperature}°C")
        print(f"  Danger Level: {self.biome_system.danger_level:.0f}%")


    def generate_ai_report(self):
    
        print("\nResource Trends:")
        resources = ["water", "wood", "meat", "fish", "ore"]
        for resource in resources:
            trend = self.get_resource_trend(resource)
            shortage = self.predict_shortage(resource, turns_ahead=3)
            warning = " SHORTAGE PREDICTED!" if shortage else ""
            print(f"  {resource.capitalize()}: {trend}{warning}")
    
        print("\nAI Statistics:")
        stats = self.decision_maker.job_manager.get_statistics()
        print(f"  Total Days: {self.time_days}")
        print(f"  Completed Tasks: {stats.get('completed')}")
        print(f"  Active Workers: {stats.get('active')}")
        print(f"  Decisions Made: {len(self.decision_maker.decision_history)}")
    
        print("\n👥 Population Analysis:")
        happy_count = 0
        unhappy_count = 0
    
        for dwarf in self.population.iterate():
            if hasattr(dwarf, 'needs_system'):
                happiness = dwarf.needs_system.get_overall_happiness()
                if happiness > 60:
                    happy_count += 1
                elif happiness < 40:
                    unhappy_count += 1
    
        print(f"  Happy: {happy_count}")
        print(f"  Unhappy: {unhappy_count}")
        print(f"  General Morale: {self.general_morale:.1f}%")


    def simulate_days(self, num_days=10):
        for day in range(num_days):
            self.ai_turn()
            if self.resources["water"] < 10:
                print("\nCRITICAL: Extremely low water levels!")
        
            if (self.resources["meat"] + self.resources["fish"]) < 10:
                print("\nCRITICAL: Food shortage detected!")
        
            if self.general_morale < 30:
                print("\nCRITICAL: Morale dangerously low!")
    
        self.show_state()
        self.generate_ai_report()
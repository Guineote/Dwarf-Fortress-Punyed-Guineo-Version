# stress_test_pure_logic.py
# Prueba de estrés: 50 tareas, 100% lógica, SIN pygame
# Solo Colony, Dwarf (simulado), Task, Queue

from Classes.colony_with_ai import Colony
from Classes.enums import Biome
from Classes.tasksystem import Task, TaskType, TaskPriority
from Classes.data_structures import Queue
import random
import time

class SimDwarf:
    def __init__(self, name, pos):
        self.name = name
        self.rect = type('Rect', (), {'center': pos})()
        self.home_pos = pos
        self.colony = None
        self.is_busy = False
        self.task = None
        self.target_obj = None
        self.state = "idle"
        self.task_start_time = 0
        self.task_duration = 0

    def assign_task(self, task, world_objects, pozo):
        if self.is_busy:
            return False

        self.is_busy = True
        self.task = task
        self.target_obj = None

        # Simular búsqueda de objetivo
        if task.task_type == TaskType.CHOP_TREE:
            trees = [o for o in world_objects if o.type in ["tree", "forest_tree"] and not o.is_targeted]
            if trees:
                self.target_obj = random.choice(trees)
                self.target_obj.is_targeted = True

        elif task.task_type == TaskType.MINE_ORE:
            ores = [o for o in world_objects if o.type in ["stone", "bronze", "iron", "gold", "diamond"] and not o.is_targeted]
            if ores:
                self.target_obj = random.choice(ores)
                self.target_obj.is_targeted = True

        elif task.task_type == TaskType.COLLECT_WATER:
            self.target_obj = pozo

        elif task.task_type == TaskType.HUNT_ANIMAL:
            animals = [o for o in world_objects if o.type == "animal" and o.alive and not o.is_targeted]
            if animals:
                self.target_obj = random.choice(animals)
                self.target_obj.is_targeted = True

        elif task.task_type == TaskType.FISH:
            self.target_obj = type('Water', (), {'type': 'water'})()

        elif task.task_type == TaskType.DEFEND_COLONY:
            enemies = [o for o in world_objects if o.type in ["dragon", "minotaur"]]
            if enemies:
                self.target_obj = random.choice(enemies)
                self.target_obj.is_targeted = True

        elif task.task_type in [TaskType.BUILD_STRUCTURE, TaskType.SOCIALIZE, TaskType.TRAIN_COMBAT, TaskType.HAUL_ITEM]:
            self.target_obj = type('Dummy', (), {'type': 'task_point'})()

        if not self.target_obj and task.task_type not in [TaskType.BUILD_STRUCTURE, TaskType.SOCIALIZE, TaskType.TRAIN_COMBAT, TaskType.HAUL_ITEM]:
            self.is_busy = False
            self.task = None
            return False

        self.state = "working"
        self.task_start_time = time.time()
        base = 2.0  
        self.task_duration = base + random.uniform(0, 1.5)
        return True

    def update(self):
        if not self.is_busy or self.state != "working":
            return

        if time.time() - self.task_start_time >= self.task_duration:
            gained = 0
            resource = "unknown"
            obj_type = getattr(self.target_obj, "type", "")

            if obj_type in ["tree", "forest_tree"]:
                gained = random.randint(8, 15)
                resource = "wood"
            elif obj_type in ["stone", "bronze", "iron", "gold", "diamond"]:
                gained = random.randint(10, 25)
                resource = "ore" if obj_type != "stone" else "stone"
            elif obj_type == "pozo":
                gained = random.randint(5, 10)
                resource = "water"
            elif obj_type == "animal":
                gained = random.randint(10, 20)
                resource = "meat"
            elif obj_type == "water":
                gained = random.randint(6, 12)
                resource = "fish"
            else:
                gained = random.randint(3, 8)
                resource = "wood"

            if self.colony and gained > 0:
                self.colony.resources[resource] = self.colony.resources.get(resource, 0) + gained

            if self.target_obj and hasattr(self.target_obj, "is_targeted"):
                self.target_obj.is_targeted = False

            # Reset
            self.is_busy = False
            self.task = None
            self.target_obj = None
            self.state = "idle"


class SimObject:
    def __init__(self, obj_type):
        self.type = obj_type
        self.is_targeted = False
        self.alive = True

print("INICIANDO PRUEBA DE ESTRÉS (LÓGICA PURA)")
print("═" * 60)

colony = Colony(biome=Biome.FOREST)
dwarves = []

for dwarf_data in colony.population.iterate():
    dwarf = SimDwarf(dwarf_data.name, (2700, 550))
    dwarf.colony = colony
    dwarves.append(dwarf)

task_queue = Queue()

world_objects =[]
pozo = SimObject("pozo")

for _ in range(25):
    world_objects.append(SimObject(random.choice(["tree", "forest_tree"])))

for _ in range(20):
    world_objects.append(SimObject(random.choice(["stone", "bronze", "iron", "gold", "diamond"])))

for _ in range(15):
    animal = SimObject("animal")
    world_objects.append(animal)

world_objects.extend([SimObject("dragon"), SimObject("minotaur")])

ACTIONS = [
    ("Talar", TaskType.CHOP_TREE, TaskPriority.HIGH),
    ("Minar", TaskType.MINE_ORE, TaskPriority.HIGH),
    ("Agua", TaskType.COLLECT_WATER, TaskPriority.NORMAL),
    ("Cazar", TaskType.HUNT_ANIMAL, TaskPriority.HIGH),
    ("Pescar", TaskType.FISH, TaskPriority.NORMAL),
    ("Construir", TaskType.BUILD_STRUCTURE, TaskPriority.NORMAL),
    ("Reparar", TaskType.REPAIR_STRUCTURE, TaskPriority.NORMAL),
    ("Socializar", TaskType.SOCIALIZE, TaskPriority.IDLE),
    ("Entrenar", TaskType.TRAIN_COMBAT, TaskPriority.NORMAL),
    ("Defender", TaskType.DEFEND_COLONY, TaskPriority.CRITICAL),
    ("Transportar", TaskType.HAUL_ITEM, TaskPriority.LOW),
]

start_time = time.time()
initial_resources = colony.resources.copy()
completed = 0

print("Encolando 50 tareas...")
for i in range(50):
    name, ttype, prio = random.choice(ACTIONS)
    task = Task(ttype, prio)
    task_queue.enqueue(task)
    print(f"  [{i+1:2d}] {name}")

print("\nEjecutando...")
print("═" * 60)

while completed < 50:
    for dwarf in dwarves:
        if not dwarf.is_busy and not task_queue.is_empty():
            task = task_queue.dequeue()
            if dwarf.assign_task(task, world_objects, pozo):
                completed += 0  # Se cuenta al finalizar

    # Actualizar
    for dwarf in dwarves:
        dwarf.update()
        if not dwarf.is_busy and dwarf.task is None and dwarf.state == "idle":
            completed += 1
            if completed <= 50:
                print(f"Completadas: {completed}/50")

    if completed >= 50:
        break

    time.sleep(0.01)  # Simular 100 FPS

end_time = time.time()
elapsed = end_time - start_time
minutes = elapsed / 60

print("\n" + "═" * 60)
print("PRUEBA COMPLETADA")
print("═" * 60)
print(f"Tareas: {completed}/50")
print(f"Tiempo: {elapsed:.1f}s ({minutes:.2f} min)")
print(f"Rendimiento: {completed/minutes:.1f} tareas/min")

print("\nRECURSOS GANADOS:")
gained = {k: colony.resources.get(k, 0) - initial_resources.get(k, 0) for k in colony.resources}
for res, amt in gained.items():
    if amt > 0:
        print(f"  {res.capitalize():6}: +{amt}")

print("\nINVENTARIO FINAL:")
for res, amt in colony.resources.items():
    print(f"  {res.capitalize():6}: {amt}")

print(f"\nMorale: {colony.general_morale:.1f}%")
print(f"Enanos: {len(dwarves)}")
print("═" * 60)
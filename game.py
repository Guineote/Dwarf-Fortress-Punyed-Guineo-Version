from Classes.GameObjects import *
from Classes.colony_with_ai import *
from Classes.enums import Biome
from Classes.tasksystem import Task, TaskType, TaskPriority
from Classes.colony_dwarves import ColonyDwarves
from Classes.structures import House
import pygame 
import sys
import random

pygame.init()
colony = Colony(biome=Biome.FOREST)
colony_dwarves = ColonyDwarves(colony)
colony_dwarves.list_dwarves()

invaders = []  
event_timer = 0
event_cooldown = 3600  # ~1 min a 60fps

bioma_w = 800
bioma_h = 800
WIDTH, HEIGHT = 800, 800
WORLD_H = bioma_h
WORLD_W = bioma_w * 8

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dwarf Fortress')
PUNTERO = pygame.image.load("Assets/Img/Puntero.png").convert_alpha()
tundra_bg = pygame.image.load("Assets/Img/Tundra.png").convert()
grassland_bg = pygame.image.load("Assets/Img/Grassland.png").convert()
swamp_bg = pygame.image.load("Assets/Img/Swamp.png").convert()
forest_bg = pygame.image.load("Assets/Img/Forest.png").convert()
desert_bg = pygame.image.load("Assets/Img/desert_bg.png").convert()
aquatic_bg = pygame.image.load("Assets/Img/Aquatic.png").convert()
mountain_bg = pygame.image.load("Assets/Img/Mountain.png").convert()
volcano_bg = pygame.image.load("Assets/Img/Volcano.png").convert()
pozo_img = pygame.image.load('Assets/Img/pozo_green.png').convert_alpha()
pozo_img = pygame.transform.scale(pozo_img, (150, 150))
pozo_img_d = pygame.image.load('Assets/Img/pozo_dessert.png').convert_alpha()
pozo_img_d = pygame.transform.scale(pozo_img, (150, 150))
baobab_img = pygame.image.load('Assets/Img/baobab.png')
townhall = pygame.image.load('Assets/Img/TownHall.png').convert_alpha()
townhall_pos = townhall.get_rect(center=(WIDTH // 2, HEIGHT // 2))

font = pygame.font.Font('Assets/Font/headstone.ttf', 30)
town_text = font.render("Centro de acopio", True, (255, 255, 255))

clock = pygame.time.Clock()
player = pygame.Rect(200, 400, 50, 50)
speed = 8

camera_x = 0
camera_y = 0

start_x = 0
start_y = 0

menu_h = 400
menu_w = 150
menu_x_pos = 10
menu_y_pos = 10

MENU_COLOR = (50, 50, 50, 200)
MENU_RECT = pygame.Rect(menu_x_pos, menu_y_pos, menu_w, menu_h)
menu_font = pygame.font.Font('Assets/Font/headstone.ttf', 20)
menu_visible = False

BIOMAS = {
    "Desert":    (0, 800),
    "Swamp":     (800, 1600),
    "Grassland": (1600, 2400),
    "Forest":    (2400, 3200),
    "Aquatic":   (3200, 4000),
    "Tundra":    (4000, 4800),
    "Mountain":  (4800, 5600),
    "Volcano":   (5600, 6400)
}

def respawn_animals(objects):
    GROUND_Y = 750
    important_rects = [obj.rect for obj in objects if hasattr(obj, 'rect')] 
    
    dead_animals = [obj for obj in objects if isinstance(obj, (Pig, Sheep, Chicken)) and not getattr(obj, "alive", True)]
    for dead in dead_animals:
        objects.remove(dead) 
        
    bioma_animales = {
        "Grassland": [(Pig, 3, 5), (Sheep, 2, 4), (Chicken, 3, 6)],
        "Forest": [(Chicken, 2, 4)],
        "Swamp": [(Pig, 1, 3)],
        "Tundra": [(Sheep, 1, 2)]
    }

    for bioma, (start_x, end_x) in BIOMAS.items():
        if bioma in bioma_animales:
            for AnimalClass, min_count, max_count in bioma_animales[bioma]:
                for _ in range(random.randint(min_count, max_count)):
                    x = random.randint(start_x + 100, end_x - 100)  
                    y = GROUND_Y - 20
                    animal = AnimalClass((x, y))
                    if not any(animal.rect.colliderect(r) for r in important_rects):
                        objects.append(animal)
                        print(f"🐖 Respawn de {AnimalClass.__name__} en {bioma} en nueva posición: ({x}, {y})")

def generate_world_objects():
    objects = []
    GROUND_Y = 750 
    pozo = Pozo(forest_center[0] + 300, forest_center[1] + 300, pozo_img)
    
    important_rects = [
    townhall.get_rect(center=(forest_center[0], forest_center[1] + 150)),
    pozo.rect
]
    iron_count = 0
    stone_count = 0
    
    for bioma, (start_x, end_x) in BIOMAS.items():
        if bioma == "Forest":
            for _ in range(random.randint(3, 6)):
                x = random.randint(start_x + 50, end_x - 50)
                tree = ForestTree((x, GROUND_Y))
                tree.rect.bottom = GROUND_Y  
                if not any(tree.rect.colliderect(r) for r in important_rects):
                    objects.append(tree)

        elif bioma == "Desert":
            for _ in range(random.randint(5, 15)):
                x = random.randint(start_x + 50, end_x - 50)
                ore_type = random.choice(["stone", "bronze", "iron", "gold", "diamond"])
                if ore_type == "stone":
                    ore = Rock((x, GROUND_Y))
                    stone_count += 1
                elif ore_type == "bronze":
                    ore = Bronze((x, GROUND_Y))
                elif ore_type == "iron":
                    ore = Iron((x, GROUND_Y))
                    iron_count += 1
                elif ore_type == "gold":
                    ore = Gold((x, GROUND_Y))
                elif ore_type == "diamond":
                    ore = Diamond((x, GROUND_Y))
                ore.rect.bottom = GROUND_Y
                objects.append(ore)

        elif bioma == "Mountain":
            for _ in range(random.randint(5, 20)):
                x = random.randint(start_x + 50, end_x - 50)
                ore_type = random.choice(["stone", "bronze", "iron", "gold", "diamond"])
                if ore_type == "stone":
                    ore = Rock((x, GROUND_Y))
                    stone_count +=1
                elif ore_type == "bronze":
                    ore = Bronze((x, GROUND_Y))
                elif ore_type == "iron":
                    ore = Iron((x, GROUND_Y))
                    iron_count += 1
                elif ore_type == "gold":
                    ore = Gold((x, GROUND_Y))
                elif ore_type == "diamond":
                    ore = Diamond((x, GROUND_Y))
                ore.rect.bottom = GROUND_Y
                objects.append(ore)

        elif bioma == "Grassland":
            for _ in range(random.randint(2, 4)):
                x = random.randint(start_x + 50, end_x - 50)
                tree = Tree((x, GROUND_Y))
                tree.rect.bottom = GROUND_Y
                if not any(tree.rect.colliderect(r) for r in important_rects):
                    objects.append(tree)

        elif bioma == "Swamp":
            for _ in range(random.randint(3, 6)):
                x = random.randint(start_x + 50, end_x - 50)
                swamp_tree = SwampTree((x, GROUND_Y))
                swamp_tree.rect.bottom = GROUND_Y
                if not any(swamp_tree.rect.colliderect(r) for r in important_rects):
                    objects.append(swamp_tree)

        elif bioma == "Tundra":
            for _ in range(random.randint(3, 6)):
                x = random.randint(start_x + 50, end_x - 50)
                tundra_tree = TundraTree((x, GROUND_Y))
                tundra_tree.rect.bottom = GROUND_Y
                if not any(tundra_tree.rect.colliderect(r) for r in important_rects):
                    objects.append(tundra_tree)
                
    # === ANIMALES ===
    bioma_animales = {
        "Grassland": [(Pig, 3, 5), (Sheep, 2, 4), (Chicken, 3, 6)],
        "Forest": [(Chicken, 2, 4)],
        "Swamp": [(Pig, 1, 3)],
        "Tundra": [(Sheep, 1, 2)]
    }

    for bioma, (start_x, end_x) in BIOMAS.items():
        if bioma in bioma_animales:
            for AnimalClass, min_count, max_count in bioma_animales[bioma]:
                for _ in range(random.randint(min_count, max_count)):
                    x = random.randint(start_x + 100, end_x - 100)
                    y = GROUND_Y - 20
                    animal = AnimalClass((x, y))
                    if not any(animal.rect.colliderect(r) for r in important_rects):
                        objects.append(animal)
    
    volcano_start, volcano_end = BIOMAS["Volcano"]
    dragon_x = (volcano_start + volcano_end) // 2
    dragon_y = 400  # Nivel de suelo
    dragon = Dragon(pos=(dragon_x, dragon_y))
    objects.append(dragon)
    mountain_center_x = (BIOMAS["Mountain"][0] + BIOMAS["Mountain"][1]) // 2
    minotaur = Minotaur(pos=(mountain_center_x, 600))
    objects.append(minotaur)

    mountain_start, mountain_end = BIOMAS["Mountain"]
    while iron_count < 5:
        x = random.randint(mountain_start + 50, mountain_end - 50)
        ore = Iron((x, GROUND_Y))
        ore.rect.bottom = GROUND_Y
        if not any(ore.rect.colliderect(r) for r in important_rects):
            objects.append(ore)
            iron_count += 1

    desert_start, desert_end = BIOMAS["Desert"]
    while stone_count < 10:
        x = random.randint(desert_start + 50, desert_end - 50)
        ore = Rock((x, GROUND_Y))
        ore.rect.bottom = GROUND_Y
        if not any(ore.rect.colliderect(r) for r in important_rects):
            objects.append(ore)
            stone_count += 1

    return objects


def draw_world(surface, camera_x, camera_y):
    surface.fill((0, 0, 0))
    desert_rect    = pygame.Rect(0 - camera_x, 0, bioma_w, bioma_h)
    swamp_rect     = pygame.Rect(bioma_w - camera_x, 0, bioma_w, bioma_h)
    grassland_rect = pygame.Rect(2*bioma_w - camera_x, 0, bioma_w, bioma_h)
    forest_rect    = pygame.Rect(3*bioma_w - camera_x, 0, bioma_w, bioma_h)
    aquatic_rect   = pygame.Rect(4*bioma_w - camera_x, 0, bioma_w, bioma_h)
    tundra_rect    = pygame.Rect(5*bioma_w - camera_x, 0, bioma_w, bioma_h)
    mountain_rect  = pygame.Rect(6*bioma_w - camera_x, 0, bioma_w, bioma_h)
    volcano_rect   = pygame.Rect(7*bioma_w - camera_x, 0, bioma_w, bioma_h)
    surface.blit(pygame.transform.scale(tundra_bg, (bioma_w, bioma_h)), tundra_rect)
    surface.blit(pygame.transform.scale(swamp_bg, (bioma_w, bioma_h)), swamp_rect)
    surface.blit(pygame.transform.scale(desert_bg, (bioma_w, bioma_h)), desert_rect)
    surface.blit(pygame.transform.scale(mountain_bg, (bioma_w, bioma_h)), mountain_rect)
    surface.blit(pygame.transform.scale(grassland_bg, (bioma_w, bioma_h)), grassland_rect)
    surface.blit(pygame.transform.scale(forest_bg, (bioma_w, bioma_h)), forest_rect)
    surface.blit(pygame.transform.scale(aquatic_bg, (bioma_w, bioma_h)), aquatic_rect)
    surface.blit(pygame.transform.scale(volcano_bg, (bioma_w, bioma_h)), volcano_rect)

    town_offset_y = 150
    surface.blit(townhall, (forest_rect.centerx - townhall.get_width()//2, 
                            forest_rect.centery - townhall.get_height()//2 + town_offset_y))
    
    return (forest_rect.centerx, forest_rect.centery)

forest_center = draw_world(window, 0, 0)
player.center = forest_center 
pozo = Pozo(forest_center[0] + 300, forest_center[1] + 300, pozo_img)
dwarves = []
dwarves = colony_dwarves.create_visuals((forest_center[0], forest_center[1] + 300))



PUNTERO = pygame.transform.scale(PUNTERO, (player.width, player.height)) 
world_objects = generate_world_objects()

def generate_random_event(colony, town_center, invaders, colony_dwarves):
    import random
    event_system = colony.event_system
    
    print("🎲 Generando evento random...")
    
    if random.random() < 0.5:  
        attacking_races = ["orc", "ogre"]
        attacking_race = random.choice(attacking_races)
        population = colony.count_population()
        event = event_system.invasion_event(
            defending_race=colony.defending_race,
            attacking_race=attacking_race,
            settlement_population=population,
            military_strength=colony.military_strength
        )
        
        if event["occurred"]:
            num_invaders = random.randint(3, 8)
            side = random.choice([-1, 1])
            base_spawn_x = town_center[0] + (side * random.randint(200, 400))
            spawn_y = town_center[1] + random.randint(-100, 100)
            
            spawned = 0
            for i in range(num_invaders):
                x = base_spawn_x + (i * 60 * side)
                y = spawn_y + random.randint(-30, 30)
                
                if attacking_race == "ogre":
                    invader = Ogre((x, y))  
                else:
                    invader = Orc((x, y))
                
                invaders.append(invader)
                spawned += 1
            
            damage = event["damage"]
            food_loss = int(damage * 1.5)
            colony.resources["meat"] = max(0, colony.resources["meat"] - food_loss)
            colony.resources["wood"] = max(0, colony.resources["wood"] - int(damage * 0.5))
            colony.general_morale = max(0, colony.general_morale - (damage / 2))
            
            print(f"🚨 ¡INVASIÓN {attacking_race.upper()}! {spawned} enemigos spawneados.")
            print(f"💥 Daño: {damage}%, Comida perdida: {food_loss}, Madera perdida: {int(damage * 0.5)}")
            print(f"😞 Moral general: {colony.general_morale:.1f}%")
            
            casualties = event.get("casualties", 0)
            if casualties > 0:
                dwarves_list = colony_dwarves.dwarves[:]  
                non_warriors = [d for d in dwarves_list if d.occupation != Occupation.WARRIOR and d.is_alive]
                random.shuffle(non_warriors)
                killed = 0
                for dwarf_data in non_warriors[:casualties]:
                    dwarf_data.is_alive = False
                    killed += 1
                print(f"💀 {killed} dwarves muertos")
        else:
            print(f"🛡️ {attacking_race.capitalize()}s repelidos sin combate.")
    
    else:  
        population = colony.count_population()
        event = event_system.natural_disaster_event(
            biome=colony.biome,
            population=population,
            settlement_durability=colony.settlement_durability
        )
        
        if event["occurred"]:
            damage = event["damage"]
            for res in list(colony.resources.keys()):
                if res not in ["gold", "diamond"]:
                    loss_factor = damage / 100.0
                    colony.resources[res] = max(0, int(colony.resources[res] * (1 - loss_factor)))
            
            colony.settlement_durability = max(0, colony.settlement_durability - (damage / 2))
            colony.general_morale = max(0, colony.general_morale - (damage / 3))
            
            print(f"🌪️ {event['disaster_type']}! Daño: {damage}%")
            print(f"🏚️ Durabilidad asentamiento: {colony.settlement_durability:.1f}")
            print(f"😞 Moral general: {colony.general_morale:.1f}%")
        else:
            print(f"✅ {event['disaster_type']} evitado.")

def print_colony_inventory(colony, world_objects):
    summary = colony.get_colony_summary()  
    
    print("\n=== INVENTARIO DE LA COLONIA ===")
    print("\nRecursos:")
    for res_str in summary["resources"].values():
        print(f"  {res_str}")
    print("\nEdificios:")
    for bld, count in summary["buildings"].items():
        print(f"  {bld}: {count}")
    houses = [obj for obj in world_objects if isinstance(obj, House)]
    if houses:
        print("\nCasas y Habitantes:")
        for house in houses:
            inh_str = ", ".join(house.inhabitants) if house.inhabitants else "Vacía"
            print(f"  {house.name}: {inh_str} ({len(house.inhabitants)}/{house.capacity}) | Comfort: {house.comfort_level:.0f}%")
    print("\nPoblación:")
    for pop in summary["population"]:
        print(f"  • {pop['name']} ({pop['occupation']}) - Happiness: {pop['happiness']} - Status: {pop['status']}")

    print("\nMoral General:")
    print(f"  {summary['general_morale']}")
    print(f"  Happy: {summary['morale_breakdown']['happy']} | Unhappy: {summary['morale_breakdown']['unhappy']}")
    
    print(f"\nBioma: {summary['biome']}")
    
    if summary["trends"]:
        print("\nTendencias de Recursos:")
        for res, diff in summary["trends"].items():
            trend = "INCREASING" if diff > 0 else "DECREASING" if diff < 0 else "STABLE"
            print(f"  {res.capitalize()}: {trend} ({diff})")
    
    if summary["shortages"]:
        print("\nEscasez Predichas:")
        for short in summary["shortages"]:
            print(f"  {short}")
    
    print("=== FIN DEL INVENTARIO ===")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for dwarf in dwarves:
            dwarf.handle_event(event)
            
        if event.type == pygame.MOUSEBUTTONDOWN and menu_visible:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if MENU_RECT.collidepoint(mouse_x, mouse_y):
                relative_y = mouse_y - menu_y_pos
                option_index = relative_y // 30
                actions = ["Talar arbol", "Minar minerales", "Atacar dragon", "Obtener agua", "Cazar animal",
                            "Comer", "Beber", "Dormir", "Construir", "Socializar", "Atacar minotauro", "Random event"]
                if option_index < len(actions):
                    selected_action = actions[option_index]
                    print(f"Comando recibido: {selected_action}")

                    if selected_action == "Talar arbol":
                        task = Task(TaskType.CHOP_TREE, TaskPriority.HIGH)
                    elif selected_action == "Minar minerales":
                        task = Task(TaskType.MINE_ORE, TaskPriority.HIGH)
                    elif selected_action == "Atacar dragon":
                        task = Task(TaskType.ATTACK_DRAGON, TaskPriority.CRITICAL)
                    elif selected_action == "Obtener agua":
                        task = Task(TaskType.COLLECT_WATER, TaskPriority.NORMAL)
                    elif selected_action == "Cazar animal":
                        task = Task(TaskType.HUNT_ANIMAL, TaskPriority.URGENT)
                    elif selected_action == "Comer":
                        task = Task(TaskType.EAT, TaskPriority.URGENT)
                    elif selected_action == "Beber":
                        task = Task(TaskType.DRINK, TaskPriority.URGENT)
                    elif selected_action == "Dormir":
                        task = Task(TaskType.SLEEP, TaskPriority.HIGH)
                    elif selected_action == "Construir":
                        task = Task(TaskType.BUILD, TaskPriority.NORMAL)
                    elif selected_action == "Socializar":
                        task = Task(TaskType.SOCIALIZE, TaskPriority.LOW)
                    elif selected_action == "Atacar minotauro":
                        task = Task(TaskType.ATTACK_MINOTAUR, TaskPriority.CRITICAL)
                    elif selected_action == "Random event":
                        town_offset_y = 150
                        town_center = (forest_center[0], forest_center[1] + town_offset_y)
                        generate_random_event(colony, town_center, invaders, colony_dwarves)  
                        print("🚨 Evento random activado manualmente.")
                        continue
                        #task = Task(TaskType.RANDOM_EVENT, TaskPriority.CRITICAL)

                    colony.decision_maker.job_manager.add_task(task)
                    colony.decision_maker.job_manager.assign_best_dwarf(task, colony_dwarves.dwarves)
                    assigned_dwarf = next((d for d in colony_dwarves.dwarves if d.name == task.assigned_to), None)
                    if assigned_dwarf and assigned_dwarf.sprite:
                        assigned_dwarf.sprite.assign_task(task, world_objects, pozo)
                        if assigned_dwarf.sprite.target_obj and isinstance(assigned_dwarf.sprite.target_obj, tuple):
                            print("Advertencia: No se encontró objetivo para la tarea.")
                

            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.x -= speed
    if keys[pygame.K_d]:
        player.x += speed
    if keys[pygame.K_w]:
        player.y -= speed
    if keys[pygame.K_s]:
        player.y += speed
    if keys[pygame.K_l]:
        colony_dwarves.list_dwarves()
        pygame.time.delay(150)
    if keys[pygame.K_i]:
        print_colony_inventory(colony, world_objects)  
        pygame.time.delay(150) 
    if keys[pygame.K_r]:
        print("Activando Menu")
        menu_visible = not menu_visible
        pygame.time.delay(150)  
# En el bucle principal, dentro de la sección de keys = pygame.key.get_pressed(), agrega esto:
    if keys[pygame.K_t]:
        print("🚀 INICIANDO PRUEBA DE ESTRÉS: 50 TAREAS SIMULADAS DESDE MENÚ!")
        actions = ["Talar arbol", "Minar minerales", "Atacar dragon", "Obtener agua", "Cazar animal",
                "Comer", "Beber", "Dormir", "Construir", "Socializar", "Atacar minotauro", "Random event"]
        
        for _ in range(50):
            selected_action = random.choice(actions)
            print(f"Simulando selección: {selected_action}")
            
            if selected_action == "Talar arbol":
                task = Task(TaskType.CHOP_TREE, TaskPriority.HIGH)
            elif selected_action == "Minar minerales":
                task = Task(TaskType.MINE_ORE, TaskPriority.HIGH)
            elif selected_action == "Atacar dragon":
                task = Task(TaskType.ATTACK_DRAGON, TaskPriority.CRITICAL)
            elif selected_action == "Obtener agua":
                task = Task(TaskType.COLLECT_WATER, TaskPriority.NORMAL)
            elif selected_action == "Cazar animal":
                task = Task(TaskType.HUNT_ANIMAL, TaskPriority.URGENT)
            elif selected_action == "Comer":
                task = Task(TaskType.EAT, TaskPriority.URGENT)
            elif selected_action == "Beber":
                task = Task(TaskType.DRINK, TaskPriority.URGENT)
            elif selected_action == "Dormir":
                task = Task(TaskType.SLEEP, TaskPriority.HIGH)
            elif selected_action == "Construir":
                task = Task(TaskType.BUILD, TaskPriority.NORMAL)
            elif selected_action == "Socializar":
                task = Task(TaskType.SOCIALIZE, TaskPriority.LOW)
            elif selected_action == "Atacar minotauro":
                task = Task(TaskType.ATTACK_MINOTAUR, TaskPriority.CRITICAL)
            
            if selected_action != "Random event":
                colony.decision_maker.job_manager.add_task(task)
                colony.decision_maker.job_manager.assign_best_dwarf(task, colony_dwarves.dwarves)
                assigned_dwarf = next((d for d in colony_dwarves.dwarves if d.name == task.assigned_to), None)
                if assigned_dwarf and assigned_dwarf.sprite:
                    assigned_dwarf.sprite.assign_task(task, world_objects, pozo)
                    if assigned_dwarf.sprite.target_obj and isinstance(assigned_dwarf.sprite.target_obj, tuple):
                        print("Advertencia: No se encontró objetivo para la tarea en stress test.")

        colony.decision_maker.job_manager.process_buffer()

        pygame.time.delay(300)
    
    event_timer += 1
    if event_timer > event_cooldown:
        town_offset_y = 150
        town_center = (forest_center[0], forest_center[1] + town_offset_y)
        generate_random_event(colony, town_center, invaders, colony_dwarves)
        event_timer = 0

    player.x = max(0, min(player.x, WORLD_W - player.width))
    player.y = max(0, min(player.y, bioma_h - player.height))
    
    camera_x = player.centerx - WIDTH // 2
    camera_y = player.centery - HEIGHT // 2

    camera_x = max(0, min(camera_x, WORLD_W - WIDTH))
    camera_y = max(0, min(camera_y, WORLD_H - HEIGHT))

    draw_world(window, camera_x, camera_y)
    pozo.draw(window, camera_x, camera_y)
    
    for obj in world_objects:
        if hasattr(obj, 'update'):
            obj.update()
        obj.draw(window, camera_x, camera_y)
    
    for dwarf in dwarves:
        dwarf.update(invaders)
        window.blit(dwarf.image, (dwarf.rect.x - camera_x, dwarf.rect.y - camera_y))
        colony.decision_maker.job_manager.process_buffer()


    for inv in invaders[:]:  
        inv.update(dwarves, invaders, colony)
    
    for inv in invaders:
        inv.draw(window, camera_x, camera_y)
        

    window.blit(PUNTERO, (player.x - camera_x, player.y - camera_y))
    town_offset_y = 150
    town_center = (forest_center[0], forest_center[1] + town_offset_y)
    puntero_pos = (player.centerx, player.centery)
    dist = ((puntero_pos[0] - town_center[0])**2 + (puntero_pos[1] - town_center[1])**2)**0.5

    if dist < 100:
        window.blit(town_text, (town_center[0] - camera_x - 100, town_center[1] - camera_y - 200))

    if menu_visible:
            menu_surface = pygame.Surface((menu_w, menu_h), pygame.SRCALPHA)
            pygame.draw.rect(menu_surface, MENU_COLOR, menu_surface.get_rect(), border_radius=5)
            window.blit(menu_surface, (menu_x_pos, menu_y_pos))
            actions = ["Talar arbol", "Minar minerales", "Atacar dragon", "Obtener agua", "Cazar animal",
                        "Comer", "Beber", "Dormir", "Construir", "Socializar", "Atacar minotauro", "Random event"] 
            text_start_x = 15 
            text_start_y = 15
            line_spacing = 30
            TEXT_COLOR = (255, 255, 255) 

            for i, action in enumerate(actions):
                text_surface = menu_font.render(action, True, TEXT_COLOR)
                text_pos_x = menu_x_pos + text_start_x
                text_pos_y = menu_y_pos + text_start_y + i * line_spacing
                
                window.blit(text_surface, (text_pos_x, text_pos_y))

    if pozo.is_near((player.centerx, player.centery)):
        text_surface = font.render(pozo.interaction_text, True, (255, 255, 255))
        window.blit(text_surface, (pozo.rect.x - camera_x, pozo.rect.y - camera_y - 50))
        
    pygame.display.flip()
    clock.tick(60)
    

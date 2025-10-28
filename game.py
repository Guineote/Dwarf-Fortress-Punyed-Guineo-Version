from Classes.GameObjects import *
from Classes.colony_with_ai import *
from Classes.enums import Biome
from Classes.tasksystem import Task, TaskType, TaskPriority
from Classes.colony_dwarves import ColonyDwarves
import pygame 
import sys
import random

pygame.init()
colony = Colony(biome=Biome.FOREST)
colony_dwarves = ColonyDwarves(colony)
# Mostrar lista inicial en consola
colony_dwarves.list_dwarves()

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

menu_h = 200
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

def generate_world_objects():
    objects = []
    GROUND_Y = 750 
    important_rects = [
    townhall.get_rect(center=(forest_center[0], forest_center[1] + 150)),
    pozo.rect
]
    
    for bioma, (start_x, end_x) in BIOMAS.items():
        if bioma == "Forest":
            for _ in range(random.randint(3, 6)):
                x = random.randint(start_x + 50, end_x - 50)
                tree = ForestTree((x, GROUND_Y))
                tree.rect.bottom = GROUND_Y  
                if not any(tree.rect.colliderect(r) for r in important_rects):
                        objects.append(tree)
                        break

        elif bioma == "Desert":
            for _ in range(random.randint(3, 7)):
                x = random.randint(start_x + 50, end_x - 50)
                rock = DesertRock((x, GROUND_Y))
                rock.rect.bottom = GROUND_Y
                objects.append(rock)

        elif bioma == "Mountain":
            for _ in range(random.randint(4, 8)):
                x = random.randint(start_x + 50, end_x - 50)
                rock = Rock((x, GROUND_Y))
                rock.rect.bottom = GROUND_Y
                objects.append(rock)

        elif bioma == "Grassland":
            for _ in range(random.randint(2, 4)):
                x = random.randint(start_x + 50, end_x - 50)
                tree = Tree((x, GROUND_Y))
                tree.rect.bottom = GROUND_Y
                objects.append(tree)

        elif bioma == "Swamp":
            for _ in range(random.randint(3, 6)):
                x = random.randint(start_x + 50, end_x - 50)
                swamp_tree = SwampTree((x, GROUND_Y))
                swamp_tree.rect.bottom = GROUND_Y
                objects.append(swamp_tree)

        elif bioma == "Tundra":
            for _ in range(random.randint(3, 6)):
                x = random.randint(start_x + 50, end_x - 50)
                tundra_tree = TundraTree((x, GROUND_Y))
                tundra_tree.rect.bottom = GROUND_Y
                objects.append(tundra_tree)
    
    volcano_start, volcano_end = BIOMAS["Volcano"]
    dragon_x = (volcano_start + volcano_end) // 2
    dragon_y = 400  # Nivel de suelo
    dragon = Dragon(pos=(dragon_x, dragon_y))
    objects.append(dragon)
    mountain_center_x = (BIOMAS["Mountain"][0] + BIOMAS["Mountain"][1]) // 2
    minotaur = Minotaur(pos=(mountain_center_x, 600))
    objects.append(minotaur)

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

#dwarf_img = pygame.image.load("Assets/Img/dwarf_idle.png").convert_alpha()
#dwarf_img = pygame.transform.scale(dwarf_img, (45, 45))
dwarves = []
#for i, dwarf in enumerate(colony.population.iterate()):
#    x = forest_center[0] + i * 60 - 150
#    y = forest_center[1] + 300
#    dwarves.append(Dwarf((x, y)))
dwarves = colony_dwarves.create_visuals((forest_center[0], forest_center[1] + 300))


PUNTERO = pygame.transform.scale(PUNTERO, (player.width, player.height)) 
world_objects = generate_world_objects()

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
                actions = ["Talar arbol", "Minar minerales", "Atacar dragon", "Obtener agua"]
                if option_index < len(actions):
                    selected_action = actions[option_index]
                    print(f"Comando recibido: {selected_action}")

                if selected_action == "Talar arbol":
                    task = Task(TaskType.CHOP_TREE, TaskPriority.HIGH)
                elif selected_action == "Minar minerales":
                    task = Task(TaskType.MINE_ORE, TaskPriority.HIGH)
                elif selected_action == "Atacar dragon":
                    task = Task(TaskType.DEFEND_COLONY, TaskPriority.CRITICAL)
                elif selected_action == "Obtener agua":
                    task = Task(TaskType.COLLECT_WATER, TaskPriority.NORMAL)

            for dwarf in dwarves:
                if not dwarf.is_busy:
                    dwarf.assign_task(task, world_objects, pozo)
                    break

            print("Tareas en buffer:", colony.decision_maker.job_manager.task_buffer)
                

            
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
    if keys[pygame.K_r]:
        print("Activando Menu")
        menu_visible = not menu_visible
        pygame.time.delay(150)  

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
        dwarf.update()
        window.blit(dwarf.image, (dwarf.rect.x - camera_x, dwarf.rect.y - camera_y))
        

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
            actions = ["Talar arbol", "Minar minerales", "Atacar dragon", "Obtener agua"] 
            text_start_x = 10 
            text_start_y = 10
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
    
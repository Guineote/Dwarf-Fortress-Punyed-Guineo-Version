import pygame
import time
import random
from Classes.tasksystem import TaskType

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = [
            pygame.image.load("Assets/Img/pino_growing_0.png").convert_alpha(), 
            pygame.image.load("Assets/Img/pino_growing_1.png").convert_alpha(),  
            pygame.image.load("Assets/Img/pino.png").convert_alpha(),            
        ]
        self.current_frame = 2
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.is_cut = False
        self.last_cut_time = 0
        self.regrow_time = 5
        self.resources_obtained = 0

    def update(self):
        if self.is_cut:
            elapsed = time.time() - self.last_cut_time
            if elapsed > self.regrow_time:
                self.animate_growth()
                self.is_cut = False

    def animate_growth(self):
        for i in range(3):
            self.image = self.frames[i]
            pygame.display.flip()
            pygame.time.delay(150)
        self.current_frame = 2

    def interact(self):
        if not self.is_cut:
            print("Árbol talado 🌲 → +5 madera")
            self.image = self.frames[0]
            self.is_cut = True
            self.last_cut_time = time.time()
            self.resources_obtained += 5

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def show_interaction_text(self, surface, camera_x, camera_y, font):
        text = font.render("Presiona E para talar", True, (255, 255, 255))
        surface.blit(text, (self.rect.centerx - camera_x - text.get_width() // 2,
                            self.rect.top - camera_y - 25))

class TundraTree(Tree):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = [
            pygame.image.load("Assets/Img/Tundra_tree_g_0.png").convert_alpha(),
            pygame.image.load("Assets/Img/tundra_tree_g_1.png").convert_alpha(),
            pygame.image.load("Assets/Img/Tundra_tree.png").convert_alpha(),
        ]
        self.image = self.frames[2]


class ForestTree(Tree):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = [
            pygame.image.load("Assets/Img/tree_g_0.png").convert_alpha(),
            pygame.image.load("Assets/Img/tree_g_1.png").convert_alpha(),
            pygame.image.load("Assets/Img/tree1.png").convert_alpha(),
        ]
        self.image = self.frames[2]


class SwampTree(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/baobab.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/stone.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Bronze(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/bronze.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Iron(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/iron.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Gold(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/gold.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Diamond(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/diamond.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class DesertRock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/rock_large.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Pozo:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.interaction_text = "E"

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def is_near(self, player_pos, distance=100):
        dx = self.rect.centerx - player_pos[0]
        dy = self.rect.centery - player_pos[1]
        return (dx*dx + dy*dy)**0.5 < distance

    def show_interaction_text(self, surface, camera_x, camera_y, font):
        text = font.render(self.interaction_text, True, (255, 255, 255))
        surface.blit(text, (self.rect.centerx - camera_x - text.get_width() // 2,
                            self.rect.top - camera_y - 25))


class Dragon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {
            "idle": [pygame.transform.scale(pygame.image.load(f"Assets/Img/dragon_idle_f{i+1}.png").convert_alpha(), (256, 256)) for i in range(8)],
            "attack": [pygame.transform.scale(pygame.image.load(f"Assets/Img/dragon_attack_f{i+1}.png").convert_alpha(), (256,256)) for i in range(7)],
            "fly": [pygame.transform.scale(pygame.image.load(f"Assets/Img/dragon_fly_f{i+1}.png").convert_alpha(),(256,256)) for i in range(6)],
            "death": [pygame.transform.scale(pygame.image.load(f"Assets/Img/dragon_death_f{i+1}.png").convert_alpha(), (256,256)) for i in range(5)],
        }

        self.state = "idle"
        self.frames = self.animations[self.state]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.last_update = pygame.time.get_ticks()
        self.frame_interval = 100
        self.is_attacked = False

    def change_state(self, new_state):
        if new_state in self.animations and new_state != self.state:
            self.state = new_state
            self.frames = self.animations[self.state]
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.is_attacked:
            self.change_state("attack")
            self.is_attacked = False

        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now

    def interact(self):
        print("🔥 ¡El dragón ha sido atacado!")
        self.is_attacked = True

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


class Minotaur(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {
            "idle": [pygame.transform.scale(pygame.image.load(f"Assets/Img/minotauro_idle_{i+1}.png").convert_alpha(), (128, 128)) for i in range(6)],
            "attack": [pygame.transform.scale(pygame.image.load(f"Assets/Img/minotauro_attack_f{i+1}.png").convert_alpha(), (128, 128)) for i in range(7)],
            "death": [pygame.transform.scale(pygame.image.load(f"Assets/Img/minotauro_death_f{i+1}.png").convert_alpha(), (128,128)) for i in range(7)],
        }
        self.state = "idle"
        self.frames = self.animations[self.state]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.last_update = pygame.time.get_ticks()
        self.frame_interval = 120
        self.is_attacked = False

    def change_state(self, new_state):
        if new_state in self.animations and new_state != self.state:
            self.state = new_state
            self.frames = self.animations[self.state]
            self.current_frame = 0
            self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.is_attacked:
            self.change_state("attack")
            self.is_attacked = False

        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now

    def interact(self):
        print("¡El minotauro ha sido provocado!")
        self.is_attacked = True

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


class Dwarf(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {
            "idle": [pygame.image.load(f"Assets/Img/dwarf_idle_f{i+1}.png").convert_alpha() for i in range(4)],
            "walk": [pygame.image.load(f"Assets/Img/dwarf_walking_f{i+1}.png").convert_alpha() for i in range(6)],
            "attack": [pygame.image.load(f"Assets/Img/dwarf_cutting_f{i+1}.png").convert_alpha() for i in range(6)],
        }
        self.current_anim = "idle"
        self.frame_index = 0
        self.image = self.animations[self.current_anim][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # Movimiento y estados
        self.speed = 2
        self.is_busy = False
        self.task = None
        self.target_pos = None
        self.home_pos = pos
        self.state = "idle"
        self.animation_timer = 0

    def assign_task(self, task, world_objects, pozo):
        """Asignar tarea y calcular destino según objetos en el mapa"""
        self.is_busy = True
        self.task = task

        # Determinar destino según tipo de tarea
        if task.task_type == TaskType.MINE_ORE:
            ores = [obj for obj in world_objects if isinstance(obj, (Rock, DesertRock))]
            self.target_pos = self.find_nearest(ores)
        elif task.task_type == TaskType.CHOP_TREE:
            trees = [obj for obj in world_objects if isinstance(obj, (Tree, ForestTree, SwampTree, TundraTree))]
            self.target_pos = self.find_nearest(trees)
        elif task.task_type == TaskType.COLLECT_WATER:
            self.target_pos = pozo.rect.center
        elif task.task_type == TaskType.DEFEND_COLONY:
            dragons = [obj for obj in world_objects if isinstance(obj, Dragon)]
            self.target_pos = self.find_nearest(dragons)
        
        # Cambiar estado a caminar
        self.state = "walking_to_target"
        self.set_animation("walk")
        print(f"Tarea {task.task_type} asignada a enano. Destino: {self.target_pos}")

    def find_nearest(self, objects):
        """Encuentra el objeto más cercano del tipo deseado"""
        if not objects:
            return self.home_pos
        nearest = min(objects, key=lambda obj: (obj.rect.centerx - self.rect.centerx)**2 + (obj.rect.centery - self.rect.centery)**2)
        return nearest.rect.center

    def set_animation(self, anim):
        self.current_anim = anim
        self.frame_index = 0

    def update(self):
        self.animation_timer += 1
        if self.animation_timer % 15 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])
            self.image = self.animations[self.current_anim][self.frame_index]
        if self.state == "walking_to_target" and self.target_pos:
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            dist = (dx**2 + dy**2)**0.5
            if dist > 5:
                self.rect.centerx += self.speed * dx / dist
                self.rect.centery += self.speed * dy / dist
            else:
                self.state = "performing_task"
                self.perform_task()
        elif self.state == "performing_task":
            now = pygame.time.get_ticks()
            if now - self.task_start_time >= self.task_duration:
                gained = random.randint(5, 20)
                print(f"✅ {self.task.task_type} completada. Recursos obtenidos: {gained}")
                self.target_pos = self.home_pos
                self.state = "returning_home"
                self.set_animation("walk")
                self.task = None

        elif self.state == "returning_home" and self.target_pos:
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            dist = (dx**2 + dy**2)**0.5
            if dist > 5:
                self.rect.centerx += self.speed * dx / dist
                self.rect.centery += self.speed * dy / dist
            else:
                self.state = "idle"
                self.set_animation("idle")
                self.is_busy = False
                print(f"🏠 Enano regresó al centro de acopio")


    def perform_task(self):
        self.set_animation("attack")
        print(f"⚒️ {self.task.task_type} en progreso...")
        self.task_start_time = pygame.time.get_ticks()  # guarda el tiempo de inicio
        self.task_duration = 3000  # milisegundos

    def handle_event(self, event):
        """Manejo de fin de tarea"""
        if event.type == pygame.USEREVENT + id(self):
            pygame.time.set_timer(event.type, 0)
            gained = random.randint(5, 20)
            print(f"✅ {self.task.task_type} completada. Recursos obtenidos: {gained}")
            self.target_pos = self.home_pos
            self.state = "returning_home"
            self.set_animation("walk")
            self.task = None

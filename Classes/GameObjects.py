import pygame
import time
import random
from Classes.tasksystem import TaskType
from Classes.structures import House

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
        self.is_targeted = False
        self.type = "tree"

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
            print("Árbol talado 🌲")
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
        self.is_targeted = False
        self.type = "tree"


class ForestTree(Tree):
    def __init__(self, pos):
        super().__init__(pos)
        self.frames = [
            pygame.image.load("Assets/Img/tree_g_0.png").convert_alpha(),
            pygame.image.load("Assets/Img/tree_g_1.png").convert_alpha(),
            pygame.image.load("Assets/Img/tree1.png").convert_alpha(),
        ]
        self.image = self.frames[2]
        self.is_targeted = False
        self.type = "tree"


class SwampTree(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/baobab.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.is_targeted = False
        self.type = "tree"
        
    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))



class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/stone.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.is_targeted = False
        self.type = "ore"         # Categoría general
        self.material = "stone"  # Mineral específico que se agregará al inventario

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Bronze(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/bronze.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.is_targeted = False
        self.type = "ore"         
        self.material = "bronze"  

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Iron(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/iron.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.is_targeted = False
        self.type = "ore"         # Categoría general
        self.material = "iron"  # Mineral específico que se agregará al inventario

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Gold(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/gold.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.is_targeted = False
        self.type = "ore"        
        self.material = "gold"  

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Diamond(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/diamond.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.is_targeted = False
        self.type = "ore"         # Categoría general
        self.material = "diamond"  # Mineral específico que se agregará al inventario

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class DesertRock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Img/rock_large.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.is_targeted = False
        self.type = "ore"         # Categoría general
        self.material = "stone"  # Mineral específico que se agregará al inventario

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
    
    def interact(self):
        print("💧 Agua recolectada → +10 agua")

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
        self.type = "enemy"

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
        if self.state == "death" and hasattr(self, 'death_start_time'):
            if now - self.death_start_time >= 3000:  # 3 segundos
                self.change_state("idle")
                del self.death_start_time  # Limpia el timer
        
        if now - self.last_update >= self.frame_interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now

    def interact(self):
        print("🔥 ¡El dragón ha sido atacado!")
        self.is_attacked = True

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


class Animal(pygame.sprite.Sprite):
    def __init__(self, pos, animal_type, meat_yield, idle_frames):
        super().__init__()
        self.animations = {
            "idle": [pygame.image.load(f).convert_alpha() for f in idle_frames],
        }
        self.current_anim = "idle"
        self.frame_index = 0
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(center=pos)
        self.type = animal_type
        self.meat_yield = meat_yield
        self.is_targeted = False
        self.alive = True
        self.animation_timer = 0
        self.type = "meat"  # Repetido, pero ok; considera remover uno
        self.death_start_time = None
        self.respawn_delay = 30000  # 30s en ms

    def change_state(self, new_state):
        if new_state in self.animations and new_state != self.current_anim:
            self.current_anim = new_state
            self.frame_index = 0
            self.image = self.animations[self.current_anim][self.frame_index]

    def update(self):
        if self.alive:
            self.animation_timer += 1
            if self.animation_timer % 20 == 0:  # Animación lenta para idle
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])
                self.image = self.animations[self.current_anim][self.frame_index]
        else:
            # Si muerto, check timer para respawn
            if self.death_start_time and pygame.time.get_ticks() - self.death_start_time >= self.respawn_delay:
                self.respawn()

    def draw(self, surface, camera_x, camera_y):
        if self.alive:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def die(self):
        self.change_state("death")  # Usa el nuevo método para cambiar a death anim
        self.alive = False
        self.death_start_time = pygame.time.get_ticks()  # Inicia timer para respawn
        # Opcional: self.image = pygame.Surface((1, 1), pygame.SRCALPHA) si quieres invisible inmediatamente, pero con death anim es mejor mantener visible durante anim

    def respawn(self):
        # Infiera bioma por current x, pero randomiza en mismo bioma range
        if 1600 <= self.rect.x < 2400:  # Grassland (hardcode ranges de BIOMAS)
            start_x, end_x = 1600, 2400
        elif 2400 <= self.rect.x < 3200:  # Forest
            start_x, end_x = 2400, 3200
        elif 800 <= self.rect.x < 1600:  # Swamp
            start_x, end_x = 800, 1600
        elif 4000 <= self.rect.x < 4800:  # Tundra
            start_x, end_x = 4000, 4800
        else:
            return  # No respawn si bioma desconocido
        
        self.rect.x = random.randint(start_x + 100, end_x - 100)  # Nueva pos diferente
        self.rect.y = 730  # Ajusta y si es necesario
        self.alive = True
        self.change_state("idle")  # Reset anim a idle
        self.death_start_time = None
        print(f"🐖 {self.__class__.__name__} respawneado en nueva posición: ({self.rect.x}, {self.rect.y})")

class Pig(Animal):
    def __init__(self, pos):
        idle_frames = [
            "Assets/Img/pig_idle_f1.png",
            "Assets/Img/pig_idle_f2.png",  
            "Assets/Img/pig_idle_f3.png",
            "Assets/Img/pig_idle_f4.png"
        ]
        super().__init__(pos, "pig", random.randint(15, 25), idle_frames)

class Sheep(Animal):
    def __init__(self, pos):
        idle_frames = [
            "Assets/Img/sheep_idle_f1.png",
            "Assets/Img/sheep_idle_f2.png",
            "Assets/Img/sheep_idle_f3.png",
            "Assets/Img/sheep_idle_f4.png"
        ]
        super().__init__(pos, "sheep", random.randint(12, 20), idle_frames)

class Chicken(Animal):
    def __init__(self, pos):
        idle_frames = [
            "Assets/Img/gallina_idle_f1.png",
            "Assets/Img/gallina_idle_f2.png",
            "Assets/Img/gallina_idle_f3.png",
            "Assets/Img/gallina_idle_f4.png"
        ]
        super().__init__(pos, "chicken", random.randint(5, 10), idle_frames)

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
        self.type = "enemy"

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

class Ogre(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {
            "idle": [pygame.transform.scale(pygame.image.load(f"Assets/Img/ogre_idle_f{i+1}.png").convert_alpha(), (128, 128)) for i in range(5)],
            "walk": [pygame.transform.scale(pygame.image.load(f"Assets/Img/ogre_walk_f{i+1}.png").convert_alpha(), (128, 128)) for i in range(7)],
            "attack": [pygame.transform.scale(pygame.image.load(f"Assets/Img/ogre_attack_f{i+1}.png").convert_alpha(), (128, 128)) for i in range(3)],
            "die": [pygame.transform.scale(pygame.image.load(f"Assets/Img/ogre_death_f{i+1}.png").convert_alpha(), (128, 128)) for i in range(4)],
        }
        self.current_anim = "idle"
        self.frame_index = 0
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(center=pos)
        self.type = "invasor"
        self.is_targeted = False
        self.animation_timer = 0
        self.health = 100
        self.strength = 25 if self.__class__.__name__ == "Ogre" else 8 if self.__class__.__name__ == "Ork" else 15  
        self.speed = 1.5 if self.__class__.__name__ == "Ogre" else 3 if self.__class__.__name__ == "Ork" else 2.5
        self.state = "idle"  
        self.target_dwarf = None
        self.death_timer = 0
        self.alive = True

    def update(self, dwarves, invaders, colony):  
            if not self.alive:
                return

            if self.state == "death":
                self.current_anim = "die"
                self.death_timer += 1
                if self.death_timer > 60:  
                    invaders.remove(self)
                else:
                    self.animation_timer += 1
                    if self.animation_timer % 15 == 0:
                        self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])
                        self.image = self.animations[self.current_anim][self.frame_index]
                return

            nearest_dist = float('inf')
            self.target_dwarf = None
            for dwarf in dwarves:
                if hasattr(dwarf, 'is_alive') and dwarf.is_alive: 
                    dist = ((self.rect.centerx - dwarf.rect.centerx)**2 + (self.rect.centery - dwarf.rect.centery)**2)**0.5
                    if dist < nearest_dist:
                        nearest_dist = dist
                        self.target_dwarf = dwarf

            if self.target_dwarf and nearest_dist < 80:  
                self.state = "attack"
                self.current_anim = "attack"
                self.attack_dwarf(self.target_dwarf, colony)
            else:
                self.state = "walk"
                self.current_anim = "walk"
                if self.target_dwarf:
                    dx = self.target_dwarf.rect.centerx - self.rect.centerx
                    dy = self.target_dwarf.rect.centery - self.rect.centery
                    dist = (dx**2 + dy**2)**0.5
                    if dist > 0:
                        self.rect.centerx += self.speed * dx / dist
                        self.rect.centery += self.speed * dy / dist

            self.animation_timer += 1
            if self.animation_timer % 15 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])
                self.image = self.animations[self.current_anim][self.frame_index]

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
    
    def attack_dwarf(self, dwarf, colony):

        dwarf_strength = dwarf.strength if hasattr(dwarf, 'strength') else 10  
        prob_win_inv = 0.5 + (self.strength - dwarf_strength) * 0.02  
        if random.random() < prob_win_inv:
            if hasattr(dwarf, 'health'):
                dwarf.health -= random.randint(20, 40)
                if dwarf.health <= 0:
                    dwarf.is_alive = False
                    print(f"💀 Dwarf {dwarf.name} muerto por {self.__class__.__name__}!")
            res = random.choice(list(colony.resources.keys()))
            loss = random.randint(3, 8)
            colony.resources[res] = max(0, colony.resources.get(res, 0) - loss)
            print(f"🗡️ {self.__class__.__name__} robó {loss} {res}!")
        else:
            self.health -= random.randint(30, 50)
            if self.health <= 0:
                self.state = "death"
                self.death_timer = 0
                self.alive = False
                print(f"✅ {self.__class__.__name__} derrotado por dwarf!")


class Orc(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = {
            "idle": [pygame.transform.scale(pygame.image.load(f"Assets/Img/ork_idle_f{i+1}.png").convert_alpha(), (128, 128)) for i in range(5)],
            "walk": [pygame.transform.scale(pygame.image.load(f"Assets/Img/ork_walk_f{i+1}.png").convert_alpha(), (128, 128)) for i in range(7)],
            "attack": [pygame.transform.scale(pygame.image.load(f"Assets/Img/ork_attack_f{i+1}.png").convert_alpha(), (128, 128)) for i in range(4)],
            "die": [pygame.transform.scale(pygame.image.load(f"Assets/Img/ork_death_f{i+1}.png").convert_alpha(), (128, 128)) for i in range(4)],
        }
        self.current_anim = "idle"
        self.frame_index = 0
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect(center=pos)
        self.type = "invasor"
        self.is_targeted = False
        self.animation_timer = 0
        self.health = 100
        self.strength = 25 if self.__class__.__name__ == "Ogre" else 8 if self.__class__.__name__ == "Ork" else 15  # Varía por tipo
        self.speed = 1.5 if self.__class__.__name__ == "Ogre" else 3 if self.__class__.__name__ == "Ork" else 2.5
        self.state = "idle"  # idle, walk, attack, death
        self.target_dwarf = None
        self.death_timer = 0
        self.alive = True

    def update(self, dwarves, invaders, colony):  # Agrega params: dwarves (lista sprites), invaders (lista), colony
            if not self.alive:
                return

            if self.state == "death":
                self.current_anim = "die"
                self.death_timer += 1
                if self.death_timer > 60:  # ~1 seg a 60fps
                    invaders.remove(self)  # Remueve de lista global
                else:
                    self.animation_timer += 1
                    if self.animation_timer % 15 == 0:
                        self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])
                        self.image = self.animations[self.current_anim][self.frame_index]
                return

            # Encontrar dwarf más cercano
            nearest_dist = float('inf')
            self.target_dwarf = None
            for dwarf in dwarves:
                if hasattr(dwarf, 'is_alive') and dwarf.is_alive:  # Asumir agregado en Dwarf
                    dist = ((self.rect.centerx - dwarf.rect.centerx)**2 + (self.rect.centery - dwarf.rect.centery)**2)**0.5
                    if dist < nearest_dist:
                        nearest_dist = dist
                        self.target_dwarf = dwarf

            if self.target_dwarf and nearest_dist < 80:  # Rango de ataque
                self.state = "attack"
                self.current_anim = "attack"
                self.attack_dwarf(self.target_dwarf, colony)
            else:
                self.state = "walk"
                self.current_anim = "walk"
                if self.target_dwarf:
                    # Mover hacia target
                    dx = self.target_dwarf.rect.centerx - self.rect.centerx
                    dy = self.target_dwarf.rect.centery - self.rect.centery
                    dist = (dx**2 + dy**2)**0.5
                    if dist > 0:
                        self.rect.centerx += self.speed * dx / dist
                        self.rect.centery += self.speed * dy / dist

            # Animación estándar
            self.animation_timer += 1
            if self.animation_timer % 15 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])
                self.image = self.animations[self.current_anim][self.frame_index]

    def attack_dwarf(self, dwarf, colony):
        # Simular combate equilibrado (50% base, ajusta por strength)
        dwarf_strength = dwarf.strength if hasattr(dwarf, 'strength') else 10  # Asumir en Dwarf
        prob_win_inv = 0.5 + (self.strength - dwarf_strength) * 0.02  # Equilibrado
        if random.random() < prob_win_inv:
            # Invader gana: daño a dwarf o robo
            if hasattr(dwarf, 'health'):
                dwarf.health -= random.randint(20, 40)
                if dwarf.health <= 0:
                    dwarf.is_alive = False
                    print(f"💀 Dwarf {dwarf.name} muerto por {self.__class__.__name__}!")
            res = random.choice(list(colony.resources.keys()))
            loss = random.randint(3, 8)
            colony.resources[res] = max(0, colony.resources.get(res, 0) - loss)
            print(f"🗡️ {self.__class__.__name__} robó {loss} {res}!")
        else:
            # Dwarf gana
            self.health -= random.randint(30, 50)
            if self.health <= 0:
                self.state = "death"
                self.death_timer = 0
                self.alive = False
                print(f"✅ {self.__class__.__name__} derrotado por dwarf!")

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Dwarf(pygame.sprite.Sprite):
    def __init__(self, pos, colony, colony_dwarves, name="Unnamed Dwarf", strength=5): 
        super().__init__()
        self.name = name
        self.strength = strength  
        self.animations = {
            "idle": [pygame.image.load(f"Assets/Img/dwarf_idle_f{i+1}.png").convert_alpha() for i in range(4)],
            "walk": [pygame.image.load(f"Assets/Img/dwarf_walking_f{i+1}.png").convert_alpha() for i in range(6)],
            "attack": [pygame.image.load(f"Assets/Img/dwarf_cutting_f{i+1}.png").convert_alpha() for i in range(6)],
        }
        self.current_anim = "idle"
        self.frame_index = 0
        self.image = self.animations[self.current_anim][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.speed = 2
        self.is_busy = False
        self.task = None
        self.target_pos = None
        self.target_obj = None
        self.home_pos = pos
        self.state = "idle"
        self.animation_timer = 0
        self.inventory = {}
        self.colony = colony
        self.colony_dwarves = colony_dwarves 
        self.world_objects = None  
        self.task_start_time = 0  
        self.task_duration = 0

    def assign_task(self, task, world_objects, pozo, invaders=None):
        self.is_busy = True
        dwarf_data = next((d for d in self.colony_dwarves.dwarves if d.name == self.name), None)
        if dwarf_data:
            dwarf_data.is_busy = True  
        self.task = task
        self.target_obj = None
        self.world_objects = world_objects
        
        if task.task_type == TaskType.MINE_ORE:
            ores = [obj for obj in world_objects 
                    if getattr(obj, "type", None) == "ore" and not getattr(obj, "is_targeted", False)]
            self.target_obj = self.find_nearest_obj(ores)
            if self.target_obj and self.target_obj != self.home_pos:
                self.target_obj.is_targeted = True
                self.target_pos = self.target_obj.rect.center
            else:
                self.target_pos = self.home_pos
                print(f"⚠️ No hay minerales disponibles. Enano regresando a casa.")

        elif task.task_type == TaskType.CHOP_TREE:
            trees = [obj for obj in world_objects 
                    if getattr(obj, "type", None) == "tree" and not getattr(obj, "is_targeted", False)]
            print(f"Árboles disponibles: {len(trees)}")  
            self.target_obj = self.find_nearest_obj(trees)
            if self.target_obj and self.target_obj != self.home_pos:
                self.target_obj.is_targeted = True
                self.target_pos = self.target_obj.rect.center
            else:
                self.target_pos = self.home_pos  
                print(f"⚠️ No hay árboles disponibles para talar. Enano regresando a casa.")

        elif task.task_type == TaskType.COLLECT_WATER:
            self.target_obj = pozo
            if self.target_obj:  
                self.target_pos = pozo.rect.center
            else:
                self.target_pos = self.home_pos
                print(f"⚠️ No hay pozo disponible. Enano regresando a casa.")

        elif task.task_type == TaskType.HUNT_ANIMAL:
            animals = [obj for obj in world_objects 
                    if getattr(obj, "type", None) == "meat" and getattr(obj, "alive", False) and not getattr(obj, "is_targeted", False)]  # Agregué check de alive si existe
            self.target_obj = self.find_nearest_obj(animals)
            if self.target_obj and self.target_obj != self.home_pos:
                self.target_obj.is_targeted = True
                self.target_pos = self.target_obj.rect.center
            else:
                self.target_pos = self.home_pos 
                print(f"⚠️ No hay animales disponibles para cazar. Enano regresando a casa.")

        elif task.task_type == TaskType.ATTACK_DRAGON:
            enemies = [obj for obj in world_objects 
                        if getattr(obj, "type", None) == "enemy" and isinstance(obj, Dragon) and not getattr(obj, "is_targeted", False)]
            self.target_obj = self.find_nearest_obj(enemies)
            if self.target_obj and self.target_obj != self.home_pos:
                self.target_obj.is_targeted = True
                self.target_pos = self.target_obj.rect.center
            else:
                self.target_pos = self.home_pos
                print(f"⚠️ No hay dragón disponible para atacar. Enano regresando a casa.")

        elif task.task_type == TaskType.ATTACK_MINOTAUR:
            enemies = [obj for obj in world_objects 
                    if getattr(obj, "type", None) == "enemy" and isinstance(obj, Minotaur) and not getattr(obj, "is_targeted", False)]
            self.target_obj = self.find_nearest_obj(enemies)
            if isinstance(self.target_obj, tuple):
                self.target_pos = self.target_obj
                self.target_obj = None  # Evita atributos en tuple
            elif self.target_obj:
                self.target_pos = self.target_obj.rect.center
                if hasattr(self.target_obj, 'is_targeted'):
                    self.target_obj.is_targeted = True
            else:
                self.target_pos = self.home_pos
                print("⚠️ No se encontró objetivo para la tarea. Regresando a casa.")
                self.state = "returning_home"
                self.set_animation("walk")
                self.task = None
                return
            if self.target_obj and self.target_obj != self.home_pos:
                self.target_obj.is_targeted = True
                self.target_pos = self.target_obj.rect.center
            else:
                self.target_pos = self.home_pos
                print(f"⚠️ No hay minotauro disponible para atacar. Enano regresando a casa.")

        elif task.task_type in (TaskType.EAT, TaskType.DRINK, TaskType.SLEEP): 
            self.target_pos = self.home_pos
            print(f"🛌 {self.name} realizando {task.task_type} en casa.")

        elif task.task_type == TaskType.BUILD:
            aquatic_start, aquatic_end = 3200, 4000
            target_x = random.randint(aquatic_start + 100, aquatic_end - 100)
            target_y = 750 - 50
            self.target_pos = (target_x, target_y)


        elif task.task_type == TaskType.SOCIALIZE:
            self.target_pos = (self.home_pos[0] + random.randint(-50, 50), self.home_pos[1] + random.randint(-50, 50))
            print(f"🗣️ {self.name} socializando cerca de casa.")


        elif self.task.task_type == TaskType.RANDOM_EVENT:
            print(f"🚨 {self.name} asignado a manejar evento random (invasión o desastre).")
            
            if random.random() < 0.5:  
                attacker = random.choice(["orc", "ogre"])
                event = self.colony.event_system.invasion_event(self.colony.defending_race, attacker, self.colony.count_population(), self.colony.military_strength)
                if event["occurred"]:
                    print(f"🚨 Invasión generada: {event['description']}. Afecta colonia con {event['damage']}% daño inicial.")
                    # Spawn invasores (agrega a invaders global; asume import global invaders o self.colony.invaders = [])
                    num_inv = random.randint(3, min(8, self.colony.count_population() // 3 + 1))
                    for _ in range(num_inv):
                        offset_x = random.randint(-100, 100)
                        offset_y = random.randint(-50, 50)
                        spawn_pos = (self.home_pos[0] + offset_x, self.home_pos[1] + offset_y)  # Cerca centro acopio
                        inv_class = Orc if attacker == "orc" else Ogre if attacker == "ogre" else "" 
                        inv = inv_class(spawn_pos)
                        invaders.append(inv)
                    self.colony.apply_invasion_damage(event["damage"], event["casualties"])
                else:
                    print(f"ℹ️ Invasión evitada: {event['description']}.")
            else:  
                event = self.colony.event_system.natural_disaster_event(self.colony.biome, self.colony.count_population(), self.colony.settlement_durability)
                if event["occurred"]:
                    print(f"🌪️ Desastre generado en bioma {event['biome']}: {event['description']}. Afecta colonia con {event['damage']}% daño y {event['casualties']} bajas.")
                    self.colony.apply_disaster_damage(event)  
                else:
                    print(f"☀️ Desastre evitado: {event['description']}.")
        
            self.state = "returning_home" if not invaders else "attacking"  
            self.target_pos = self.home_pos
            self.set_animation("walk")
            self.task.is_completed = True  

        if self.target_pos:
            self.state = "walking_to_target"
            self.set_animation("walk")
            print(f"Tarea {task.task_type} asignada a enano. Destino: {self.target_pos}")
        else:
            print(f"No hay objetivos disponibles para {task.task_type}")
            self.is_busy = False  
            if dwarf_data:
                dwarf_data.is_busy = False

    def find_nearest_obj(self, objects):
        """Encuentra el objeto más cercano del tipo deseado"""
        if not objects:
            return self.home_pos
        nearest = min(objects, key=lambda obj: (obj.rect.centerx - self.rect.centerx)**2 + (obj.rect.centery - self.rect.centery)**2)
        return nearest

    def set_animation(self, anim):
        self.current_anim = anim
        self.frame_index = 0

    def update(self, invaders=None):
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
                if self.target_obj:
                    if isinstance(self.target_obj, Animal) and self.task.task_type == TaskType.HUNT_ANIMAL:
                        meat_amount = self.target_obj.meat_yield
                        self.inventory["meat"] = self.inventory.get("meat", 0) + meat_amount
                        self.target_obj.die() 
                    
                    elif self.task.task_type == TaskType.COLLECT_WATER:
                        self.inventory["water"] = self.inventory.get("water", 0) + 10
                        if self.target_obj:  
                            self.target_obj.interact()  
                        
                    elif self.task.task_type == TaskType.ATTACK_DRAGON:
                        if self.target_obj and hasattr(self.target_obj, 'interact'):
                            self.target_obj.interact()
                            win_prob = self.strength / 20.0
                            if random.random() < win_prob:
                                print(f"🏆 {self.name} ganó contra el dragón!")
                                self.target_obj.change_state("death")
                                self.target_obj.death_start_time = pygame.time.get_ticks()
                                self.inventory["loot"] = self.inventory.get("loot", 0) + random.randint(10, 20)
                            else:
                                print(f"💀 {self.name} perdió contra el dragón!")
                                self.target_obj.change_state("idle")
                    
                    elif self.task.task_type == TaskType.ATTACK_MINOTAUR:
                        if self.target_obj:
                            self.target_obj.interact()
                            win_prob = self.strength / 20.0
                            if random.random() < win_prob:
                                print(f"🏆 {self.name} ganó contra el minotauro!")
                                self.target_obj.change_state("death")
                                self.target_obj.death_start_time = pygame.time.get_ticks()
                                self.inventory["loot"] = self.inventory.get("loot", 0) + random.randint(5, 15)
                            else:
                                print(f"💀 {self.name} perdió contra el minotauro!")
                                self.target_obj.change_state("idle")
                    
                    else:  
                        rtype = getattr(self.target_obj, "material", getattr(self.target_obj, "type", "unknown"))
                        if rtype == "tree":
                            rtype = "wood"
                        amount = random.randint(1, 3)
                        self.inventory[rtype] = self.inventory.get(rtype, 0) + amount

                    if hasattr(self.target_obj, "is_targeted"):
                        self.target_obj.is_targeted = False
                    if hasattr(self.target_obj, "is_cut"):
                        self.target_obj.interact()
                    
                    if self.task and self.task.task_type == TaskType.RANDOM_EVENT:
                        if not invaders:  
                            self.state = "returning_home"
                            self.target_pos = self.home_pos
                            self.set_animation("walk")
                            self.task = None

                else:  
                    if self.task.task_type == TaskType.EAT:
                        if self.colony.resources.get("meat", 0) >= 1:
                            self.colony.resources["meat"] -= 1  
                            print(f"🍲 {self.name} comió. Energía restaurada.")
                            self.inventory["food"] = self.inventory.get("food", 0) - 1
                        else:
                            print(f"⚠️ No hay comida en la colonia.")
                            self.state = "returning_home"  
                            self.target_pos = self.home_pos
                            self.set_animation("walk")
                            self.task = None
                            return  
                    elif self.task.task_type == TaskType.DRINK:
                        print(f"🥤 {self.name} bebió. Hidratación restaurada.")
                        self.inventory["water"] = self.inventory.get("water", 0) - 1
                    elif self.task.task_type == TaskType.SLEEP:
                        print(f"😴 {self.name} durmió. Descanso completo.")
                    elif self.task.task_type == TaskType.BUILD:
                        print(f"🏗️ {self.name} intentando construir casa en bioma acuático.")
                        current_houses = self.colony.buildings.get("House", 0)
                        if current_houses >= 3:
                            print("⚠️ Máximo de 3 casas alcanzado. No se puede construir más.")
                            self.state = "returning_home"
                            self.target_pos = self.home_pos
                            self.set_animation("walk")
                            self.task = None
                            return
                        
                        required = {"wood": 20, "stone": 10, "iron": 5}
                        missing = {}
                        for res, amt in required.items():
                            if self.colony.resources.get(res, 0) < amt:
                                missing[res] = amt - self.colony.resources.get(res, 0)
                        
                        if missing:
                            missing_str = " y ".join([f"{amt} {res}" for res, amt in missing.items()])
                            print(f"⚠️ Falta {missing_str} para construir la casa.")
                            self.state = "returning_home"
                            self.target_pos = self.home_pos
                            self.set_animation("walk")
                            self.task = None
                            return
                        
                        for res, amt in required.items():
                            self.colony.resources[res] -= amt
                        
                        house_id = current_houses + 1
                        house_pos = self.target_pos
                        house = House(house_id, house_pos, self.colony_dwarves)
                        self.world_objects.append(house) 
                        
                        idle_dwarves = self.colony_dwarves.get_idle_dwarves()
                        for _ in range(min(4, len(idle_dwarves))):
                            dwarf = idle_dwarves.pop(0)
                            if house.add_inhabitant(dwarf.name):
                                print(f"🏠 Asignado {dwarf.name} a {house.name}.")
                                dwarf.current_activity = "Living in house"
                        
                        self.colony.buildings["House"] = house_id
                        print("🏠 Casa construida en el bioma acuático.")
                    elif self.task.task_type == TaskType.SOCIALIZE:
                        print(f"🗣️ {self.name} socializó. Moral aumentada.")
                    elif self.task.task_type == TaskType.RANDOM_EVENT:
                        print(f"🎲 {self.name} manejó evento random. Outcome random.")

                self.target_pos = self.home_pos
                self.state = "returning_home"
                self.set_animation("walk")
                self.task = None
                self.target_obj = None

        elif self.state == "returning_home" and self.target_pos:
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            dist = (dx**2 + dy**2)**0.5
            if dist > 5:
                self.rect.centerx += self.speed * dx / dist
                self.rect.centery += self.speed * dy / dist
            else:
                for rtype, amount in self.inventory.items():
                    self.colony.add_resource(rtype, amount)
                self.inventory.clear()
                self.state = "idle"
                self.set_animation("idle")
                self.is_busy = False
                dwarf_data = next((d for d in self.colony_dwarves.dwarves if d.name == self.name), None)
                if dwarf_data:
                    dwarf_data.is_busy = False
                print(f"🏠 {self.name} regresó al centro de acopio")

        nearest_invader = None
        min_dist = float('inf')
        invaders_list = invaders if invaders is not None else []
        for obj in invaders_list: 
            if hasattr(obj, 'type') and obj.type == "invasor" and hasattr(obj, 'alive') and obj.alive:
                dist = ((self.rect.centerx - obj.rect.centerx)**2 + (self.rect.centery - obj.rect.centery)**2)**0.5
                if dist < min_dist:
                    min_dist = dist
                    nearest_invader = obj

        if nearest_invader and min_dist < 80:
            self.target_obj = nearest_invader
            self.state = "attacking" 
            self.set_animation("attack")
            if random.random() < 0.6: 
                nearest_invader.health -= random.randint(25, 45)
                if nearest_invader.health <= 0:
                    nearest_invader.state = "death"
                    nearest_invader.alive = False
                    print(f"🔨 Dwarf {self.name} mató {nearest_invader.__class__.__name__}!")

    def perform_task(self):
        if self.target_obj is None and self.task.task_type not in [TaskType.BUILD, TaskType.EAT, TaskType.DRINK, TaskType.SLEEP, TaskType.SOCIALIZE, TaskType.RANDOM_EVENT]:
            print("⚠️ No hay objetivo válido para la tarea. Regresando a casa.")
            self.state = "returning_home"
            self.target_pos = self.home_pos
            self.set_animation("walk")
            self.task = None
            return

        if self.task.task_type not in [TaskType.EAT, TaskType.DRINK, TaskType.SLEEP]:
            self.set_animation("attack")
        print(f"⚒️ {self.task.task_type} en progreso...")
        self.task_start_time = pygame.time.get_ticks()
        self.task_duration = 3000
    
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
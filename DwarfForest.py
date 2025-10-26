import random
import time
from enum import Enum

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class ListaEnlazada:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def remove_first(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self.size -= 1
        return data
    
    def is_empty(self):
        return self.head is None
    
    def __length__(self):
        return self.size
    
    def iterate(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

class Queue:
    def __init__(self):
        self.list = ListaEnlazada()
    
    def entailr(self, data):
        self.list.append(data)
    
    def desentailr(self):
        return self.list.remove_first()
    
    def is_empty(self):
        return self.list.is_empty()
    
    def len(self):
        return len(self.list)
    
    def iterate(self):
        return self.list.iterate()

class DeQue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def add_first(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
    
    def add_last(self, data):
        new_node = Node(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def remove_first(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return data
    
    def remove_last(self):
        if not self.tail:
            return None
        data = self.tail.data
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.size -= 1
        return data
    
    def is_empty(self):
        return self.head is None
    
    def __len__(self):
        return self.size

class Heap:
    def __init__(self):
        self.elements = []
    
    def _parent(self, i):
        return (i - 1) // 2
    
    def _left_child(self, i):
        return 2 * i + 1
    
    def _right_child(self, i):
        return 2 * i + 2
    
    def _swap(self, i, j):
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]
    
    def _heapify_up(self, i):
        while i > 0:
            parent = self._parent(i)
            if self.elements[i][0] < self.elements[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break
    
    def _heapify_down(self, i):
        while True:
            min = i
            left = self._left_child(i)
            right = self._right_child(i)
            
            if left < len(self.elements) and self.elements[left][0] < self.elements[min][0]:
                min = left
            if right < len(self.elements) and self.elements[right][0] < self.elements[min][0]:
                min = right
            
            if min != i:
                self._swap(i, min)
                i = min
            else:
                break
    
    def insert(self, priority, data):
        self.elements.append((priority, data))
        self._heapify_up(len(self.elements) - 1)
    
    def get_min(self):
        if not self.elements:
            return None
        if len(self.elements) == 1:
            return self.elements.pop()[1]
        
        min = self.elements[0][1]
        self.elements[0] = self.elements.pop()
        self._heapify_down(0)
        return min
    
    def is_empty(self):
        return len(self.elements) == 0
    
    def size(self):
        return len(self.elements)

class PriorityQueue:
    def __init__(self):
        self.heap = Heap()
    
    def entailr(self, priority, data):
        self.heap.insert(priority, data)
    
    def desentailr(self):
        return self.heap.get_min()
    
    def is_empty(self):
        return self.heap.is_empty()
    
    def size(self):
        return self.heap.size()



class ActionType(Enum):
    Colect_Water = "Colect_Water"
    Felling = "Felling"
    Hunt = "Hunt"
    Fish = "Fish"
    Mine = "Mine"
    Construct = "Construct"
    Defend = "Defend"
    Sleep = "Sleep"

class ResourcesType(Enum):
    Water = "Water"
    Wood = "Wood"
    Meat = "Meat"
    Fish = "Fish"
    MINERAL = "mineral"
    Stone = "Stone"

class Occupation(Enum):
    Lumberjack = "Lumberjack"
    Miner = "Miner"
    Hunter = "Hunter"
    Fisherman = "Fisherman"
    Waterman = "Waterman"
    Builder = "Builder"
    Warrior = "Warrior"
    Farmer = "Farmer"

# ============= CLASES DE CharacterS =============

class Character:
    def __init__(self, name, Occupation, level=1):
        self.name = name
        self.Occupation = Occupation
        self.level = level
        self.Busy = False
        self.Energy = 100
        self.Happiness = 80
        self.XP = 0
        
    def calcular_eficiencia(self, Action):
        Compatibility = self.Get_Compatibility(Action)
        modifier_level = 1 + (self.level * 0.15)
        modifier_Energy = self.Energy / 100
        modifier_Happiness = self.Happiness / 100
        
        return Compatibility * modifier_level * modifier_Energy * modifier_Happiness
    
    def Get_Compatibility(self, Action):
        return 0.5
    
    def Start_action(self, Action):
        self.Busy = True
        self.Energy -= 15
        self.XP += 10
        
        if self.XP >= 100 * self.level:
            self.Level_Up()
    
    def Level_Up(self):
        self.level += 1
        self.XP = 0
        self.Happiness += 10
        if self.Happiness > 100:
            self.Happiness = 100
    
    def Sleep(self):
        self.Energy += 30
        if self.Energy > 100:
            self.Energy = 100
        self.Busy = False
    
    def __str__(self):
        return f"{self.name} ({self.Occupation.value} Nv{self.level})"

class Gatherer(Character):
    def __init__(self, name, Occupation, level=1):
        super().__init__(name, Occupation, level)
        self.Colection_speed = 1.2
    
    def Get_Compatibility(self, Action):
        if Action.type in [ActionType.Colect_Water, ActionType.Felling]:
            if self.Occupation == Occupation.Lumberjack and Action.type == ActionType.Felling:
                return 0.95
            elif self.Occupation == Occupation.Waterman and Action.type == ActionType.Colect_Water:
                return 0.95
            return 0.7
        return 0.3

class Water_Gatherer(Gatherer):
    def __init__(self, name, level=1):
        super().__init__(name, Occupation.Waterman, level)
        self.carrying_capacity = 2.0
    
    def Get_Compatibility(self, Action):
        if Action.type == ActionType.Colect_Water:
            return 0.98
        elif Action.type in [ActionType.Fish]:
            return 0.6
        return 0.25

class Wood_Gatherer(Gatherer):
    def __init__(self, name, level=1):
        super().__init__(name, Occupation.Lumberjack, level)
        self.cutting_strength = 1.5
    
    def Get_Compatibility(self, Action):
        if Action.type == ActionType.Felling:
            return 0.98
        elif Action.type == ActionType.Construct:
            return 0.65
        return 0.25

class Hunter(Character):
    def __init__(self, name, Occupation, level=1):
        super().__init__(name, Occupation, level)
        self.precision = 1.3
    
    def Get_Compatibility(self, Action):
        if self.Occupation == Occupation.Hunter and Action.type == ActionType.Hunt:
            return 0.95
        elif self.Occupation == Occupation.Fisherman and Action.type == ActionType.Fish:
            return 0.95
        elif Action.type in [ActionType.Hunt, ActionType.Fish]:
            return 0.6
        elif Action.type == ActionType.Defend:
            return 0.5
        return 0.2

class Hunter_class(Hunter):
    def __init__(self, name, level=1):
        super().__init__(name, Occupation.Hunter, level)
        self.stealth = 1.4
    
    def Get_Compatibility(self, Action):
        if Action.type == ActionType.Hunt:
            return 0.97
        elif Action.type == ActionType.Defend:
            return 0.6
        return 0.25

class Fisherman(Hunter):
    def __init__(self, name, level=1):
        super().__init__(name, Occupation.Fisherman, level)
        self.patience = 1.5
    
    def Get_Compatibility(self, Action):
        if Action.type == ActionType.Fish:
            return 0.97
        elif Action.type == ActionType.Colect_Water:
            return 0.5
        return 0.2

class Miner(Character):
    def __init__(self, name, level=1):
        super().__init__(name, Occupation.Miner, level)
        self.strength = 1.6
        self.endurance = 1.3
    
    def Get_Compatibility(self, Action):
        if Action.type == ActionType.Mine:
            return 0.95
        elif Action.type == ActionType.Construct:
            return 0.6
        elif Action.type == ActionType.Defend:
            return 0.4
        return 0.2

class Builder(Character):
    def __init__(self, name, level=1):
        super().__init__(name, Occupation.Builder, level)
        self.dexterity = 1.5
    
    def Get_Compatibility(self, Action):
        if Action.type == ActionType.Construct:
            return 0.95
        elif Action.type in [ActionType.Felling, ActionType.Mine]:
            return 0.5
        return 0.25

class Warrior(Character):
    def __init__(self, name, level=1):
        super().__init__(name, Occupation.Warrior, level)
        self.combat_strength = 1.8
        self.defense = 1.4
    
    def Get_Compatibility(self, Action):
        if Action.type == ActionType.Defend:
            return 0.98
        elif Action.type == ActionType.Hunt:
            return 0.5
        return 0.3


class Action:
    def __init__(self, type, necessary_resources=None, generated_resources=None, Urgency=5):
        self.type = type
        self.necessary_resources = necessary_resources or {}
        self.generated_resources = generated_resources or {}
        self.Urgency = Urgency
        self.assigned = False
        self.assigned_Dwarf = None
        self.Finished = False
    
    def __str__(self):
        return f"Acción: {self.type.value} (Urgency: {self.Urgency})"
    

class Planner:
    def __init__(self, colony):
        self.colony = colony
        self.buffer_Actione = Queue()
        self.tail_priority = PriorityQueue()
        self.Actions_history = DeQue()
    
    def append_Action_buffer(self, Action):
        self.buffer_Actions.entailr(Action)
    
    def buffer_processor(self):
        while not self.buffer_Actions.is_empty():
            Action = self.buffer_Actions.desentailr()
            priority = self.Priority_calculator(Action)
            self.tail_priority.entailr(priority, Action)
    
    def Priority_calculator(self, Action):
        priority = Action.Urgency

        if Action.type == ActionType.Colect_Water:
            if self.colony.recursos.get(ResourcesType.Water, 0) < 20:
                priority -= 3 
        
        if Action.type == ActionType.Defend:
            priority = 1
        
        if Action.type == ActionType.Felling:
            if self.colony.recursos.get(ResourcesType.Wood, 0) < 15:
                priority -= 2
        
        if Action.type in [ActionType.Hunt, ActionType.Fish]:
            comida_total = (self.colony.recursos.get(ResourcesType.Meat, 0) + 
                           self.colony.recursos.get(ResourcesType.Fish, 0))
            if comida_total < 25:
                priority -= 2.5
        
        if Action.type == ActionType.Mine:
            if self.colony.recursos.get(ResourcesType.MINERAL, 0) < 10:
                priority -= 1
        
        if self.colony.Happiness_general < 50:
            if Action.type == ActionType.Construct:
                priority -= 1
        
        enanos_disponibles = self.contar_enanos_compatibles(Action)
        if enanos_disponibles == 0:
            priority += 5  # Menos prioritario si no hay nadie
        elif enanos_disponibles == 1:
            priority -= 0.5
        
        return priority
    
    def contar_enanos_compatibles(self, Action):
        """Cuenta enanos disponibles y compatibles"""
        contador = 0
        for enano in self.colony.poblacion.iterate():
            if not enano.Busy and enano.Energy > 20:
                if enano.Get_Compatibility(Action) > 0.5:
                    contador += 1
        return contador
    
    def asignar_mejor_enano(self, Action):
        """Encuentra el mejor enano para una acción"""
        mejor_enano = None
        mejor_score = -1
        
        for enano in self.colony.poblacion.iterate():
            if not enano.Busy and enano.Energy > 20:
                eficiencia = enano.calcular_eficiencia(Action)
                
                # Score compuesto
                score = (eficiencia * 0.6 + 
                        (enano.Energy / 100) * 0.2 + 
                        (enano.Happiness / 100) * 0.2)
                
                if score > mejor_score:
                    mejor_score = score
                    mejor_enano = enano
        
        return mejor_enano
    
    def ejecutar_Actiones(self):
        """Ejecuta Actiones desde la tail de priority"""
        Actiones_ejecutadas = 0
        
        while not self.tail_priority.is_empty() and Actiones_ejecutadas < 5:
            Action = self.tail_priority.desentailr()
            
            # Buscar mejor enano
            enano = self.asignar_mejor_enano(Action)
            
            if enano:
                # Verificar recursos necesarios
                puede_ejecutar = True
                for recurso, cantidad in Action.necessary_resources.items():
                    if self.colony.recursos.get(recurso, 0) < cantidad:
                        puede_ejecutar = False
                        break
                
                if puede_ejecutar:
                    # Consumir recursos
                    for recurso, cantidad in Action.necessary_resources.items():
                        self.colony.recursos[recurso] -= cantidad
                    
                    # Ejecutar acción
                    enano.Start_action(Action)
                    Action.assigned = True
                    Action.assigned_Dwarf = enano
                    
                    # Generar recursos
                    eficiencia = enano.calcular_eficiencia(Action)
                    for recurso, cantidad_base in Action.generated_resources.items():
                        cantidad_real = int(cantidad_base * eficiencia)
                        self.colony.recursos[recurso] = self.colony.recursos.get(recurso, 0) + cantidad_real
                    
                    # append al historial
                    self.Actions_history.append_final((enano, Action))
                    if len(self.Actions_history) > 20:
                        self.Actions_history.remover_frente()
                    
                    Actiones_ejecutadas += 1
                    
                    print(f"  ✓ {enano} ejecutó {Action.type.value} (Eficiencia: {eficiencia:.2f})")
                else:
                    # Devolver a la tail con menor priority
                    self.tail_priority.entailr(Action.Urgency + 2, Action)
        
        return Actiones_ejecutadas

# ============= colony =============

class colony:
    """Gestiona la colony completa"""
    def __init__(self):
        self.poblacion = ListaEnlazada()
        self.recursos = {
            ResourcesType.Water: 0,
            ResourcesType.Wood: 0,
            ResourcesType.Meat: 0,
            ResourcesType.Fish: 0,
            ResourcesType.MINERAL: 0,
            ResourcesType.Stone: 0
        }
        self.edificios = {"Almacén General": 1}
        self.tiempo_dias = 0
        self.Happiness_general = 75
        self.Planner = Planner(self)
        self.evento_activo = None
        
        # Inicializar población
        self._crear_poblacion_inicial()
    
    def _crear_poblacion_inicial(self):
        """Crea la población inicial diversa"""
        names = ["Thorin", "Balin", "Dwalin", "Fili", "Kili", "Dori", "Nori", 
                   "Ori", "Oin", "Gloin", "Bifur", "Bofur", "Bombur", "Gimli", "Durin"]
        
        # 2 Watermanes
        self.poblacion.append(Water_Gatherer(names[0]))
        self.poblacion.append(Water_Gatherer(names[1]))
        
        # 2 Lumberjackes
        self.poblacion.append(Wood_Gatherer(names[2]))
        self.poblacion.append(Wood_Gatherer(names[3]))
        
        # 2 Hunteres
        self.poblacion.append(Hunter_class(names[4]))
        self.poblacion.append(Hunter_class(names[5]))
        
        # 2 Fishermanes
        self.poblacion.append(Fisherman(names[6]))
        self.poblacion.append(Fisherman(names[7]))
        
        # 2 Miners
        self.poblacion.append(Miner(names[8]))
        self.poblacion.append(Miner(names[9]))
        
        # 2 Builderes
        self.poblacion.append(Builder(names[10]))
        self.poblacion.append(Builder(names[11]))
        
        # 3 Warriors
        self.poblacion.append(Warrior(names[12]))
        self.poblacion.append(Warrior(names[13]))
        self.poblacion.append(Warrior(names[14]))
    
    def consumir_recursos_diarios(self):
        """Consume recursos por día"""
        poblacion_total = len(self.poblacion)
        
        # Consumo de Water
        consumo_Water = poblacion_total * 2
        self.recursos[ResourcesType.Water] = max(0, self.recursos[ResourcesType.Water] - consumo_Water)
        
        # Consumo de comida
        consumo_comida = poblacion_total * 1.5
        comida_disponible = self.recursos[ResourcesType.Meat] + self.recursos[ResourcesType.Fish]
        
        if comida_disponible >= consumo_comida:
            # Priorizar Fish
            if self.recursos[ResourcesType.Fish] >= consumo_comida:
                self.recursos[ResourcesType.Fish] -= consumo_comida
            else:
                self.recursos[ResourcesType.Fish] = 0
                self.recursos[ResourcesType.Meat] -= (consumo_comida - self.recursos[ResourcesType.Fish])
        else:
            self.Happiness_general -= 5
            self.recursos[ResourcesType.Meat] = 0
            self.recursos[ResourcesType.Fish] = 0
    
    def currentizar_Happiness(self):
        """currentiza la Happiness general"""
        total_Happiness = 0
        contador = 0
        
        for enano in self.poblacion.iterate():
            total_Happiness += enano.Happiness
            contador += 1
            
            # Recuperar Happiness si hay recursos suficientes
            if self.recursos[ResourcesType.Water] > 30 and (self.recursos[ResourcesType.Meat] + self.recursos[ResourcesType.Fish]) > 40:
                enano.Happiness += 2
                if enano.Happiness > 100:
                    enano.Happiness = 100
        
        if contador > 0:
            self.Happiness_general = total_Happiness / contador
    
    def Sleep_enanos(self):
        """Hace Sleep a los enanos cansados"""
        for enano in self.poblacion.iterate():
            if enano.Energy < 40:
                enano.Sleep()
    
    def generar_evento_aleatorio(self):
        """Genera eventos aleatorios"""
        if random.random() < 0.15:  # 15% de probabilidad
            eventos = [
                ("ataque_goblins", 10),
                ("tormenta", 8),
                ("descubrimiento", 5)
            ]
            
            type_evento, _ = random.choice(eventos)
            
            if type_evento == "ataque_goblins":
                print("\n🗡️  ¡ALERTA! ¡Ataque de goblins!")
                self.evento_activo = "ataque"
                # Generar Actiones de defense automáticamente
                for _ in range(3):
                    Action_defense = Action(ActionType.Defend, Urgency=1)
                    self.Planner.append_Action_buffer(Action_defense)
            
            elif type_evento == "tormenta":
                print("\n⛈️  ¡Tormenta! Recursos dañados.")
                self.recursos[ResourcesType.Wood] = max(0, self.recursos[ResourcesType.Wood] - 5)
                self.Happiness_general -= 5
            
            elif type_evento == "descubrimiento":
                print("\n💎 ¡Descubrimiento! Veta mineral encontrada.")
                self.recursos[ResourcesType.MINERAL] += 15
                self.Happiness_general += 5
    
    def avanzar_dia(self):
        """Avanza un día en la simulación"""
        self.tiempo_dias += 1
        self.consumir_recursos_diarios()
        self.currentizar_Happiness()
        self.Sleep_enanos()
        self.generar_evento_aleatorio()
    
    def mostrar_estado(self):
        """Muestra el estado actual de la colony"""
        print("\n" + "="*60)
        print(f"📅 DÍA {self.tiempo_dias} | 😊 Happiness: {self.Happiness_general:.1f}%")
        print("="*60)
        
        print("\n📦 RECURSOS:")
        for recurso, cantidad in self.recursos.items():
            emoji = {"Water": "💧", "madera": "🪵", "Meat": "🥩", 
                    "Fish": "🐟", "mineral": "⚒️", "Stone": "🪨"}
            print(f"  {emoji.get(recurso.value, '📦')} {recurso.value.capitalize()}: {cantidad}")
        
        print("\n👥 POBLACIÓN:")
        Occupations_count = {}
        for enano in self.poblacion.iterar():
            if not enano.Busy:
                estado = "⚪ Disponible"
            else:
                estado = "🔵 Trabajando"
            print(f"  {estado} | {enano} | E:{enano.Energy:.0f} M:{enano.Happiness:.0f}")
            
            Occupations_count[enano.Occupation.value] = Occupations_count.get(enano.Occupation.value, 0) + 1
        
        print("\n📊 DISTRIBUCIÓN POR Occupation:")
        for Occupation, cant in Occupations_count.items():
            print(f"  {Occupation.capitalize()}: {cant}")
        
        print(f"\n🏛️ EDIFICIOS: {len(self.edificios)}")
        for edificio, cant in self.edificios.items():
            print(f"  {edificio}: {cant}")

# ============= SISTEMA DE JUEGO =============

class Juego:
    """Controlador principal del juego"""
    def __init__(self):
        self.colony = colony()
        self.jugando = True
    
    def mostrar_menu(self):
        """Muestra el menú de Actiones"""
        print("\n" + "─"*60)
        print("🎮 MENÚ DE ActionES")
        print("─"*60)
        print("1. Recolectar Water")
        print("2. Felling árboles")
        print("3. Hunt animales")
        print("4. Fish")
        print("5. Mine minerales")
        print("6. Construct edificio")
        print("7. Asignar múltiples Actiones")
        print("8. Procesar y ejecutar Actiones")
        print("9. Avanzar día (automático)")
        print("10. Ver estado detallado")
        print("0. Salir")
        print("─"*60)
    
    def crear_Action_desde_menu(self, opcion):
        """Crea una acción basada en la opción del menú"""
        Actiones_map = {
            1: (ActionType.Colect_Water, {}, {ResourcesType.Water: 15}, 6),
            2: (ActionType.Felling, {}, {ResourcesType.MADERA: 10}, 5),
            3: (ActionType.Hunt, {}, {ResourcesType.Meat: 12}, 6),
            4: (ActionType.Fish, {}, {ResourcesType.Fish: 14}, 5),
            5: (ActionType.Mine, {}, {ResourcesType.MINERAL: 8, ResourcesType.Stone: 5}, 7),
            6: (ActionType.Construct, {ResourcesType.MADERA: 10, ResourcesType.Stone: 5}, {}, 8)
        }
        
        if opcion in Actiones_map:
            type, req, gen, urg = Actiones_map[opcion]
            return Action(type, req, gen, urg)
        return None
    
    def agregar_Actiones_automaticas(self):
        """Agrega Actiones automáticas basadas en necesidades"""
        # Verificar necesidades críticas
        if self.colony.recursos[ResourcesType.Water] < 15:
            Action = Action(ActionType.Colect_Water, {}, {ResourcesType.Water: 15}, 3)
            self.colony.Planner.agregar_Action_buffer(Action)
            print("  ⚠️  Acción automática agregada: Recolectar Water (crítico)")
        
        comida_total = (self.colony.recursos[ResourcesType.Meat] + 
                       self.colony.recursos[ResourcesType.Fish])
        if comida_total < 20:
            Action = Action(ActionType.Fish, {}, {ResourcesType.Fish: 14}, 4)
            self.colony.Planner.agregar_Action_buffer(Action)
            print("  ⚠️  Acción automática agregada: Fish (crítico)")
    
    def ejecutar_turno_completo(self):
        """Ejecuta un turno completo: procesar buffer y ejecutar Actiones"""
        print("\n🔄 PROCESANDO BUFFER DE ActionES...")
        self.colony.Planner.buffer_processor()
        
        print(f"\n⚙️  EJECUTANDO ActionES (Cola: {self.colony.Planner.cola_prioridad.tamano()})...")
        Actiones_ejecutadas = self.colony.Planner.ejecutar_Actiones()
        
        if Actiones_ejecutadas == 0:
            print("  ℹ️  No se ejecutaron Actiones (sin enanos disponibles o recursos insuficientes)")
        else:
            print(f"\n✅ {Actiones_ejecutadas} Actiones ejecutadas con éxito")
        
        # Avanzar día
        self.colony.avanzar_dia()
    
    def modo_automatico(self, dias=5):
        """Ejecuta varios días automáticamente"""
        print(f"\n🤖 MODO AUTOMÁTICO: {dias} días")
        print("="*60)
        
        for dia in range(dias):
            print(f"\n📅 Simulando día {self.colony.tiempo_dias + 1}...")
            
            # Agregar Actiones balanceadas
            self.colony.Planner.agregar_Action_buffer(
                Action(ActionType.Colect_Water, {}, {ResourcesType.Water: 15}, 5))
            self.colony.Planner.agregar_Action_buffer(
                Action(ActionType.Felling, {}, {ResourcesType.MADERA: 10}, 6))
            self.colony.Planner.agregar_Action_buffer(
                Action(ActionType.Fish, {}, {ResourcesType.Fish: 14}, 5))
            self.colony.Planner.agregar_Action_buffer(
                Action(ActionType.Hunt, {}, {ResourcesType.Meat: 12}, 6))
            self.colony.Planner.agregar_Action_buffer(
                Action(ActionType.Mine, {}, {ResourcesType.MINERAL: 8}, 7))
            
            # Agregar Actiones automáticas si hay necesidades críticas
            self.agregar_Actiones_automaticas()
            
            # Ejecutar turno
            self.colony.Planner.buffer_processor()
            Actiones = self.colony.Planner.ejecutar_Actiones()
            print(f"  ✓ {Actiones} Actiones Finisheds")
            
            self.colony.avanzar_dia()
            
            time.sleep(0.5)  # Pausa para legibilidad
        
        print("\n✅ Simulación automática Finished")
        self.colony.mostrar_estado()
    
    def jugar(self):
        """Loop principal del juego"""
        print("\n" + "="*60)
        print("🏔️  BIENVENIDO A LA SIMULACIÓN DE colony DE ENANOS 🏔️")
        print("="*60)
        print("\n🎯 OBJETIVO: Gestiona tu colony agregando Actiones al buffer.")
        print("   El sistema inteligente las priorizará y asignará a los enanos.")
        print("\n📋 INSTRUCCIONES:")
        print("   - Agrega Actiones al buffer (opciones 1-7)")
        print("   - Ejecuta con opción 8 o modo automático (9)")
        print("   - ¡Mantén recursos suficientes y Happiness alta!")
        
        self.colony.mostrar_estado()
        
        while self.jugando:
            try:
                self.mostrar_menu()
                opcion = input("\n👉 Selecciona una opción: ").strip()
                
                if not opcion.isdigit():
                    print("❌ Por favor ingresa un número válido")
                    continue
                
                opcion = int(opcion)
                
                if opcion == 0:
                    print("\n👋 ¡Gracias por jugar! La colony quedará en buenas manos.")
                    self.jugando = False
                
                elif opcion >= 1 and opcion <= 6:
                    Action = self.crear_Action_desde_menu(opcion)
                    if Action:
                        self.colony.Planner.agregar_Action_buffer(Action)
                        print(f"✅ Acción agregada al buffer: {Action.type.value}")
                        print(f"📊 Buffer actual: {self.colony.Planner.buffer_Actions.tamano()} Actiones")
                
                elif opcion == 7:
                    print("\n📝 AGREGAR MÚLTIPLES ActionES")
                    print("Ingresa las Actiones (1-6) separadas por comas")
                    print("Ejemplo: 1,2,3,4")
                    entrada = input("Actiones: ").strip()
                    
                    try:
                        opciones = [int(x.strip()) for x in entrada.split(',')]
                        contador = 0
                        for op in opciones:
                            if 1 <= op <= 6:
                                Action = self.crear_Action_desde_menu(op)
                                if Action:
                                    self.colony.Planner.agregar_Action_buffer(Action)
                                    contador += 1
                        print(f"✅ {contador} Actiones agregadas al buffer")
                        print(f"📊 Buffer actual: {self.colony.Planner.buffer_Actions.tamano()} Actiones")
                    except:
                        print("❌ Formato inválido")
                
                elif opcion == 8:
                    self.ejecutar_turno_completo()
                    self.colony.mostrar_estado()
                
                elif opcion == 9:
                    print("\n¿Cuántos días simular? (1-10)")
                    try:
                        dias = int(input("Días: ").strip())
                        if 1 <= dias <= 10:
                            self.modo_automatico(dias)
                        else:
                            print("❌ Ingresa un número entre 1 y 10")
                    except:
                        print("❌ Número inválido")
                
                elif opcion == 10:
                    self.colony.mostrar_estado()
                    
                    # Mostrar historial reciente
                    print("\n📜 ÚLTIMAS ActionES EJECUTADAS:")
                    if len(self.colony.Planner.Actions_history) > 0:
                        temp_deque = Deque()
                        contador = 0
                        max_mostrar = 5
                        
                        # Extraer elementos
                        elementos = []
                        while not self.colony.Planner.Actions_history.esta_vacia():
                            elem = self.colony.Planner.Actions_history.remover_final()
                            elementos.append(elem)
                        
                        # Mostrar últimos
                        for i, (enano, Action) in enumerate(reversed(elementos[:max_mostrar])):
                            print(f"  {i+1}. {enano} -> {Action.type.value}")
                        
                        # Restaurar
                        for elem in reversed(elementos):
                            self.colony.Planner.Actions_history.agregar_final(elem)
                    else:
                        print("  (No hay historial todavía)")
                    
                    # Estado del buffer y cola
                    print(f"\n📊 ESTADO DEL Planner:")
                    print(f"  Buffer de Actiones: {self.colony.Planner.buffer_Actions.tamano()}")
                    print(f"  Cola de prioridad: {self.colony.Planner.cola_prioridad.tamano()}")
                
                else:
                    print("❌ Opción no válida")
                
                # Verificar condiciones de game over
                if self.colony.Happiness_general < 20:
                    print("\n💀 GAME OVER: La Happiness de la colony es demasiado baja")
                    print("Los enanos han abandonado la colony...")
                    self.jugando = False
                
                poblacion_activa = sum(1 for e in self.colony.poblacion.iterar() if e.Energy > 0)
                if poblacion_activa < 3:
                    print("\n💀 GAME OVER: No hay suficientes enanos activos")
                    self.jugando = False
            
            except KeyboardInterrupt:
                print("\n\n👋 Juego interrumpido. ¡Hasta pronto!")
                self.jugando = False
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Continuando...")

# ============= PUNTO DE ENTRADA =============

if __name__ == "__main__":
    juego = Juego()
    juego.jugar()
# Dwarf Fortress AI Colony Simulator

## Descripción del Proyecto

**Dwarf Fortress AI Colony Simulator** es un juego/simulación inspirado en *Dwarf Fortress*, pero con un enfoque innovador: **no controlas directamente a ningún enano**, sino que gestionas una **colonia entera como una mente colectiva**. El jugador define **objetivos de alto nivel** (recolectar agua, talar madera, cazar, minar, construir estructuras, defenderse, etc.) a través de un **buffer de acciones**, y la colonia —impulsada por inteligencia artificial— decide **cómo, cuándo y quién** ejecuta cada tarea.

La toma de decisiones se basa en un **sistema de priorización avanzado** implementado con una **Heap / Priority Queue**, que evalúa en tiempo real factores como:

- Urgencia de la necesidad (agua, comida, seguridad)
- Disponibilidad de recursos y enanos
- Habilidades individuales (minero, leñador, guerrero, etc.)
- Riesgos y costos asociados
- Estado emocional y físico de los enanos (necesidades, cansancio, moral)

---

## Características Principales

- **Control indirecto**: El jugador no micromaneja. Solo indica *"quiero una muralla"* o *"necesito más comida"*. La IA decide el plan.
- **Colonia autónoma con IA**: Los enanos forman una sociedad emergente que prioriza, delega y adapta tareas.
- **Sistema de tareas dinámico** basado en `PriorityQueue` para máxima eficiencia.
- **Simulación profunda**:
  - Necesidades fisiológicas y emocionales (hambre, sed, sueño, felicidad)
  - Habilidades y profesiones especializadas
  - Ciclo día/noche, clima y biomas
  - Eventos aleatorios (tormentas, ataques, migraciones)
- **Motor gráfico con Pygame** en `game.py` para visualización en 2D.

---

## Estructura del Proyecto
dwarf_fortress/
├── classes/
│   ├── animals/              # Comportamiento y tipos de fauna
│   ├── biome_system/         # Generación de biomas y recursos naturales
│   ├── body_parts/           # Sistema de lesiones y anatomía
│   ├── characters/           # Lógica base de entidades vivas
│   ├── colony_dwarves/       # Enanos de la colonia y sus estados
│   ├── colony_with_ai/       # Núcleo de la IA colectiva
│   ├── data_structures/      # Estructuras personalizadas (colas, grafos, etc.)
│   ├── decisionMaker/        # Algoritmos de toma de decisiones
│   ├── demo_colony_ai/       # Ejemplos y pruebas de IA
│   ├── entity_Creation/      # Fábrica de entidades
│   ├── enums/                # Enumeraciones del juego
│   ├── equiment/             # Herramientas, armas y armaduras
│   ├── GameObjects/          # Objetos interactivos del mundo
│   ├── jobManager/           # Gestión y asignación de trabajos
│   ├── name_generator/       # Nombres épicos para enanos y lugares
│   ├── needsystem/           # Sistema de necesidades (Maslow para enanos)
│   ├── plants/               # Cultivos, árboles y vegetación
│   ├── random_events/        # Eventos emergentes y narrativa
│   ├── stats/                # Estadísticas y progresión
│   ├── structures/           # Edificios y construcciones
│   └── tasksystem/           # Tareas, estados y ejecución
├── game.py                   # Bucle principal y renderizado con Pygame


---

## Cómo Funciona la IA de Priorización

1. El jugador añade una acción al **buffer** (ej: `Construir almacén`).
2. El `decisionMaker` descompone la meta en subtareas (`Minar piedra`, `Transportar madera`, `Construir`).
3. Cada subtarea entra en la **Priority Queue** con un peso calculado según:
   ```python
   prioridad = urgencia * escasez_recursos * riesgo + bonus_habilidad_enano
## Requisitos

Python 3.8+
Pygame

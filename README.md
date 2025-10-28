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
```plaintext
dwarf_fortress/
├── classes/
│   ├── animals/
│   ├── biome_system/
│   ├── body_parts/
│   ├── characters/
│   ├── colony_dwarves/
│   ├── colony_with_ai/
│   ├── data_structures/
│   ├── decisionMaker/
│   ├── demo_colony_ai/
│   ├── entity_Creation/
│   ├── enums/
│   ├── equiment/
│   ├── GameObjects/
│   ├── jobManager/
│   ├── name_generator/
│   ├── needsystem/
│   ├── plants/
│   ├── random_events/
│   ├── stats/
│   ├── structures/
│   └── tasksystem/
├── game.py

```
---


## Requisitos

Python 3.8+
Pygame

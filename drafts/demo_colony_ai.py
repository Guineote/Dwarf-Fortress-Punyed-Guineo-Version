from colony_with_ai import *
if __name__ == "__main__":
    
    colony = Colony(biome=Biome.FOREST)
    
    print("\n COLONY INITIALIZED")
    print(f"Biome: {colony.biome.value.capitalize()}")
    print(f"Population: {colony.count_population()} colonists")
    
    colony.mostrar_estado()
    colony.simular_dias(15)

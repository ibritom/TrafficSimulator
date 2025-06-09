from Simulación import Simulacion

def main():
    sim = Simulacion()

    # Agregar nodos CON coordenadas desde el inicio
    sim.agregar_nodo("Cartago", 100, 100)
    sim.agregar_nodo("San José", 200, 150)
    sim.agregar_nodo("Alajuela", 300, 200)
    sim.agregar_nodo("Puntarenas", 400, 300)

    # Conectar nodos con pesos
    sim.conectar("Cartago", "San José", 10)
    sim.conectar("San José", "Alajuela", 5)
    sim.conectar("Alajuela", "Puntarenas", 20)
    sim.conectar("Cartago", "Puntarenas", 100)

    # Ejecutar Dijkstra desde Cartago
    sim.dijkstra("Cartago")

    # Consultar ruta hacia Puntarenas
    ruta = sim.obtener_ruta("Puntarenas")
    print("Ruta más corta de Cartago a Puntarenas:")
    print(" → ".join(ruta))

    # Mostrar también las coordenadas
    ruta_info = sim.obtener_ruta_con_info("Puntarenas")
    for nombre, (x, y) in ruta_info:
        print(f"{nombre} en coordenadas ({x}, {y})")

if __name__ == "__main__":
    main()

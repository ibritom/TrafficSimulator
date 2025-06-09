from ListaAdyacentes import ListaAdyacencia

class Nodo:
    def __init__(self, nombre, x=0, y=0):
        self.nombre = nombre                    # Nombre único del nodo
        self.x = x
        self.y = y
        self.adyacentes = ListaAdyacencia()     # Lista personalizada de conexiones
        self.distancia = 999999                 # Usado para Dijkstra (inicialmente infinito)
        self.predecesor = None                  # Nodo anterior en la ruta más corta
        self.asentado = False                   # Indica si el nodo ya fue procesado
        self.siguiente = None                   # Para formar una lista enlazada de nodos

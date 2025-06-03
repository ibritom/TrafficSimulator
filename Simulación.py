from diccionario import DiccionarioPersonalizado
from Nodo import Nodo

class Simulacion:
    def __init__(self):
        self.nodos = None  # Lista enlazada de nodos (cabeza)

    def agregar_nodo(self, nombre):
        if self.buscar_nodo(nombre):
            return False  # Ya existe
        nuevo = Nodo(nombre)
        nuevo.siguiente = self.nodos
        self.nodos = nuevo
        return True

    def buscar_nodo(self, nombre):
        actual = self.nodos
        while actual:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

    def conectar(self, origen_nombre, destino_nombre, peso):
        origen = self.buscar_nodo(origen_nombre)
        destino = self.buscar_nodo(destino_nombre)
        if origen and destino:
            origen.adyacentes.agregar_conexion(destino, peso)
            destino.adyacentes.agregar_conexion(origen, peso)  # Si es grafo no dirigido
            return True
        return False



    def dijkstra(self, origen_nombre):
        origen = self.buscar_nodo(origen_nombre)
        if not origen:
            print("Nodo origen no encontrado.")
            return

        # Inicializar todas las distancias y predecesores
        actual = self.nodos
        while actual:
            actual.distancia = 999999
            actual.predecesor = None
            actual.asentado = False
            actual = actual.siguiente

        # Establecer la distancia inicial del nodo origen
        origen.distancia = 0

        # Diccionario para manejar nodos no asentados por distancia
        no_asentados = DiccionarioPersonalizado()
        actual = self.nodos
        while actual:
            no_asentados.agregar(actual.nombre, actual.distancia)
            actual = actual.siguiente

        # Mientras haya nodos no asentados
        while no_asentados.tamano > 0:
            nombre_actual = no_asentados.obtener_menor()
            nodo_actual = self.buscar_nodo(nombre_actual)
            no_asentados.eliminar(nombre_actual)
            nodo_actual.asentado = True

            # Recorrer los vecinos
            conexion = nodo_actual.adyacentes.cabeza
            while conexion:
                vecino = conexion.destino
                if not vecino.asentado:
                    nueva_distancia = nodo_actual.distancia + conexion.peso
                    if nueva_distancia < vecino.distancia:
                        vecino.distancia = nueva_distancia
                        vecino.predecesor = nodo_actual
                        no_asentados.actualizar(vecino.nombre, nueva_distancia)
                conexion = conexion.siguiente

    def obtener_ruta(self, destino_nombre):
        destino = self.buscar_nodo(destino_nombre)
        if not destino:
            print("Nodo destino no encontrado.")
            return []

        ruta = []
        actual = destino
        while actual:
            ruta.insert(0, actual.nombre)  # Inserta al inicio para construir la ruta
            actual = actual.predecesor

        # Verifica que la ruta realmente se haya formado desde un origen
        if len(ruta) == 1 and ruta[0] != destino_nombre:
            print("No hay ruta encontrada.")
            return []

        return ruta


# backend/services/simulacion_facade.py (Patrón Facade)
from traffic_simulator.backend.interfaces.observer_interface import Observable
from traffic_simulator.backend.models.grafo_lista_adyacencia import GrafoListaAdyacencia
from traffic_simulator.backend.models.nodo import Nodo
from traffic_simulator.backend.services.dijkstra_strategy import DijkstraStrategy
import math


class SimulacionFacade(Observable):
    """Patrón Facade - Simplifica la interacción con el sistema de simulación"""

    def __init__(self):
        super().__init__()
        self._grafo = GrafoListaAdyacencia()
        self._algoritmo_ruta = DijkstraStrategy()
        self._contador_nodos = 1

    def crear_nodo(self, nombre, x=0, y=0):
        """Crea un nuevo nodo en el grafo"""
        identificador = f"nodo_{self._contador_nodos}"
        nodo = Nodo(identificador, nombre, (x, y))

        if self._grafo.agregar_nodo(nodo):
            self._contador_nodos += 1
            self.notificar_observadores('nodo_agregado', nodo)
            return nodo
        return None

    def obtener_nodo_por_posicion(self, x: int, y: int, radio_deteccion: int = 25) -> Nodo:
        """Encuentra el nodo más cercano a una posición"""
        for nodo in self._grafo.obtener_todos_los_nodos():
            distancia = math.sqrt((nodo.x - x) ** 2 + (nodo.y - y) ** 2)
            if distancia <= radio_deteccion:
                return nodo
        return None

    def conectar_nodos(self, origen_id, destino_id, peso=None):
        """Conecta dos nodos con una arista"""
        if peso is None:
            # Calcular peso basado en distancia euclidiana
            origen = self._grafo.obtener_nodo(origen_id)
            destino = self._grafo.obtener_nodo(destino_id)

            if origen and destino:
                dx = origen.x - destino.x
                dy = origen.y - destino.y
                peso = int(math.sqrt(dx * dx + dy * dy) / 10)

        if self._grafo.agregar_arista(origen_id, destino_id, peso):
            self.notificar_observadores('conexion_agregada', {
                'origen': origen_id,
                'destino': destino_id,
                'peso': peso
            })
            return True
        return False

    def calcular_rutas_optimas(self, origen_id):
        """Calcula todas las rutas óptimas desde un nodo origen"""
        self._algoritmo_ruta.calcular_todas_las_rutas(self._grafo, origen_id)
        self.notificar_observadores('rutas_calculadas', origen_id)

    def obtener_ruta_entre_nodos(self, origen_id, destino_id):
        """Obtiene la ruta óptima entre dos nodos específicos"""
        return self._algoritmo_ruta.calcular_ruta_optima(self._grafo, origen_id, destino_id)

    def bloquear_ruta(self, origen_id, destino_id):
        """Bloquea una ruta específica (simula accidente)"""
        arista = self._grafo.obtener_arista(origen_id, destino_id)
        if arista:
            arista.bloquear()
            # También bloquear la arista inversa
            arista_inversa = self._grafo.obtener_arista(destino_id, origen_id)
            if arista_inversa:
                arista_inversa.bloquear()

            self.notificar_observadores('ruta_bloqueada', {
                'origen': origen_id,
                'destino': destino_id
            })
            return True
        return False

    def desbloquear_ruta(self, origen_id, destino_id):
        """Desbloquea una ruta específica"""
        arista = self._grafo.obtener_arista(origen_id, destino_id)
        if arista:
            arista.desbloquear()
            arista_inversa = self._grafo.obtener_arista(destino_id, origen_id)
            if arista_inversa:
                arista_inversa.desbloquear()

            self.notificar_observadores('ruta_desbloqueada', {
                'origen': origen_id,
                'destino': destino_id
            })
            return True
        return False

    def obtener_todos_los_nodos(self):
        """Obtiene todos los nodos del grafo"""
        return self._grafo.obtener_todos_los_nodos()

    def obtener_nodo_por_posicion(self, x, y, radio_deteccion=25):
        """Encuentra el nodo más cercano a una posición"""
        for nodo in self._grafo.obtener_todos_los_nodos():
            distancia = math.sqrt((nodo.x - x) ** 2 + (nodo.y - y) ** 2)
            if distancia <= radio_deteccion:
                return nodo
        return None

    def reiniciar_simulacion(self):
        """Reinicia la simulación completa"""
        for nodo in self._grafo.obtener_todos_los_nodos():
            nodo.limpiar_metadatos()

        self.notificar_observadores('simulacion_reiniciada', None)


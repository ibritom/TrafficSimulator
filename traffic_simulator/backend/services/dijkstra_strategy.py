# backend/services/dijkstra_strategy.py (Patrón Strategy)
from traffic_simulator.backend.interfaces.algoritmo_interface import AlgoritmoRutaInterface
from traffic_simulator.backend.models.diccionario import DiccionarioPersonalizado


class DijkstraStrategy(AlgoritmoRutaInterface):
    """Implementación del algoritmo Dijkstra - Patrón Strategy"""

    def calcular_ruta_optima(self, grafo, origen_id, destino_id):
        """Calcula la ruta óptima entre dos nodos específicos"""
        self.calcular_todas_las_rutas(grafo, origen_id)

        destino = grafo.obtener_nodo(destino_id)
        if not destino:
            return []

        return self._reconstruir_ruta(destino)

    def calcular_todas_las_rutas(self, grafo, origen_id):
        """Implementación completa del algoritmo Dijkstra"""
        # Limpiar metadatos previos
        for nodo in grafo.obtener_todos_los_nodos():
            nodo.limpiar_metadatos()
            nodo.establecer_metadato('distancia', float('inf'))
            nodo.establecer_metadato('predecesor', None)
            nodo.establecer_metadato('visitado', False)

        origen = grafo.obtener_nodo(origen_id)
        if not origen:
            return

        origen.establecer_metadato('distancia', 0)

        # Cola de prioridad usando diccionario personalizado
        no_visitados = DiccionarioPersonalizado()
        for nodo in grafo.obtener_todos_los_nodos():
            no_visitados.agregar(nodo.identificador, nodo.obtener_metadato('distancia'))

        while no_visitados.tamano > 0:
            # Obtener nodo con menor distancia
            nodo_actual_id = no_visitados.obtener_menor()
            nodo_actual = grafo.obtener_nodo(nodo_actual_id)
            no_visitados.eliminar(nodo_actual_id)

            if nodo_actual.obtener_metadato('distancia') == float('inf'):
                break

            nodo_actual.establecer_metadato('visitado', True)

            # Examinar vecinos
            vecinos = grafo.obtener_vecinos(nodo_actual_id)
            for vecino, arista in vecinos:
                if not vecino.obtener_metadato('visitado'):
                    peso = arista.peso
                    print(f"[Dijkstra] Evaluando {nodo_actual.nombre} → {vecino.nombre}, peso = {arista.peso}")

                    nueva_distancia = nodo_actual.obtener_metadato('distancia') + peso

                    if nueva_distancia < vecino.obtener_metadato('distancia'):
                        vecino.establecer_metadato('distancia', nueva_distancia)
                        vecino.establecer_metadato('predecesor', nodo_actual)
                        no_visitados.actualizar(vecino.identificador, nueva_distancia)

    def _reconstruir_ruta(self, destino):
        """Reconstruye la ruta desde el destino hasta el origen"""
        ruta = []
        actual = destino

        while actual:
            ruta.insert(0, actual)
            actual = actual.obtener_metadato('predecesor')

        return ruta if len(ruta) > 1 else []

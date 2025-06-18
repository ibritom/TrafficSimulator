
from traffic_simulator.backend.interfaces.grafo_interface import GrafoInterface
from traffic_simulator.backend.models.diccionario import DiccionarioPersonalizado


class GrafoListaAdyacencia(GrafoInterface):
    """Implementación concreta de grafo usando lista de adyacencia - Principio OCP"""

    def __init__(self):
        self._nodos = DiccionarioPersonalizado()  # identificador -> Nodo
        self._adyacencias = DiccionarioPersonalizado()  # identificador -> Lista de Aristas

    def agregar_nodo(self, nodo):
        """Agrega un nodo al grafo"""
        if not self._nodos.contiene(nodo.identificador):
            self._nodos.agregar(nodo.identificador, nodo)
            # Inicializar lista de adyacencia vacía usando estructura personalizada
            from .lista_enlazada import ListaEnlazada
            self._adyacencias.agregar(nodo.identificador, ListaEnlazada())
            return True
        return False

    def agregar_arista(self, origen_id, destino_id, peso):
        """Agrega una arista entre dos nodos"""
        if not (self._nodos.contiene(origen_id) and self._nodos.contiene(destino_id)):
            return False

        origen = self._nodos.obtener(origen_id)
        destino = self._nodos.obtener(destino_id)

        from .arista import Arista
        arista = Arista(origen, destino, peso)

        # Agregar arista en ambas direcciones (grafo no dirigido)
        lista_origen = self._adyacencias.obtener(origen_id)
        lista_destino = self._adyacencias.obtener(destino_id)

        lista_origen.agregar(arista)

        # Crear arista inversa para grafo no dirigido
        arista_inversa = Arista(destino, origen, peso)
        lista_destino.agregar(arista_inversa)

        return True

    def obtener_nodo(self, identificador):
        """Obtiene un nodo por su identificador"""
        try:
            return self._nodos.obtener(identificador)
        except:
            return None

    def obtener_vecinos(self, nodo_id):
        if not self._adyacencias.contiene(nodo_id):
            return []

        lista_aristas = self._adyacencias.obtener(nodo_id)
        vecinos = []

        actual = lista_aristas.cabeza
        while actual:
            arista = actual.datos
            if arista and arista.activa and not arista.bloqueada and arista.peso != float('inf'):
                vecinos.append((arista.destino, arista))
            actual = actual.siguiente

        return vecinos

    def obtener_todos_los_nodos(self):
        """Obtiene todos los nodos del grafo"""
        nodos = []
        elementos = self._nodos.elementos()
        for identificador, nodo in elementos:
            nodos.append(nodo)
        return nodos

    def obtener_arista(self, origen_id, destino_id):
        """Obtiene la arista entre dos nodos"""
        if not self._adyacencias.contiene(origen_id):
            return None

        lista_aristas = self._adyacencias.obtener(origen_id)
        actual = lista_aristas.cabeza

        while actual:
            if actual.datos.destino.identificador == destino_id:
                return actual.datos
            actual = actual.siguiente

        return None

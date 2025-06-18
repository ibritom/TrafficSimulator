
from abc import ABC, abstractmethod


class GrafoInterface(ABC):
    """Interface para diferentes implementaciones de grafos"""

    @abstractmethod
    def agregar_nodo(self, nodo):
        pass

    @abstractmethod
    def agregar_arista(self, origen, destino, peso):
        pass

    @abstractmethod
    def obtener_nodo(self, identificador):
        pass

    @abstractmethod
    def obtener_vecinos(self, nodo):
        pass

    @abstractmethod
    def obtener_todos_los_nodos(self):
        pass
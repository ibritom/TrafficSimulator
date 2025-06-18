
from abc import ABC, abstractmethod


class AlgoritmoRutaInterface(ABC):
    """Interface para algoritmos de búsqueda de rutas"""

    @abstractmethod
    def calcular_ruta_optima(self, grafo, origen, destino):
        pass

    @abstractmethod
    def calcular_todas_las_rutas(self, grafo, origen):
        pass


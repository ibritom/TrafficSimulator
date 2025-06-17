# backend/interfaces/calculador_peso_interface.py
from abc import ABC, abstractmethod


class CalculadorPesoInterface(ABC):
    """Interface para estrategias de cálculo de peso dinámico"""
    @abstractmethod
    def calcular_peso_base(self,origen,destino):
        pass
    @abstractmethod
    def calcular_peso_dinamico(self, origen, destino, arista=None):
        pass

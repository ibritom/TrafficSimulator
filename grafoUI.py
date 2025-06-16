from abc import ABC, abstractmethod
from figura import *
class elemento_grafico(ABC):
    @abstractmethod
    def rederizar(self):
        raise NotImplementedError
class verticeUI(elemento_grafico):
    def __init__(self):
        circulo = Figura.crear_circulo()

from abc import ABC, abstractmethod


class Observer(ABC):
    """Patrón Observer - Interface para observadores"""

    @abstractmethod
    def actualizar(self, evento, datos):
        pass


class Observable(ABC):
    """Patrón Observer - Interface para sujetos observables"""

    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador: Observer):
        self._observadores.append(observador)

    def remover_observador(self, observador: Observer):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar_observadores(self, evento, datos=None):
        for observador in self._observadores:
            observador.actualizar(evento, datos)

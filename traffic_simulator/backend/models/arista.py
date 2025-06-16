# backend/models/arista.py
class Arista:
    """Representa una arista en el grafo - Principio SRP"""

    def __init__(self, origen, destino, peso=1, bidireccional=True):
        self._origen = origen
        self._destino = destino
        self._peso = peso
        self._bidireccional = bidireccional
        self._activa = True  # Para simular bloqueos de rutas

    @property
    def origen(self):
        return self._origen

    @property
    def destino(self):
        return self._destino

    @property
    def peso(self):
        return self._peso if self._activa else float('inf')

    @property
    def peso_original(self):
        return self._peso

    @property
    def bidireccional(self):
        return self._bidireccional

    @property
    def activa(self):
        return self._activa

    def bloquear(self):
        """Simula un accidente o bloqueo en la ruta"""
        self._activa = False

    def desbloquear(self):
        """Remueve el bloqueo de la ruta"""
        self._activa = True

    def ajustar_peso(self, factor):
        """Ajusta el peso por congestión o condiciones especiales"""
        self._peso = max(1, int(self._peso * factor))

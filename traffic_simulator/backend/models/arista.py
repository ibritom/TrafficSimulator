
class Arista:
    """Representa una arista en el grafo - Principio SRP"""

    def __init__(self, origen, destino, peso=1, bidireccional=True):
        self._origen = origen
        self._destino = destino
        self._peso = peso
        self._bidireccional = bidireccional
        self._activa = True  # Para simular bloqueos de rutas
        # 🔽 Nuevas propiedades para congestión/eventos
        self.vehiculos_actuales = 0
        self.capacidad = 10
        self.accidentes = 0
        self.construcciones = 0
        self.operativos = 0
        self.clima_adverso = False
        self.bloqueada = False
    @property
    def origen(self):
        return self._origen

    @property
    def destino(self):
        return self._destino

    @property
    def peso(self):
        if not self._activa or self.bloqueada:
            return float('inf')
        return self._peso

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
        """Simula un bloqueo total en la arista"""
        self._activa = False
        self.bloqueada = True
        self._peso = float('inf')  # fuerza Dijkstra a ignorarla

    def desbloquear(self):
        """Remueve el bloqueo de la arista"""
        self._activa = True
        self.bloqueada = False


    def ajustar_peso(self, factor):
        """Ajusta el peso por congestión o condiciones especiales"""
        self._peso = max(1, int(self._peso * factor))

    def establecer_peso_dinamico(self, nuevo_peso):
        if nuevo_peso is None:
            return

        if nuevo_peso >= 999999:
            self.bloquear()
        else:
            self._peso = nuevo_peso
            self._activa = True
            self.bloqueada = False

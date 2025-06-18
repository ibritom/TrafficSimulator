
class Nodo:
    """Representa un nodo en el grafo - Principio SRP"""

    def __init__(self, identificador, nombre, coordenadas=(0, 0)):
        self._identificador = identificador
        self._nombre = nombre
        self._x, self._y = coordenadas
        self._metadatos = {}  # Para datos adicionales como distancia Dijkstra

    # Principio de Encapsulación
    @property
    def identificador(self):
        return self._identificador

    @property
    def nombre(self):
        return self._nombre

    @property
    def coordenadas(self):
        return (self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def obtener_metadato(self, clave, valor_defecto=None):
        return self._metadatos.get(clave, valor_defecto)

    def establecer_metadato(self, clave, valor):
        self._metadatos[clave] = valor

    def limpiar_metadatos(self):
        self._metadatos.clear()

    def __eq__(self, other):
        return isinstance(other, Nodo) and self._identificador == other._identificador

    def __hash__(self):
        return hash(self._identificador)

    def __str__(self):
        return f"Nodo({self._identificador}, {self._nombre})"
from conexion import Conexion
class ListaAdyacencia:
    def __init__(self):
        self.cabeza = None

    def agregar_conexion(self, destino, peso):
        nueva = Conexion(destino, peso)
        if not self.cabeza:
            self.cabeza = nueva
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nueva

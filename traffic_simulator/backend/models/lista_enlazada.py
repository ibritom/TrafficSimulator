# backend/models/lista_enlazada.py (Nueva estructura)
class NodoLista:
    def __init__(self, datos):
        self.datos = datos
        self.siguiente = None


class ListaEnlazada:
    """Lista enlazada simple para manejar aristas"""

    def __init__(self):
        self.cabeza = None
        self.tamano = 0

    def agregar(self, datos):
        nuevo = NodoLista(datos)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamano += 1

    def contiene(self, datos):
        actual = self.cabeza
        while actual:
            if actual.datos == datos:
                return True
            actual = actual.siguiente
        return False

    def eliminar(self, datos):
        if not self.cabeza:
            return False

        if self.cabeza.datos == datos:
            self.cabeza = self.cabeza.siguiente
            self.tamano -= 1
            return True

        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.datos == datos:
                actual.siguiente = actual.siguiente.siguiente
                self.tamano -= 1
                return True
            actual = actual.siguiente

        return False


# Nodo para lista doblemente enlazada circular
#Hola
class DiccionarioNodo:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None
        self.anterior = None


# Diccionario personalizado basado en lista doblemente enlazada circular
class DiccionarioPersonalizado:
    def __init__(self):
        self.cabeza = None
        self.tamano = 0
    # Añade clave-valor al final, solo si no existe.
    def agregar(self, clave, valor):
        if self.contiene(clave):
            return

        nuevo = DiccionarioNodo(clave, valor)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cabeza.siguiente = self.cabeza
            self.cabeza.anterior = self.cabeza
        else:
            cola = self.cabeza.anterior
            cola.siguiente = nuevo
            nuevo.anterior = cola
            nuevo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo

        self.tamano += 1
    # Busca si una clave está presente.
    def contiene(self, clave):
        if self.cabeza is None:
            return False

        actual = self.cabeza
        while True:
            if actual.clave == clave:
                return True
            actual = actual.siguiente
            if actual == self.cabeza:
                break

        return False
    # Devuelve el valor asociado a una clave(lanzando error si no existe).
    def obtener(self, clave):
        if self.cabeza is None:
            raise Exception("Clave no encontrada")

        actual = self.cabeza
        while True:
            if actual.clave == clave:
                return actual.valor
            actual = actual.siguiente
            if actual == self.cabeza:
                break

        raise Exception("Clave no encontrada")
    # Elimina un nodo con clave específica.
    def eliminar(self, clave):
        if self.cabeza is None:
            return

        actual = self.cabeza
        while True:
            if actual.clave == clave:
                if actual == self.cabeza and self.tamano == 1:
                    self.cabeza = None
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                    if actual == self.cabeza:
                        self.cabeza = actual.siguiente
                self.tamano -= 1
                return
            actual = actual.siguiente
            if actual == self.cabeza:
                break
    # Devuelve todas las entradas como array de tuplas.
    def elementos(self):
        elementos = []
        actual = self.cabeza

        if actual is not None:
            while True:
                elementos.append((actual.clave, actual.valor))
                actual = actual.siguiente
                if actual == self.cabeza:
                    break

        return elementos
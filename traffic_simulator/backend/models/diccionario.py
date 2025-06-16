# Nodo para lista doblemente enlazada circular
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

    def actualizar(self, clave, nuevo_valor):
        if self.cabeza is None:
            return False

        actual = self.cabeza
        while True:
            if actual.clave == clave:
                actual.valor = nuevo_valor
                return True
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return False

    def imprimir(self):
        actual = self.cabeza
        if actual is None:
            print("Diccionario vacío.")
            return

        while True:
            print(f"{actual.clave}: {actual.valor}")
            actual = actual.siguiente
            if actual == self.cabeza:
                break

    def obtener_menor(self):
        if self.cabeza is None:
            return None

        actual = self.cabeza
        menor = actual
        actual = actual.siguiente

        while actual != self.cabeza:
            if actual.valor < menor.valor:
                menor = actual
            actual = actual.siguiente

        return menor.clave

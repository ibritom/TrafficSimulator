class Simulacion:
    def __init__(self):
        self.nodos = None  # Lista enlazada de nodos (cabeza)

    def agregar_nodo(self, nombre):
        if self.buscar_nodo(nombre):
            return False  # Ya existe
        nuevo = Nodo(nombre)
        nuevo.siguiente = self.nodos
        self.nodos = nuevo
        return True

    def buscar_nodo(self, nombre):
        actual = self.nodos
        while actual:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None

    def conectar(self, origen_nombre, destino_nombre, peso):
        origen = self.buscar_nodo(origen_nombre)
        destino = self.buscar_nodo(destino_nombre)
        if origen and destino:
            origen.adyacentes.agregar_conexion(destino, peso)
            destino.adyacentes.agregar_conexion(origen, peso)  # Si es grafo no dirigido
            return True
        return False

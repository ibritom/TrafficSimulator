import os
import json
from diccionario import DiccionarioPersonalizado

class Grafo:
    def __init__(self, aristas):
        self.aristas = aristas
        #crea el diccionario personalizado
        self.grafo_dicc = DiccionarioPersonalizado()
        
        #procede a rellenar el diccionario con las
        #claves y los valores provenientes de los
        #nodos y sus respectivas aristas del grafo
        for inicio, final in self.aristas:
            if self.grafo_dicc.contiene(inicio):
                valor_actual = self.grafo_dicc.obtener(inicio)
                valor_actual.append(final)
                self.grafo_dicc.eliminar(inicio)
                self.grafo_dicc.agregar(inicio, valor_actual)
            else:
                self.grafo_dicc.agregar(inicio, [final])
                
        #permite visualizar el diccionario
        print(json.dumps(dict(self.grafo_dicc.elementos()), sort_keys=False, indent=4))

    #método que permite generar todas las posibles rutas que se pueden
    #utilizar para ir desde el nodo origen hasta el destino. Las rutas
    #son almacenados en el vector ruta
    def getRuta(self,inicio, final, ruta=[]):
        ruta = ruta + [inicio]
        if inicio == final:
            return [ruta]
        if not self.grafo_dicc.contiene(inicio):
            return []
        camino = []
        for nodo in self.grafo_dicc.obtener(inicio):
            if nodo not in ruta:
                nuevaRuta = self.getRuta(nodo, final, ruta)
                for c in nuevaRuta:
                    camino.append(c)
        return camino

    #método recursivo que recorre las rutas guardadas en el
    #diccionario para cada entrada (llave) y determina cuál
    #es la ruta más corta de acuerdo con el número de nodos que
    #deben ser visitados
    def getRutaCorta(self,inicio,final,ruta=[]):
        ruta = ruta + [inicio]
        if inicio == final:
            return ruta
        if not self.grafo_dicc.contiene(inicio):
            return None
        rutaCorta = None
        for nodo in self.grafo_dicc.obtener(inicio):
            if nodo not in ruta:
                rCorta = self.getRutaCorta(nodo,final,ruta)
                if rCorta:
                    if rutaCorta is None or len(rCorta) < len(rutaCorta):
                        rutaCorta = rCorta
        return rutaCorta

    def mostrarResultado(self):
        print(dict(self.grafo_dicc.elementos()))

def consultar():
    #se crea un vector o lista de elementos donde se
    #especifican el origen y destino de una determinada ruta
    rutas = [
        ("La Cruz", "Upala"),
        ("La Cruz", "Liberia"),
        ("Liberia", "Santa Cruz"),
        ("Liberia", "Puntarenas"),
        ("Upala", "San Carlos"),
        ("Upala", "Alajuela"),
        ("San Carlos", "San José"),
        ("Puntarenas", "Alajuela"),
        ("Santa Cruz", "Nicoya"),
        ("Nicoya", "Hojancha"),
        ("Alajuela", "San José"),
    ]
    os.system("cls")
    _rutas = Grafo(rutas)
    inicio = input("Digite el inicio de la ruta: ")
    destino = input("Digite el destino de la ruta: ")
    print()
    print(f"Las rutas posibles entre {inicio} y {destino} son:\n",_rutas.getRuta(inicio,destino))
    print()
    print(f"La ruta más corta entre {inicio} y {destino} es:",_rutas.getRutaCorta(inicio,destino))
    print()
    os.system("pause")

def validarOpcion():
    correcto = False
    num = 0
    while (not correcto):
        try:
            num = int(input("Seleccione una opción del menú: "))
            correcto = True
        except ValueError:
            print('Error, introduce un valor válido')
    return num

salir = False
while not salir:
    os.system("cls")
    print("**** Operaciones sobre grafos y menos paradas ****")
    print("1. Buscar rutas y ruta más corta")
    print("2. Salir")
    opcion = validarOpcion()
    if opcion == 1:
        consultar()
    elif opcion == 2:
        salir = True
    else:
        print("Introduce una opción entre 1 y 2")

print("Fin del programa")
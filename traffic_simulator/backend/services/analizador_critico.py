
from collections import defaultdict


class AnalizadorCritico:
    def __init__(self, grafo, algoritmo_ruta):
        self._grafo = grafo
        self._algoritmo = algoritmo_ruta

    def calcular_aristas_mas_usadas(self):
        aristas_cuenta = defaultdict(int)

        nodos = self._grafo.obtener_todos_los_nodos()
        for origen in nodos:
            for destino in nodos:
                if origen != destino:
                    ruta = self._algoritmo.calcular_ruta_optima(
                        self._grafo, origen.identificador, destino.identificador
                    )
                    for i in range(len(ruta) - 1):
                        par = tuple(sorted([ruta[i].identificador, ruta[i+1].identificador]))
                        aristas_cuenta[par] += 1

        return sorted(aristas_cuenta.items(), key=lambda x: x[1], reverse=True)


import pygame

from typing import List, Tuple, Dict, Any
from traffic_simulator.frontend.views.base_view import BaseView
from traffic_simulator.backend.utils.constantes import *
from traffic_simulator.backend.models.nodo import Nodo
from traffic_simulator.backend.models.vehiculo import Vehiculo
from traffic_simulator.backend.services.calculador_peso import CalculadorPeso


class GrafoView(BaseView):
    """
    Vista del grafo que implementa el patrón Observer para actualizaciones.

    """

    def __init__(self, controller):
        super().__init__(controller)
        self._config_visual = self._cargar_configuracion_visual()
        self._fuente = pygame.font.Font(None, self._config_visual['tamano_fuente'])
        self._fuente_pequena = pygame.font.Font(None, self._config_visual['tamano_fuente_pequena'])
        self._mostrar_rutas = False
        self._nodo_origen_dijkstra = None
        self._rutas_activas = {}  # {destino_id: (ruta, color)}

    def _cargar_configuracion_visual(self) -> Dict[str, Any]:
        """Carga configuración visual desde constantes"""
        return {
            'tamano_fuente': 24,
            'tamano_fuente_pequena': 18,
            'colores_ruta': [VERDE, AMARILLO, NARANJA, ROJO],
            'radio_nodo': RADIO_NODO,
            'grosor_conexion': GROSOR_CONEXION,
            'grosor_ruta': GROSOR_RUTA
        }

    def actualizar_desde_modelo(self, evento: str, datos: Any) -> None:
        """Implementación del patrón Observer para actualizaciones del modelo"""
        handlers = {
            'rutas_calculadas': self._manejar_rutas_calculadas,
            'simulacion_reiniciada': self._manejar_reinicio,
            'ruta_actualizada': self._manejar_actualizacion_ruta,
            'vehiculo_agregado': self._manejar_nuevo_vehiculo
        }

        if evento in handlers:
            handlers[evento](datos)

    def _manejar_rutas_calculadas(self, origen_id: str) -> None:
        """Actualiza estado cuando se calculan nuevas rutas"""
        self._nodo_origen_dijkstra = self._controller._simulacion._grafo.obtener_nodo(origen_id)
        self._mostrar_rutas = True
        self._actualizar_rutas_visibles()

    def _manejar_reinicio(self, _) -> None:
        """Limpia estado al reiniciar simulación"""
        self._nodo_origen_dijkstra = None
        self._mostrar_rutas = False
        self._rutas_activas.clear()

    def _manejar_actualizacion_ruta(self, datos: Dict) -> None:
        """Actualiza una ruta específica"""
        destino_id = datos['destino']
        if destino_id in self._rutas_activas:
            self._rutas_activas[destino_id] = (datos['ruta'], self._rutas_activas[destino_id][1])

    def _manejar_nuevo_vehiculo(self, vehiculo: Vehiculo) -> None:
        """Prepara visualización para nuevo vehículo"""

        pass

    def _actualizar_rutas_visibles(self) -> None:
        """Actualiza el cache de rutas para visualización"""
        if not self._nodo_origen_dijkstra:
            return

        nodos = self._controller.obtener_estado_actual()['nodos']
        self._rutas_activas.clear()

        for i, nodo in enumerate(nodos):
            if nodo != self._nodo_origen_dijkstra:
                ruta = self._controller._simulacion.obtener_ruta_entre_nodos(
                    self._nodo_origen_dijkstra.identificador,
                    nodo.identificador
                )
                if ruta and len(ruta) > 1:
                    color_idx = i % len(self._config_visual['colores_ruta'])
                    self._rutas_activas[nodo.identificador] = (ruta, self._config_visual['colores_ruta'][color_idx])

    def _obtener_color_nodo(self, nodo: Nodo, nodo_seleccionado: Nodo) -> Tuple[int, int, int]:
        """Determina color del nodo basado en su estado"""
        if nodo == self._nodo_origen_dijkstra:
            return VERDE
        elif nodo == nodo_seleccionado:
            return AMARILLO
        return AZUL

    def renderizar(self, pantalla: pygame.Surface) -> None:
        """Renderiza todos los elementos del grafo"""
        if not self.visible:
            return

        estado = self._controller.obtener_estado_actual()

        # Orden de renderizado importante
        self._renderizar_conexiones(pantalla, estado['nodos'])
        self._renderizar_rutas(pantalla)
        self._renderizar_nodos(pantalla, estado['nodos'], estado.get('nodo_seleccionado'))
        self._renderizar_vehiculos(pantalla, estado['vehiculos'])

    def _renderizar_conexiones(self, pantalla: pygame.Surface, nodos: List[Nodo]) -> None:
        """Renderiza todas las conexiones entre nodos"""
        for nodo in nodos:
            for vecino, arista in self._controller._simulacion._grafo.obtener_vecinos(nodo.identificador):
                if nodo.identificador < vecino.identificador:
                    self.dibujar_conexion(pantalla, nodo, vecino, arista)

    def _renderizar_rutas(self, pantalla: pygame.Surface) -> None:
        """Renderiza las rutas activas"""
        if self._mostrar_rutas and self._nodo_origen_dijkstra:
            for ruta, color in self._rutas_activas.values():
                self.dibujar_ruta(pantalla, ruta, color)

    def _renderizar_nodos(self, pantalla: pygame.Surface, nodos: List[Nodo], nodo_seleccionado: Nodo) -> None:
        """Renderiza todos los nodos del grafo"""
        for nodo in nodos:
            color = self._obtener_color_nodo(nodo, nodo_seleccionado)
            self.dibujar_nodo(pantalla, nodo, color)

    def _renderizar_vehiculos(self, pantalla: pygame.Surface, vehiculos: List[Vehiculo]) -> None:
        """Renderiza todos los vehículos activos"""
        for vehiculo in vehiculos:
            self.dibujar_vehiculo(pantalla, vehiculo)

    # Métodos de dibujo específicos
    def dibujar_nodo(self, pantalla: pygame.Surface, nodo: Nodo, color: Tuple[int, int, int]) -> None:
        """Dibuja un nodo con su información asociada"""
        pygame.draw.circle(pantalla, color, (int(nodo.x), int(nodo.y)), self._config_visual['radio_nodo'])
        pygame.draw.circle(pantalla, NEGRO, (int(nodo.x), int(nodo.y)), self._config_visual['radio_nodo'], 2)

        # Texto del nombre
        texto_nombre = self._fuente_pequena.render(nodo.nombre, True, NEGRO)
        rect_nombre = texto_nombre.get_rect(center=(nodo.x, nodo.y - 35))
        pantalla.blit(texto_nombre, rect_nombre)

        # Texto de distancia (si aplica)
        distancia = nodo.obtener_metadato('distancia')
        if distancia and distancia != float('inf'):
            texto_dist = self._fuente_pequena.render(f"d:{int(distancia)}", True, ROJO)
            rect_dist = texto_dist.get_rect(center=(nodo.x + 25, nodo.y - 25))
            pantalla.blit(texto_dist, rect_dist)

    def dibujar_conexion(self, pantalla: pygame.Surface, origen: Nodo, destino: Nodo, arista):


        """Dibuja una conexión entre nodos con color según congestión/obstáculos"""
        # Obtener la arista real entre los nodos
        arista = self._controller._simulacion._grafo.obtener_arista(origen.identificador, destino.identificador)

        if arista:
            calculador = CalculadorPeso()
            peso_base = calculador.calcular_peso_base(origen, destino)
            peso_actual = calculador.calcular_peso_dinamico(origen, destino, arista)
            color = self._obtener_color_congestion(peso_base, peso_actual)
        else:
            color = GRIS  # En caso de que no se encuentre la arista

        pygame.draw.line(pantalla, color,
                         (origen.x, origen.y),
                         (destino.x, destino.y),
                         self._config_visual['grosor_conexion'])

        # Texto del peso
        texto_peso = self._fuente_pequena.render(str(arista.peso), True, NEGRO)

        rect_peso = texto_peso.get_rect(center=(
            (origen.x + destino.x) / 2,
            (origen.y + destino.y) / 2
        ))

        pygame.draw.rect(pantalla, BLANCO, rect_peso.inflate(8, 4))
        pantalla.blit(texto_peso, rect_peso)

    def dibujar_ruta(self, pantalla: pygame.Surface, ruta: List[Nodo], color: Tuple[int, int, int]) -> None:
        """Dibuja una ruta resaltada"""
        for i in range(len(ruta) - 1):
            pygame.draw.line(pantalla, color,
                             (ruta[i].x, ruta[i].y),
                             (ruta[i + 1].x, ruta[i + 1].y),
                             self._config_visual['grosor_ruta'])

    def dibujar_vehiculo(self, pantalla: pygame.Surface, vehiculo: Vehiculo) -> None:
        """Dibuja un vehículo en su posición actual"""
        if vehiculo.activo:
            pygame.draw.circle(pantalla, vehiculo.color,
                               (int(vehiculo.posicion[0]), int(vehiculo.posicion[1])), 10)

    def _obtener_color_congestion(self, peso_base: float, peso_actual: float) -> Tuple[int, int, int]:
        """Determina color según el nivel de congestión"""
        if peso_actual >= 999999:
            return (GRIS_OSCURO)  # bloqueada = gris oscuro

        ratio = peso_actual / peso_base if peso_base > 0 else 1

        if ratio <= 1.2:
            return (VERDE)  # verde
        elif ratio <= 1.5:
            return (AMARILLO)  # amarillo
        elif ratio <= 2.0:
            return (NARANJA)  # naranja
        elif ratio <= 3.0:
            return (ROJO)  # rojo
        else:
            return (ROJO_OSCURO)  # rojo oscuro



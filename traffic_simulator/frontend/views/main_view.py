# frontend/views/main_view.py
import pygame
from traffic_simulator.frontend.views.base_view import BaseView
from traffic_simulator.frontend.views.grafo_view import GrafoView
from traffic_simulator.frontend.views.panel_control_view import PanelControlView
from traffic_simulator.frontend.views.info_estado_view import InfoEstadoView
from traffic_simulator.backend.utils.constantes import *


class MainView(BaseView):
    """Vista principal que compone otras vistas - Patrón Composite"""

    def __init__(self, controller):
        super().__init__(controller)
        self._grafo_view = GrafoView(controller)
        self._panel_control_view = PanelControlView(controller)
        self._info_estado_view = InfoEstadoView(controller)

    def actualizar_desde_modelo(self, evento, datos):
        """Propaga las actualizaciones a las vistas hijas"""
        self._grafo_view.actualizar_desde_modelo(evento, datos)
        self._panel_control_view.actualizar_desde_modelo(evento, datos)
        self._info_estado_view.actualizar_desde_modelo(evento, datos)

    def renderizar(self, pantalla):
        """Renderiza todas las vistas hijas"""
        # Fondo blanco
        pantalla.fill(BLANCO)

        # Orden de renderizado importante
        self._grafo_view.renderizar(pantalla)
        self._panel_control_view.renderizar(pantalla)
        self._info_estado_view.renderizar(pantalla)
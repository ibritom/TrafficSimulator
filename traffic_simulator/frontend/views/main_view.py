# frontend/views/main_view.py
import pygame
from traffic_simulator.frontend.views.base_view import BaseView
from traffic_simulator.frontend.views.grafo_view import GrafoView
from traffic_simulator.frontend.views.panel_control_view import PanelControlView
from traffic_simulator.frontend.views.info_estado_view import InfoEstadoView
from traffic_simulator.backend.utils.constantes import *
from traffic_simulator.frontend.views.nombre_ciudad_popup import NombreCiudadPopup

class MainView(BaseView):
    """Vista principal que compone otras vistas - Patrón Composite"""

    def __init__(self, controller, pantalla):
        super().__init__(controller)
        self._pantalla = pantalla  # ← Guardamos la surface real
        self._grafo_view = GrafoView(controller)
        self._panel_control_view = PanelControlView(controller)
        self._info_estado_view = InfoEstadoView(controller)
        self._popup = None

    def actualizar_desde_modelo(self, evento, datos):
        """Propaga las actualizaciones a las vistas hijas"""
        self._grafo_view.actualizar_desde_modelo(evento, datos)
        self._panel_control_view.actualizar_desde_modelo(evento, datos)
        self._info_estado_view.actualizar_desde_modelo(evento, datos)

    def renderizar(self, pantalla):
        """Renderiza todas las vistas hijas"""
        # Fondo blanco
        pantalla.fill(BLANCO)
        # Renderizar popup si está activo
        print(f"[Renderizar] popup = {self._popup}, activo = {getattr(self._popup, 'activo', 'Sin atributo')}")




        # Orden de renderizado importante
        self._grafo_view.renderizar(pantalla)
        self._panel_control_view.renderizar(pantalla)
        self._info_estado_view.renderizar(pantalla)
        if self.popup_activo():
            print("[Renderizar] Dibujando el popup")
            self._popup.dibujar()
    def mostrar_popup_nombre_ciudad(self, x, y):
        print(f"[Popup] Creando popup en ({x}, {y})")
        self._popup = NombreCiudadPopup(self._pantalla, self._controller, x, y)
    def popup_activo(self):
        return self._popup is not None and self._popup.activo

    def manejar_evento(self, evento):
        """Procesa eventos para popup si está activo"""
        if self.popup_activo():
            self._popup.manejar_evento(evento)
            return True  # evento consumido
        else:
            # Distribuye evento a las vistas hijas si no hay popup
            self._grafo_view.manejar_evento(evento)
            self._panel_control_view.manejar_evento(evento)
            self._info_estado_view.manejar_evento(evento)
            return False

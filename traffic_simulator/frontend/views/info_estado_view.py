
import pygame
from traffic_simulator.frontend.views.base_view import BaseView
from traffic_simulator.backend.utils.constantes import *


class InfoEstadoView(BaseView):
    """Vista para la información de estado - Principio SRP"""

    def __init__(self, controller):
        super().__init__(controller)
        self._fuente_pequena = pygame.font.Font(None, 18)

    def actualizar_desde_modelo(self, evento, datos):
        """Actualiza la vista basada en eventos del modelo"""
        pass

    def renderizar(self, pantalla):
        """Renderiza la información de estado"""
        estado = self._controller.obtener_estado_actual()
        info_y = ALTO - 260

        # Número de nodos
        nodos_texto = self._fuente_pequena.render(
            f"Nodos: {len(estado['nodos'])}", True, GRIS)
        pantalla.blit(nodos_texto, (10, info_y))

        # Número de vehículos
        vehiculos_texto = self._fuente_pequena.render(
            f"Vehículos: {len(estado['vehiculos'])}", True, GRIS)
        pantalla.blit(vehiculos_texto, (10, info_y + 20))
# frontend/views/info_estado_view.py
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
        pass  # La información de estado no necesita actualizaciones directas del modelo

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

        # Velocidad de simulación
        velocidad_texto = self._fuente_pequena.render(
            f"Velocidad: {self._controller._velocidad_simulacion}x", True, GRIS)
        pantalla.blit(velocidad_texto, (10, info_y + 40))

        # Controles adicionales
        controles_adicionales = [
            "S: Generar vehículos aleatorios",
            "SPACE: Pausar/Reanudar",
            "+/-: Cambiar velocidad",
            "Click Der: Agregar vehículo a destino"
        ]

        for i, control in enumerate(controles_adicionales):
            control_texto = self._fuente_pequena.render(control, True, GRIS)
            pantalla.blit(control_texto, (ANCHO - 300, info_y + i * 18))
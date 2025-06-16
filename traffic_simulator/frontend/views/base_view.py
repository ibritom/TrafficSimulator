# frontend/views/base_view.py
from abc import ABC, abstractmethod
import pygame
from typing import Any, Dict


class BaseView(ABC):
    """
    Clase base abstracta para todas las vistas del sistema.
    Implementa el principio de Abierto/Cerrado (OCP) y el patrón Observer.

    Métodos:
        actualizar_desde_modelo(evento: str, datos: Any) -> None
        renderizar(pantalla: pygame.Surface) -> None
        manejar_evento(evento: pygame.event.Event) -> None
    """

    def __init__(self, controller: Any):
        """
        Constructor base para todas las vistas.

        Args:
            controller: Referencia al controlador MVC que maneja la lógica.
        """
        self._controller = controller
        self._visible = True
        self._rect = pygame.Rect(0, 0, 0, 0)  # Área de la vista

    @abstractmethod
    def actualizar_desde_modelo(self, evento: str, datos: Any) -> None:
        """
        Método abstracto para actualizar la vista cuando el modelo cambia.
        Implementa la parte View del patrón Observer.

        Args:
            evento: Identificador del tipo de cambio (ej: 'nodo_agregado')
            datos: Información asociada al evento (opcional)
        """
        pass

    @abstractmethod
    def renderizar(self, pantalla: pygame.Surface) -> None:
        """
        Método abstracto para renderizar la vista en la pantalla dada.

        Args:
            pantalla: Superficie de PyGame donde se dibujará
        """
        pass

    def manejar_evento(self, evento: pygame.event.Event) -> bool:
        """
        Maneja eventos de UI. Puede ser sobreescrito por vistas hijas.

        Args:
            evento: Evento de PyGame a manejar

        Returns:
            bool: True si el evento fue consumido, False si no
        """
        return False

    @property
    def visible(self) -> bool:
        """Indica si la vista debe renderizarse"""
        return self._visible

    @visible.setter
    def visible(self, valor: bool) -> None:
        self._visible = valor

    @property
    def rect(self) -> pygame.Rect:
        """Área ocupada por la vista (para detección de clicks)"""
        return self._rect

    def obtener_config_estilo(self) -> Dict[str, Any]:
        """
        Devuelve configuración de estilo para la vista.
        Las vistas hijas pueden extender este método.
        """
        return {
            'color_fondo': (255, 255, 255),
            'color_borde': (200, 200, 200),
            'ancho_borde': 0,
            'padding': 10
        }
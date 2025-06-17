# backend/models/vehiculo.py (Jerarquía de herencia)
import math


class Vehiculo:
    """Clase base para vehículos - Principio LSP"""

    def __init__(self, ruta, velocidad=2):
        self._ruta = ruta
        self._velocidad = velocidad
        self._posicion_actual = 0
        self._pos_x, self._pos_y = ruta[0].coordenadas if ruta else (0, 0)
        self._activo = True
        self._color = (255, 0, 0)  # Rojo por defecto
        self._tipo = 'normal'

    @property
    def tipo(self):
        return self._tipo

    @property
    def activo(self):
        return self._activo

    @property
    def ruta(self):
        return self.ruta
    @property
    def posicion(self):
        return (self._pos_x, self._pos_y)

    @property
    def color(self):
        return self._color

    def mover(self):
        """Mueve el vehículo a lo largo de su ruta"""
        if not self._activo or self._posicion_actual + 1 >= len(self._ruta):
            return

        destino = self._ruta[self._posicion_actual + 1]
        dx = destino.x - self._pos_x
        dy = destino.y - self._pos_y
        distancia = math.hypot(dx, dy)

        if distancia < self._velocidad:
            self._pos_x, self._pos_y = destino.x, destino.y
            self._posicion_actual += 1
            if self._posicion_actual + 1 >= len(self._ruta):
                self._activo = False
        else:
            self._pos_x += self._velocidad * dx / distancia
            self._pos_y += self._velocidad * dy / distancia

    def obtener_prioridad(self):
        """Obtiene la prioridad del vehículo para intersecciones"""
        return 1


class VehiculoEmergencia(Vehiculo):
    """Vehículo de emergencia con mayor prioridad"""

    def __init__(self, ruta, velocidad=4):
        super().__init__(ruta, velocidad)
        self._color = (0, 0, 255)  # Azul para emergencia
        self._tipo = 'emergencia'  # En VehiculoEmergencia

    def obtener_prioridad(self):
        return 3  # Mayor prioridad


class VehiculoComercial(Vehiculo):
    """Vehículo comercial más lento"""

    def __init__(self, ruta, velocidad=1.5):
        super().__init__(ruta, velocidad)
        self._tipo = 'comercial'  # En VehiculoComercial

        self._color = (0, 255, 0)  # Verde para comercial

    def obtener_prioridad(self):
        return 0.5  # Menor prioridad


from abc import abstractmethod
from colores import *
import math
import pygame

class Figura:
    def __init__(self, color):
        self.color = color_pygame(color)

    @abstractmethod
    def dibujar(self):
        raise NotImplementedError

    @abstractmethod
    def mover(self):
        raise NotImplementedError

    @abstractmethod
    def posicionar(self, x, y):
        raise NotImplementedError

class Rectangulo(Figura):
    def __init__(self, pantalla, x1, y1, x2, y2, color, tag=""):
        super().__init__(color)
        self._rectangulo = None
        self._pantalla = pantalla
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._tag = tag

    def dibujar(self):
        self._rectangulo = pygame.draw.rect(self._pantalla, self.color, (self._x1, self._y1, self._x2, self._y2))

    def mover(self, x, y):
        self._x1 += x
        self._y1 += y
        self._x2 += x
        self._y2 += y
        self.dibujar()

    def posicionar(self, x, y):
        self._x2 = x + (self._x2 - self._x1)
        self._y2 = y + (self._y2 - self._y1)
        self._x1 = x
        self._y1 = y
        self.dibujar()

class Circulo(Figura):
    def __init__(self, pantalla, x1, y1, x2, y2, color, tag=""):
        super().__init__(color)
        self._circulo = None
        self._pantalla = pantalla
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._actualizar_centro_y_radio()
        self._tag = tag

    def _actualizar_centro_y_radio(self):
        centro_x = (self._x1 + self._x2) / 2
        centro_y = (self._y1 + self._y2) / 2
        self._centro = (centro_x, centro_y)
        self._radio = math.sqrt((centro_x - self._x1) ** 2 + (centro_y - self._y1) ** 2)

    def dibujar(self):
        self._circulo = pygame.draw.circle(self._pantalla, self.color, self._centro, int(self._radio))

    def mover(self, x, y):
        self._x1 += x
        self._y1 += y
        self._x2 += x
        self._y2 += y
        self._actualizar_centro_y_radio()
        self.dibujar()

    def posicionar(self, x, y):
        self._x2 = x + (self._x2 - self._x1)
        self._y2 = y + (self._y2 - self._y1)
        self._x1 = x
        self._y1 = y
        self._actualizar_centro_y_radio()
        self.dibujar()

class Linea(Figura):
    def __init__(self, pantalla, punto_inicio, punto_final, ancho, color, tag=""):
        super().__init__(color)
        self._linea = None
        self._pantalla = pantalla
        self._punto_inicio = punto_inicio
        self._punto_final = punto_final
        self._ancho = ancho
        self._tag = tag

    def dibujar(self):
        self._linea = pygame.draw.line(self._pantalla, self.color, self._punto_inicio, self._punto_final, self._ancho)

    def posicionar(self, x, y):
        dx = self._punto_final[0] - self._punto_inicio[0]
        dy = self._punto_final[1] - self._punto_inicio[1]
        self._punto_inicio = (x, y)
        self._punto_final = (x + dx, y + dy)
        self.dibujar()

    def mover(self, x, y):
        self._punto_inicio = (self._punto_inicio[0] + x, self._punto_inicio[1] + y)
        self._punto_final = (self._punto_final[0] + x, self._punto_final[1] + y)
        self.dibujar()

    def set_punto_inicio(self, punto_inicio):
        self._punto_inicio = punto_inicio
        self.dibujar()

    def set_punto_final(self, punto_final):
        self._punto_final = punto_final
        self.dibujar()



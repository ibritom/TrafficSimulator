from abc import abstractmethod

import pygame
class figura:
    @abstractmethod
    def dibujar(self):
        raise NotImplementedError
    @abstractmethod
    def mover(self):
        raise NotImplementedError
class rectangulo(figura):
    def __init__(self, pantalla, x1, y1, x2, y2, ancho, alto, etiqueta=""):
        self.rectangulo = 0
        self.pantalla = pantalla
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.ancho = ancho
        self.alto = alto
        self.etiqueta = etiqueta
    def dibujar(self):
        return None#implementar


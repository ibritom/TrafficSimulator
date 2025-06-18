import pygame
from pygame.locals import *
from figura import *

class verticeUI():
    def __init__(self, pantalla, color, nombre, x1, x2, y1, y2):
        self.pantalla = pantalla
        self.color = color
        self.nombre = nombre
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    def crearVertice(self, pantalla, color, nombre, x1, x2, y1, y2):
        # crear el circulo
        Figura.crear_circulo(pantalla,x1,x2,y1,y2,color=color)
        print("Ciudad añadida")


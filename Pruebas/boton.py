from abc import abstractmethod
import pygame

class boton:
    def __init__(self, color, posx, posy, alto, ancho, font, texto):
        self.color = (0,0,0)
        self.posx = 0
        self.posy = 0
        self.alto = 100
        self.ancho = 100
        font = pygame.font.SysFont('notosansmono', 35)
        texto = font.render('default', True, color)
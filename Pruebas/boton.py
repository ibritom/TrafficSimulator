from abc import abstractmethod
import pygame
from pygame.locals import *

pygame.init()

resolucion = (1920,1080)
font = pygame.font.Font(pygame.font.get_default_font(), 25)
class boton():
    def __init__(self, colorNormal, colorHover, colorTexto, posx, posy, alto, ancho, texto):
        self.colorNormal = (0,0,0)
        self.colorHover = (0,255,0)
        self.colorTexto = (255,255,255)
        self.posx = 0
        self.posy = 0
        self.alto = 100
        self.ancho = 100
        self.texto = texto
    def renderizar(self, pantalla):
        accion = False

        mousePos = pygame.mouse.get_pos()
        mouseClick = pygame.mouse.get_pressed()
        botonRect = Rect(self.posx,self.posy,self.ancho,self.alto)

        # cambiar color según hover
        if botonRect.collidepoint(mousePos):
            pygame.draw.rect(pantalla, self.colorHover, botonRect)

            # clic detectado
            if mouseClick[0] and not self.clicked:
                self.clicked = True
            elif not mouseClick[0] and self.clicked:
                self.clicked = False
                accion = True  # se ejecuta solo una vez por clic
        else:
            pygame.draw.rect(pantalla, self.colorNormal, botonRect)
            if not mouseClick[0]:
                self.clicked = False  # reset si se suelta fuera del botón
        
        # añadir el texto
        textImg = font.render(self.texto, True, self.colorTexto)
        textLen = textImg.get_width()
        pantalla.blit(textImg,(self.posx + int(self.ancho/2) - int(textLen/2), self.posy))
        return accion
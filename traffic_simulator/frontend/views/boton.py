
import pygame
from pygame.locals import *

pygame.init()

resolucion = (1920,1080)
font = pygame.font.Font(pygame.font.get_default_font(), 25)
class boton():
    def __init__(self, colorNormal, colorHover, colorTexto, posx, posy, alto, ancho, texto):
        self.colorNormal = colorNormal
        self.colorHover = colorHover
        self.colorTexto = colorTexto
        self.posx = posx
        self.posy = posy
        self.alto = alto
        self.ancho = ancho
        self.texto = texto
        self.clicked = False
    def renderizar(self, pantalla):
        accion = False

        mousePos = pygame.mouse.get_pos()
        mouseClick = pygame.mouse.get_pressed()
        botonRect = Rect(self.posx,self.posy,self.ancho,self.alto)

        # detectar clics
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
        textAlt = textImg.get_height()
        pantalla.blit(textImg,(self.posx + int(self.ancho/2) - int(textLen/2), (self.posy + int(self.alto/2)- int(textAlt/2))))
        return accion
    
class botonImg():
    def __init__(self, posx, posy, alto, ancho, imagen):
        self.posx = posx
        self.posy = posy
        self.alto = alto
        self.ancho = ancho
        self.imagen = imagen
        self.clicked = False

    def renderizar(self, pantalla):
        accion = False
        imagenOriginal = self.imagen
        self.imagen = pygame.transform.scale(imagenOriginal,(self.ancho,self.alto))
        pantalla.blit(self.imagen, (self.posx, self.posy))

        mousePos = pygame.mouse.get_pos()
        mouseClick = pygame.mouse.get_pressed()
        botonRect = Rect(self.posx,self.posy,self.ancho,self.alto)

        # detectar clics
        if botonRect.collidepoint(mousePos):
            # clic detectado
            if mouseClick[0] and not self.clicked:
                self.clicked = True
            elif not mouseClick[0] and self.clicked:
                self.clicked = False
                accion = True  # se ejecuta solo una vez por clic
        else:
            if not mouseClick[0]:
                self.clicked = False  # reset si se suelta fuera del botón
        return accion
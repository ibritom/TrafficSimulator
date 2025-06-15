import pygame
from pygame.locals import *
from boton import *

## basico de pygame
pygame.init()
resolucion = (1366,768)
pantalla = pygame.display.set_mode(resolucion)
ancho = pantalla.get_width()
largo = pantalla.get_height()

## elementos de la ui
# rects que no interactuan con el usuario
uiRect = Rect(0, 576, ancho, (largo/4))
atributosRect = (390, 590, 250, 170)
# imagenes
playImg = pygame.image.load("assets/playbutton.png")
pauseImg = pygame.image.load("assets/pausebutton.png")
# botones
botonSalir = boton((0,0,0),(0,255,0),(255,255,255),0,0,100,100,"Salir")
botonCiudad = boton((255,255,255),(30,30,30),(0,0,0),10,590,170,170,"Ciudad")
botonTrafico = boton((255,255,255),(30,30,30),(0,0,0),200,590,50,170,"Tráfico")
botonCalle = boton((255,255,255),(30,30,30),(0,0,0),200,650,50,170,"Calle")
botonPlay = botonImg(650,590,170,170,playImg)
botonPause = botonImg(820,590,170,170,pauseImg)
botonAcelerar = boton((255,255,255),(30,30,30),(0,0,0),1000,590,50,170,"Acelerar sim")
botonDecelerar = boton((255,255,255),(30,30,30),(0,0,0),1000,650,50,170,"Decelerar sim")

while True:
    pantalla.fill((255, 255, 255))
    # renderizar el rect que va a contener los botones
    pygame.draw.rect(pantalla, (0,0,0), uiRect)
    pygame.draw.rect(pantalla, (255,255,255), atributosRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    # revisar si el boton esta pulsado
    if botonSalir.renderizar(pantalla):
        pygame.quit()
    if botonCiudad.renderizar(pantalla):
        print("Añadir ciudad")
    if botonTrafico.renderizar(pantalla):
        print("Tráfico")
    if botonCalle.renderizar(pantalla):
        print("Calle")
    if botonPlay.renderizar(pantalla):
        print("Play")
    if botonPause.renderizar(pantalla):
        print("Pause")
    if botonAcelerar.renderizar(pantalla):
        print("Acelerar")
    if botonDecelerar.renderizar(pantalla):
        print("Decelerar")

    pygame.display.update()
import pygame
from boton import *

pygame.init()

resolucion = (1920,1080)
pantalla = pygame.display.set_mode(resolucion)
ancho = pantalla.get_width()
largo = pantalla.get_height()

botonSalir = boton((0,0,0),(255,255,255),(0,255,0),0,0,100,100,"Salir")
pygame.init()

while True:
    pantalla.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # revisar si el boton esta pulsado
    if botonSalir.renderizar(pantalla):
        pygame.quit()

    pygame.display.flip()
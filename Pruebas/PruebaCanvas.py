import pygame
from boton import *

pygame.init()

resolucion = (1920,1080)
pantalla = pygame.display.set_mode(resolucion)
color = (255,255,255)
color2 = (254, 254, 254)
ancho = pantalla.get_width()
largo = pantalla.get_height()
fontBoton = pygame.font.SysFont('notosansmono', 35)
textoBoton = fontBoton.render('quit', True, color)

botonTest = boton((0,0,0),0,0,100,100,fontBoton,textoBoton)

while True:
    mouse = pygame.mouse.get_pos()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
    pantalla.fill(color)
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if botonTest.ancho/2 <= mouse[0] <= botonTest.ancho/2+140 and botonTest.alto/2 <= mouse[1] <= botonTest.alto/2+40:
        pygame.draw.rect(pantalla,color2,[botonTest.ancho/2,botonTest.alto/2,140,40])    
    else:
        pygame.draw.rect(pantalla,color,[botonTest.ancho/2,botonTest.alto/2,140,40])
    pygame.display.flip()
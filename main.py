from figura import *  # Importar la clase figura desde el módulo figura.py
import pygame
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Dibujo de Figuras")

    # Crear una figura
    rectangulo = Rectangulo(pantalla=pantalla, x1=100, y1=100, x2=200, y2=200, tag="rectangulo")

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pantalla.fill((255, 255, 255))  # Limpiar pantalla con color blanco
        rectangulo.dibujar()      # Dibujar la figura
        pygame.display.flip()              # Actualizar pantalla

    pygame.quit()
main()
# This code initializes a Pygame window and draws a rectangle using the figura class.

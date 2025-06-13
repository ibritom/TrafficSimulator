import  pygame
from figura import *
def mostrar_pantalla():
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Dibujo de Figuras")

    pantalla.fill((255, 255, 255))  # Limpiar pantalla con color blanco
    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()  # Actualizar pantalla

    pygame.quit()
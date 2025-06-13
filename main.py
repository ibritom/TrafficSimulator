from figura import *  # Importar la clase figura desde el módulo figura.py
import pygame
from lista import *
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Dibujo de Figuras")

    # Crear una figura
    rectangulo = Figura.crear_rectangulo(pantalla, 20, 30, 30, 30, color="rojo")
    circulo = Figura.crear_circulo(pantalla, 60, 60, 120, 120, color="rojo")
    linea = Figura.crear_linea(pantalla, (300, 300), (155, 155), 5, color="rojo")

    lista_figuras = LinkedListQueue()
    lista_figuras.enqueue(rectangulo)
    lista_figuras.enqueue(circulo)
    lista_figuras.enqueue(linea)

    # Dibujar la figura
    actual = lista_figuras.front
    pantalla.fill((255, 255, 255))  # Limpiar pantalla con color blanco
    while actual is not None:
        actual.data.dibujar()
        actual = actual.next
    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()              # Actualizar pantalla

    pygame.quit()
main()
# This code initializes a Pygame window and draws a rectangle using the figura class.

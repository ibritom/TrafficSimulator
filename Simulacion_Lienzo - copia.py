import pygame
import sys
import math
from Simulación import Simulacion

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 1200
ALTO = 800
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 100, 200)
ROJO = (200, 50, 50)
VERDE = (50, 200, 50)
GRIS = (128, 128, 128)
AZUL_CLARO = (173, 216, 230)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)


class CarroVisual:
    def __init__(self, ruta_con_info):
        self.ruta = ruta_con_info  # Lista de (nombre, (x, y))
        self.indice = 0
        self.pos = list(ruta_con_info[0][1]) if ruta_con_info else [0, 0]
        self.velocidad = 2  # píxeles por frame
        self.activo = True

    def mover(self):
        if not self.activo or self.indice + 1 >= len(self.ruta):
            return

        destino = self.ruta[self.indice + 1][1]
        dx = destino[0] - self.pos[0]
        dy = destino[1] - self.pos[1]
        distancia = math.hypot(dx, dy)

        if distancia < self.velocidad:
            self.pos = list(destino)
            self.indice += 1
            if self.indice + 1 >= len(self.ruta):
                self.activo = False
        else:
            self.pos[0] += self.velocidad * dx / distancia
            self.pos[1] += self.velocidad * dy / distancia

    def dibujar(self, pantalla):
        if self.ruta:
            pygame.draw.circle(pantalla, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), 10)


class TrafficSimulatorCanvas:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Traffic Simulator - Lienzo de Prueba")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 24)
        self.fuente_pequena = pygame.font.Font(None, 18)

        # Estado de la aplicación
        self.simulacion = Simulacion()
        self.modo = "AGREGAR_NODO"  # AGREGAR_NODO, CONECTAR_NODOS, DIJKSTRA
        self.nodo_seleccionado = None
        self.origen_conexion = None
        self.nodo_origen_dijkstra = None
        self.mostrar_rutas = False
        #self.carro = None
        self.carros = []
        self.esperando_destino = False

        # Cargar datos de ejemplo
        self.cargar_datos_ejemplo()

    def cargar_datos_ejemplo(self):
        """Carga los datos de ejemplo del mainSimulación.py"""
        self.simulacion.agregar_nodo("Cartago", 150, 200)
        self.simulacion.agregar_nodo("San José", 300, 250)
        self.simulacion.agregar_nodo("Alajuela", 450, 150)
        self.simulacion.agregar_nodo("Puntarenas", 200, 400)
        self.simulacion.agregar_nodo("Limón", 600, 300)

        self.simulacion.conectar("Cartago", "San José", 10)
        self.simulacion.conectar("San José", "Alajuela", 5)
        self.simulacion.conectar("Alajuela", "Puntarenas", 20)
        self.simulacion.conectar("Cartago", "Puntarenas", 100)
        self.simulacion.conectar("San José", "Limón", 15)
        self.simulacion.conectar("Alajuela", "Limón", 12)

    def dibujar_nodo(self, nodo, color=AZUL):
        """Dibuja un nodo en el lienzo"""
        pygame.draw.circle(self.pantalla, color, (int(nodo.x), int(nodo.y)), 20)
        pygame.draw.circle(self.pantalla, NEGRO, (int(nodo.x), int(nodo.y)), 20, 2)

        # Dibujar nombre del nodo
        texto = self.fuente_pequena.render(nodo.nombre, True, NEGRO)
        texto_rect = texto.get_rect(center=(nodo.x, nodo.y - 35))
        self.pantalla.blit(texto, texto_rect)

        # Mostrar distancia si Dijkstra fue ejecutado
        if hasattr(nodo, 'distancia') and nodo.distancia != 999999:
            dist_texto = self.fuente_pequena.render(f"d:{nodo.distancia}", True, ROJO)
            dist_rect = dist_texto.get_rect(center=(nodo.x + 25, nodo.y - 25))
            self.pantalla.blit(dist_texto, dist_rect)

    def dibujar_conexion(self, origen, destino, peso, color=GRIS):
        """Dibuja una conexión entre dos nodos"""
        pygame.draw.line(self.pantalla, color, (origen.x, origen.y), (destino.x, destino.y), 3)

        # Calcular posición del texto del peso
        mid_x = (origen.x + destino.x) / 2
        mid_y = (origen.y + destino.y) / 2

        # Dibujar peso de la conexión
        peso_texto = self.fuente_pequena.render(str(peso), True, NEGRO)
        peso_rect = peso_texto.get_rect(center=(mid_x, mid_y))

        # Fondo blanco para el texto
        pygame.draw.rect(self.pantalla, BLANCO, peso_rect.inflate(4, 2))
        self.pantalla.blit(peso_texto, peso_rect)

    def dibujar_ruta(self, ruta, color=VERDE):
        """Dibuja una ruta específica resaltada"""
        if len(ruta) < 2:
            return

        for i in range(len(ruta) - 1):
            nodo_actual = self.simulacion.buscar_nodo(ruta[i])
            nodo_siguiente = self.simulacion.buscar_nodo(ruta[i + 1])

            if nodo_actual and nodo_siguiente:
                pygame.draw.line(self.pantalla, color,
                                 (nodo_actual.x, nodo_actual.y),
                                 (nodo_siguiente.x, nodo_siguiente.y), 6)

    def obtener_nodo_en_posicion(self, pos):
        """Encuentra el nodo más cercano a una posición dada"""
        x, y = pos
        actual = self.simulacion.nodos
        while actual:
            distancia = math.sqrt((actual.x - x) ** 2 + (actual.y - y) ** 2)
            if distancia <= 25:  # Radio de detección
                return actual
            actual = actual.siguiente
        return None

    def manejar_click(self, pos):
        """Maneja los clics del mouse según el modo actual"""
        if self.modo == "AGREGAR_NODO":
            # Verificar que no haya un nodo muy cerca
            if not self.obtener_nodo_en_posicion(pos):
                nombre = f"Nodo_{len(self.obtener_todos_los_nodos())}"
                self.simulacion.agregar_nodo(nombre, pos[0], pos[1])

        elif self.modo == "CONECTAR_NODOS":
            nodo_clickeado = self.obtener_nodo_en_posicion(pos)
            if nodo_clickeado:
                if self.origen_conexion is None:
                    self.origen_conexion = nodo_clickeado
                else:
                    if self.origen_conexion != nodo_clickeado:
                        # Conectar con peso predeterminado
                        peso = int(math.sqrt((self.origen_conexion.x - nodo_clickeado.x) ** 2 +
                                             (self.origen_conexion.y - nodo_clickeado.y) ** 2) / 10)
                        self.simulacion.conectar(self.origen_conexion.nombre, nodo_clickeado.nombre, peso)
                    self.origen_conexion = None



        elif self.modo == "DIJKSTRA":

            nodo_clickeado = self.obtener_nodo_en_posicion(pos)

            if nodo_clickeado:

                if not self.nodo_origen_dijkstra or not self.esperando_destino:

                    # Establecer un nuevo nodo origen y recalcular rutas

                    self.nodo_origen_dijkstra = nodo_clickeado

                    self.simulacion.dijkstra(nodo_clickeado.nombre)

                    self.mostrar_rutas = True

                    self.esperando_destino = True  # Ahora esperamos destino

                else:

                    # Enviamos un carro hacia el destino

                    ruta_info = self.simulacion.obtener_ruta_con_info(nodo_clickeado.nombre)

                    if ruta_info and len(ruta_info) > 1:
                        self.carros.append(CarroVisual(ruta_info))

    def obtener_todos_los_nodos(self):
        """Retorna una lista de todos los nodos"""
        nodos = []
        actual = self.simulacion.nodos
        while actual:
            nodos.append(actual)
            actual = actual.siguiente
        return nodos

    def dibujar_interfaz(self):
        """Dibuja la interfaz de usuario"""
        # Panel de información
        panel_y = 10

        # Modo actual
        modo_texto = self.fuente.render(f"Modo: {self.modo}", True, NEGRO)
        self.pantalla.blit(modo_texto, (10, panel_y))
        panel_y += 30

        # Instrucciones según el modo
        if self.modo == "AGREGAR_NODO":
            instruccion = "Click para agregar nodo"
        elif self.modo == "CONECTAR_NODOS":
            if self.origen_conexion:
                instruccion = f"Click destino para conectar desde {self.origen_conexion.nombre}"
            else:
                instruccion = "Click nodo origen para conexión"
        elif self.modo == "DIJKSTRA":
            instruccion = "Click nodo para calcular rutas más cortas"

        inst_texto = self.fuente_pequena.render(instruccion, True, AZUL)
        self.pantalla.blit(inst_texto, (10, panel_y))
        panel_y += 25

        # Controles
        controles = [
            "1: Agregar Nodos", "2: Conectar Nodos", "3: Dijkstra",
            "R: Mostrar/Ocultar Rutas", "C: Limpiar", "ESC: Salir"
        ]

        for i, control in enumerate(controles):
            control_texto = self.fuente_pequena.render(control, True, GRIS)
            self.pantalla.blit(control_texto, (10, panel_y + i * 20))

        # Información del algoritmo Dijkstra
        if self.nodo_origen_dijkstra and self.mostrar_rutas:
            panel_y += len(controles) * 20 + 20
            dijkstra_texto = self.fuente.render(f"Dijkstra desde: {self.nodo_origen_dijkstra.nombre}", True, VERDE)
            self.pantalla.blit(dijkstra_texto, (10, panel_y))

            # Mostrar algunas rutas de ejemplo
            nodos = self.obtener_todos_los_nodos()
            panel_y += 30
            for nodo in nodos[:5]:  # Mostrar solo los primeros 5
                if nodo != self.nodo_origen_dijkstra:
                    ruta = self.simulacion.obtener_ruta(nodo.nombre)
                    if ruta:
                        ruta_str = " → ".join(ruta)
                        if len(ruta_str) > 40:
                            ruta_str = ruta_str[:37] + "..."
                        ruta_texto = self.fuente_pequena.render(
                            f"A {nodo.nombre}: {ruta_str} (d:{nodo.distancia})", True, NEGRO)
                        self.pantalla.blit(ruta_texto, (10, panel_y))
                        panel_y += 18

    def dibujar_grafo(self):
        """Dibuja todo el grafo"""
        # Dibujar todas las conexiones primero
        actual = self.simulacion.nodos
        while actual:
            conexion = actual.adyacentes.cabeza
            while conexion:
                # Solo dibujar cada conexión una vez (evitar duplicados)
                if actual.nombre < conexion.destino.nombre:
                    self.dibujar_conexion(actual, conexion.destino, conexion.peso)
                conexion = conexion.siguiente
            actual = actual.siguiente

        # Dibujar rutas de Dijkstra si están habilitadas
        if self.mostrar_rutas and self.nodo_origen_dijkstra:
            nodos = self.obtener_todos_los_nodos()
            colores_ruta = [VERDE, AMARILLO, NARANJA, ROJO]
            for i, nodo in enumerate(nodos):
                if nodo != self.nodo_origen_dijkstra and nodo.distancia != 999999:
                    ruta = self.simulacion.obtener_ruta(nodo.nombre)
                    if ruta and len(ruta) > 1:
                        color = colores_ruta[i % len(colores_ruta)]
                        self.dibujar_ruta(ruta, color)

        # Dibujar todos los nodos
        actual = self.simulacion.nodos
        while actual:
            color = AZUL
            if actual == self.nodo_origen_dijkstra:
                color = VERDE
            elif actual == self.origen_conexion:
                color = AMARILLO
            self.dibujar_nodo(actual, color)
            actual = actual.siguiente

    def ejecutar(self):
        """Bucle principal de la aplicación"""
        ejecutando = True

        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                    elif evento.key == pygame.K_1:
                        self.modo = "AGREGAR_NODO"
                        self.origen_conexion = None
                        self.nodo_origen_dijkstra = None
                        #self.carro = None
                        self.carros = []
                    elif evento.key == pygame.K_2:
                        self.modo = "CONECTAR_NODOS"
                        self.origen_conexion = None
                        self.nodo_origen_dijkstra = None
                        #self.carro = None
                        self.carros = []
                    elif evento.key == pygame.K_3:
                        self.modo = "DIJKSTRA"
                        self.origen_conexion = None
                        #self.carro = None
                    elif evento.key == pygame.K_r:
                        self.mostrar_rutas = not self.mostrar_rutas
                    elif evento.key == pygame.K_c:
                        # Limpiar simulación
                        self.simulacion = Simulacion()
                        self.nodo_origen_dijkstra = None
                        self.origen_conexion = None
                        #self.carro = None
                        self.carros = []
                        self.mostrar_rutas = False

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:  # Click izquierdo
                        self.manejar_click(evento.pos)

            # Limpiar pantalla
            self.pantalla.fill(BLANCO)

            # Dibujar todo
            self.dibujar_grafo()
            self.dibujar_interfaz()

            for carro in self.carros:
                carro.mover()
                carro.dibujar(self.pantalla)

            # Actualizar pantalla
            pygame.display.flip()
            self.reloj.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Función principal"""
    print("=== TRAFFIC SIMULATOR - LIENZO DE PRUEBA ===")
    print("Controles:")
    print("- 1: Modo agregar nodos")
    print("- 2: Modo conectar nodos")
    print("- 3: Modo Dijkstra")
    print("- R: Mostrar/ocultar rutas")
    print("- C: Limpiar lienzo")
    print("- ESC: Salir")
    print("\nCargando datos de ejemplo...")

    app = TrafficSimulatorCanvas()
    app.ejecutar()


if __name__ == "__main__":
    main()
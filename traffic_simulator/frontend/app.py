# frontend/app.py
import pygame
import sys
from pygame.locals import *
from traffic_simulator.frontend.views.main_view import MainView
from traffic_simulator.frontend.controllers.simulacion_controller import SimulacionController
from traffic_simulator.backend.utils.constantes import *


class TrafficSimulatorApp:
    """Clase principal de la aplicación que implementa el patrón MVC.

    Responsabilidades:
    - Inicializar y gestionar el bucle principal del juego
    - Coordinar entre el modelo, vista y controlador
    - Manejar eventos del sistema
    """

    def __init__(self):
        """Inicializa la aplicación con el patrón MVC completo"""
        self._inicializar_pygame()
        self._inicializar_mvc()
        self._ejecutando = True
        self._reloj = pygame.time.Clock()
        self._velocidad_simulacion = 1.0
        self._pausado = False

    def _inicializar_pygame(self):
        """Configura los componentes básicos de PyGame"""
        pygame.init()
        self._pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Traffic Simulator - Algoritmos y Estructuras de Datos")
        pygame.font.init()

    def _inicializar_mvc(self):
        """Inicializa el patrón MVC con dependencias inyectadas"""
        # Capa Controller
        self._controller = SimulacionController()

        # Capa View (inyectando el controller)
        self._main_view = MainView(self._controller)

        # Configuración inicial de ejemplo
        self._configurar_ejemplo_inicial()

    def _configurar_ejemplo_inicial(self):
        """Configura algunos nodos y conexiones de ejemplo"""
        # Nodos de ejemplo
        ciudades = [
            ("San José", 400, 300),
            ("Cartago", 600, 400),
            ("Heredia", 300, 200),
            ("Alajuela", 200, 250),
            ("Puntarenas", 150, 450)
        ]

        for nombre, x, y in ciudades:
            self._controller._manejar_agregar_nodo(x, y)

        # Conexiones de ejemplo
        conexiones = [
            ("San José", "Cartago"),
            ("San José", "Heredia"),
            ("San José", "Alajuela"),
            ("Alajuela", "Puntarenas"),
            ("Heredia", "Alajuela")
        ]

        for origen, destino in conexiones:
            self._controller._simulacion.conectar_nodos(
                f"nodo_{ciudades.index(next(c for c in ciudades if c[0] == origen)) + 1}",
                f"nodo_{ciudades.index(next(c for c in ciudades if c[0] == destino)) + 1}"
            )

    def ejecutar(self):
        """Bucle principal de la aplicación"""
        self._mostrar_bienvenida()

        while self._ejecutando:
            self._manejar_eventos()

            if not self._pausado:
                self._actualizar_estado()

            self._renderizar()
            self._reloj.tick(FPS)

        self._cerrar_aplicacion()

    def _mostrar_bienvenida(self):
        """Muestra información inicial en consola"""
        print("=== Traffic Simulator ===")
        print("Controles:")
        print("1: Modo Agregar Nodos")
        print("2: Modo Conectar Nodos")
        print("3: Modo Dijkstra")
        print("R: Mostrar/Ocultar Rutas")
        print("S: Generar Vehículos Aleatorios")
        print("C: Limpiar Simulación")
        print("ESPACIO: Pausar/Reanudar")
        print("+: Aumentar velocidad")
        print("-: Disminuir velocidad")
        print("ESC: Salir")

    def _manejar_eventos(self):
        """Procesa todos los eventos del sistema"""
        for evento in pygame.event.get():
            if evento.type == QUIT:
                self._ejecutando = False
            elif evento.type == MOUSEBUTTONDOWN:
                self._manejar_click(evento)
            elif evento.type == KEYDOWN:
                self._manejar_teclado(evento)

    def _manejar_click(self, evento):
        """Maneja eventos de mouse"""
        pos = evento.pos
        if evento.button == 1:  # Click izquierdo
            self._controller.manejar_click(pos[0], pos[1])
        elif evento.button == 3:  # Click derecho
            if self._controller._modo_actual == "DIJKSTRA":
                self._controller.agregar_vehiculo_destino(pos[0], pos[1])

    def _manejar_click(self, evento):
        """Maneja eventos de mouse"""
        pos = evento.pos
        if evento.button == 1:  # Click izquierdo
            self._controller.manejar_click(pos[0], pos[1])
        elif evento.button == 3:  # Click derecho
            # Modificado para usar el método existente del controlador
            if self._controller._modo_actual == "DIJKSTRA":
                nodo = self._controller._simulacion.obtener_nodo_por_posicion(pos[0], pos[1])
                if nodo:
                    self._controller.agregar_carro(nodo.identificador)

    def _manejar_teclado(self, evento):
        """Maneja eventos de teclado"""
        teclas = {
            K_1: lambda: self._controller.cambiar_modo("AGREGAR_NODO"),
            K_2: lambda: self._controller.cambiar_modo("CONECTAR_NODOS"),
            K_3: lambda: self._controller.cambiar_modo("DIJKSTRA"),
            K_r: self._controller.alternar_visualizacion_rutas,
            K_c: self._controller.reiniciar_simulacion,
            K_s: lambda: self._controller.generar_vehiculos_aleatorios(5),
            K_PLUS: lambda: self._cambiar_velocidad(0.5),
            K_MINUS: lambda: self._cambiar_velocidad(-0.5),
            K_SPACE: self._alternar_pausa,
            K_ESCAPE: lambda: setattr(self, '_ejecutando', False)
        }

        if evento.key in teclas:
            teclas[evento.key]()

    def _cambiar_velocidad(self, incremento):
        """Ajusta la velocidad de simulación"""
        self._velocidad_simulacion = max(0.1, min(5.0, self._velocidad_simulacion + incremento))
        print(f"Velocidad de simulación: {self._velocidad_simulacion}x")

    def _alternar_pausa(self):
        """Pausa o reanuda la simulación"""
        self._pausado = not self._pausado
        estado = "PAUSADO" if self._pausado else "REANUDADO"
        print(f"Simulación {estado}")

    def _actualizar_estado(self):
        """Actualiza el estado de la simulación"""
        # Actualización basada en velocidad
        for _ in range(int(self._velocidad_simulacion)):
            self._controller.actualizar_simulacion()

    def _renderizar(self):
        """Renderiza todos los componentes"""
        self._pantalla.fill(BLANCO)
        self._main_view.renderizar(self._pantalla)
        pygame.display.flip()

    def _cerrar_aplicacion(self):
        """Libera recursos al cerrar la aplicación"""
        pygame.quit()
        sys.exit()

    def __del__(self):
        """Destructor para limpieza segura"""
        if pygame.get_init():
            pygame.quit()
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
        self._tiempo_ultimo_auto = 0  # tiempo del último vehículo generado
        self._intervalo_generacion = 500 # 2000 ms = 2 segundos
        self._simulacion_activa = False  # ← la simulación no arranca automáticamente

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
        self._main_view = MainView(self._controller, self._pantalla)
        # ✅ ESTA LÍNEA ES CLAVE:
        self._controller.establecer_vista(self._main_view)

        self._configurar_ejemplo_inicial()


        # Configuración inicial de ejemplo
        self._configurar_ejemplo_inicial()

    def _configurar_ejemplo_inicial(self):
        """Configura algunos nodos y conexiones de ejemplo"""
        # Nodos de ejemplo
        ciudades = [
            ("Atenas", 400, 300),
            ("Tibás", 600, 400),
            ("Quepos", 300, 200),
            ("Liberia", 200, 250),
            ("Upala", 150, 450),
            ("Tres Ríos", 800,500),
            ("Paraíso",1200,500),
            ("Prusia",1200,50),
            ("San Pedro",700,200),
            ("Guadalupe",950,300),
            ("San Rafael",452, 98),
            ("Pavas",351, 495),
            ("Puerto Viejo",1252, 276),
            ("San Isidro",811, 52)


        ]

        for nombre, x, y in ciudades:
            self._controller.crear_nodo_con_nombre(nombre, x, y)

        # Conexiones de ejemplo
        conexiones = [
            ("Atenas", "Tibás"),
            ("Atenas", "Quepos"),
            ("Atenas", "Liberia"),
            ("Liberia", "Upala"),
            ("Quepos", "Liberia"),
            ("Tibás", "Guadalupe"),
            ("Guadalupe", "San Pedro"),
            ("San Pedro", "Tres Ríos"),
            ("Tres Ríos", "Paraíso"),
            ("Paraíso", "Prusia"),
            ("Prusia", "Puerto Viejo"),
            ("Puerto Viejo", "San Rafael"),
            ("San Rafael", "San Isidro"),
            ("San Isidro", "Pavas"),
            ("Pavas", "Tibás")
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
        print("4: Modo Obstáculo (click arista)")
        print("5-9: Seleccionar tipo de obstáculo")
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
                # 🔹 Si el popup está activo, enviarle eventos exclusivamente
            elif self._main_view.popup_activo():
                self._main_view.manejar_evento(evento)

            elif evento.type == MOUSEBUTTONDOWN:
                self._manejar_click(evento)
            elif evento.type == KEYDOWN:
                self._manejar_teclado(evento)
            else:
                self._main_view.manejar_evento(evento)

    def _manejar_click(self, evento):
        """Maneja eventos de mouse"""
        pos = evento.pos
        if evento.button == 1:  # Click izquierdo
            vehiculo = self._controller.obtener_vehiculo_en_posicion(pos[0], pos[1])
            if vehiculo:
                self._controller.seleccionar_vehiculo(vehiculo)

            else:
                self._controller.manejar_click(pos[0], pos[1])
        elif evento.button == 3:  # Click derecho
            if self._controller._modo_actual == "DIJKSTRA":
                self._controller.agregar_vehiculo_destino(pos[0], pos[1])



    def _manejar_teclado(self, evento):
        """Maneja eventos de teclado"""
        teclas = {
            K_1: lambda: self._controller.cambiar_modo("AGREGAR_NODO"),
            K_2: lambda: self._controller.cambiar_modo("CONECTAR_NODOS"),
            K_3: lambda: self._controller.cambiar_modo("DIJKSTRA"),
            K_r: self._controller.alternar_visualizacion_rutas,
            K_c: self._controller.reiniciar_simulacion,
            K_s: lambda: self._controller.generar_vehiculos_aleatorios(10),
            K_p: self._iniciar_simulacion_automatica,
            K_i: lambda: self._controller.cambiar_modo("INFO"),


            K_4: lambda: self._controller.cambiar_modo("OBSTACULO"),
            K_5: lambda: self._controller.seleccionar_tipo_obstaculo("accidentes"),
            K_6: lambda: self._controller.seleccionar_tipo_obstaculo("construcciones"),
            K_7: lambda: self._controller.seleccionar_tipo_obstaculo("operativos"),
            K_8: lambda: self._controller.seleccionar_tipo_obstaculo("clima_adverso"),
            K_9: lambda: self._controller.seleccionar_tipo_obstaculo("bloqueada"),

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
        for _ in range(int(self._velocidad_simulacion)):
            self._controller.actualizar_simulacion()

        if self._simulacion_activa:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self._tiempo_ultimo_auto >= self._intervalo_generacion:

                self._controller.generar_vehiculos_aleatorios(4)
                self._tiempo_ultimo_auto = tiempo_actual

    def _renderizar(self):
        """Renderiza todos los componentes"""

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

    def _iniciar_simulacion_automatica(self):
        """Inicia la simulación automática al presionar 'P'"""
        if not self._simulacion_activa:
            self._simulacion_activa = True
            self._tiempo_ultimo_auto = pygame.time.get_ticks()
            print("Simulación automática iniciada")
        else:
            print("Simulación ya estaba activa")
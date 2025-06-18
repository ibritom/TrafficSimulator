import os
from pathlib import Path
from traffic_simulator.frontend.views.base_view import BaseView
from traffic_simulator.frontend.views.boton import *
from traffic_simulator.frontend.controllers.simulacion_controller import *


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Cargar imágenes con manejo de errores
try:
    play_img_path = os.path.join(BASE_DIR, "assets", "playbutton.png")
    pause_img_path = os.path.join(BASE_DIR, "assets", "pausebutton.png")

    playImg = pygame.image.load(play_img_path)
    pauseImg = pygame.image.load(pause_img_path)
except pygame.error as e:
    print(f"Error cargando imágenes: {e}")
    # Crear imágenes de respaldo
    playImg = pygame.Surface((100, 100))
    playImg.fill((0, 255, 0))  # Verde para play
    pauseImg = pygame.Surface((100, 100))
    pauseImg.fill((255, 0, 0))  # Rojo para pause


class PanelControlView(BaseView):
    """Vista para el panel de control - Principio SRP"""

    def __init__(self, controller):
        super().__init__(controller)
        self._fuente = pygame.font.Font(None, 24)
        self._fuente_pequena = pygame.font.Font(None, 18)
        self.boton_Nodo = boton((255,255,255),(30,30,30),(0,0,0),10,590,170,170,"Ciudad")
        self.boton_Vertice = boton((255,255,255),(30,30,30),(0,0,0),200,650,50,170,"Calle")
        self.boton_Peso = boton((255,255,255),(30,30,30),(0,0,0),200,590,50,170,"Tráfico")
        self.boton_Play = botonImg(650,590,170,170,playImg)
        self.boton_Pause = botonImg(820,590,170,170,pauseImg)
        self.boton_Acelerar = boton((255,255,255),(30,30,30),(0,0,0),1000,590,50,170,"Acelerar sim")
        self.boton_Decelerar = boton((255,255,255),(30,30,30),(0,0,0),1000,650,50,170,"Decelerar sim")
        self.uiRect = Rect(0, 576, ANCHO, (ALTO/4))
        self.atributosRect = (390, 590, 250, 170)

    def actualizar_desde_modelo(self, evento, datos):
        """Actualiza la vista basada en eventos del modelo"""
        pass

    def renderizar(self, pantalla):
        """Renderiza el panel de control"""
        estado = self._controller.obtener_estado_actual()
        modo = estado['modo']
        nodo_seleccionado = estado['nodo_seleccionado']
        nodo_origen_dijkstra = self._controller._simulacion._grafo.obtener_nodo(
            estado.get('nodo_origen_dijkstra', '')
        ) if estado.get('nodo_origen_dijkstra') else None

        panel_y = 10

        # Modo actual
        modo_texto = self._fuente.render(f"Modo: {modo}", True, NEGRO)
        pantalla.blit(modo_texto, (10, panel_y))
        panel_y += 30

        # Instrucciones según el modo
        if modo == "AGREGAR_NODO":
            instruccion = "Click para agregar nodo"
        elif modo == "CONECTAR_NODOS":
            if nodo_seleccionado:
                instruccion = f"Click destino para conectar desde {nodo_seleccionado.nombre}"
            else:
                instruccion = "Click nodo origen para conexión"
        elif modo == "DIJKSTRA":
            instruccion = "Click nodo para calcular rutas más cortas"
        else:
            instruccion = ""

        inst_texto = self._fuente_pequena.render(instruccion, True, AZUL)
        pantalla.blit(inst_texto, (10, panel_y))
        panel_y += 25

        # Controles
        controles = [
            "1: Agregar Nodos", "2: Conectar Nodos", "3: Dijkstra",
            "R: Mostrar/Ocultar Rutas", "C: Limpiar", "ESC: Salir"
        ]

        for i, control in enumerate(controles):
            control_texto = self._fuente_pequena.render(control, True, GRIS)
            pantalla.blit(control_texto, (10, panel_y + i * 20))

        # Información del algoritmo Dijkstra
        if nodo_origen_dijkstra:
            panel_y += len(controles) * 20 + 20
            dijkstra_texto = self._fuente.render(
                f"Dijkstra desde: {nodo_origen_dijkstra.nombre}", True, VERDE)
            pantalla.blit(dijkstra_texto, (10, panel_y))

            # Mostrar algunas rutas de ejemplo
            nodos = estado['nodos']
            panel_y += 30
            for nodo in nodos[:5]:  # Mostrar solo los primeros 5
                if nodo != nodo_origen_dijkstra:
                    ruta = self._controller._simulacion.obtener_ruta_entre_nodos(
                        nodo_origen_dijkstra.identificador,
                        nodo.identificador
                    )
                    if ruta:
                        ruta_str = " → ".join([n.nombre for n in ruta])
                        if len(ruta_str) > 40:
                            ruta_str = ruta_str[:37] + "..."
                        distancia = nodo.obtener_metadato('distancia', float('inf'))
                        ruta_texto = self._fuente_pequena.render(
                            f"A {nodo.nombre}: {ruta_str} (d:{int(distancia) if distancia != float('inf') else '∞'})",
                            True, NEGRO)
                        pantalla.blit(ruta_texto, (10, panel_y))
                        panel_y += 18
        # Botones
        pygame.draw.rect(pantalla, (0, 0, 0), self.uiRect)
        pygame.draw.rect(pantalla, (255, 255, 255), self.atributosRect)
        if self.boton_Nodo.renderizar(pantalla):
            mouse_x,mouse_y = pygame.mouse.get_pos()
            self._controller.cambiar_modo("AGREGAR_NODO")
            print("Agregar ciudad")
        if self.boton_Vertice.renderizar(pantalla):
            self._controller.cambiar_modo("CONECTAR_NODOS")
        if self.boton_Peso.renderizar(pantalla):
            print("Pesos")
        if self.boton_Play.renderizar(pantalla):
            print("Play")
        if self.boton_Pause.renderizar(pantalla):
            print("Pause")
        if self.boton_Acelerar.renderizar(pantalla):
            print("Acelerar")
        if self.boton_Decelerar.renderizar(pantalla):
            print("Decelerar")



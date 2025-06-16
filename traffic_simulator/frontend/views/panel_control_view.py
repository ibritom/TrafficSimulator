# frontend/views/panel_control_view.py
import pygame
from traffic_simulator.frontend.views.base_view import BaseView
from traffic_simulator.backend.utils.constantes import *
from traffic_simulator.frontend.views.boton import *
from traffic_simulator.backend.utils.constantes import *
from traffic_simulator.frontend.controllers.simulacion_controller import *


class PanelControlView(BaseView):
    """Vista para el panel de control - Principio SRP"""

    def __init__(self, controller):
        super().__init__(controller)
        self._fuente = pygame.font.Font(None, 24)
        self._fuente_pequena = pygame.font.Font(None, 18)
        self.boton_Nodo = boton((255,255,255),(30,30,30),(0,0,0),10,590,170,170,"Ciudad")

    def actualizar_desde_modelo(self, evento, datos):
        """Actualiza la vista basada en eventos del modelo"""
        pass  # El panel de control no necesita actualizaciones directas del modelo

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
        if self.boton_Nodo.renderizar(pantalla):
            mouse_x,mouse_y = pygame.mouse.get_pos()
            self._controller.cambiar_modo("AGREGAR_NODO")
            print("Agregar ciudad")


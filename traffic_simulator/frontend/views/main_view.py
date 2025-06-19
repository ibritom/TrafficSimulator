
import pygame
from traffic_simulator.frontend.views.base_view import BaseView
from traffic_simulator.frontend.views.grafo_view import GrafoView
from traffic_simulator.frontend.views.panel_control_view import PanelControlView
from traffic_simulator.frontend.views.info_estado_view import InfoEstadoView
from traffic_simulator.backend.utils.constantes import *
from traffic_simulator.frontend.views.nombre_ciudad_popup import NombreCiudadPopup

class MainView(BaseView):
    """Vista principal que compone otras vistas - Patrón Composite"""

    def __init__(self, controller, pantalla):
        super().__init__(controller)
        self._pantalla = pantalla  # ← Guardamos la surface real
        self._grafo_view = GrafoView(controller)
        self._panel_control_view = PanelControlView(controller)
        self._info_estado_view = InfoEstadoView(controller)
        self._popup = None
        self._mostrar_recomendaciones = False
        self._puntos_criticos_guardados = []  # ← se llena al presionar T

    def actualizar_desde_modelo(self, evento, datos):
        """Propaga las actualizaciones a las vistas hijas"""
        self._grafo_view.actualizar_desde_modelo(evento, datos)
        self._panel_control_view.actualizar_desde_modelo(evento, datos)
        self._info_estado_view.actualizar_desde_modelo(evento, datos)

    def renderizar(self, pantalla):
        """Renderiza todas las vistas hijas"""
        # Fondo blanco
        pantalla.fill(BLANCO)
        # Renderizar popup si está activo
        self._grafo_view.renderizar(pantalla)
        self._panel_control_view.renderizar(pantalla)
        self._info_estado_view.renderizar(pantalla)

        vehiculo = self._controller.obtener_vehiculo_seleccionado()
        if vehiculo:
            self._mostrar_info_vehiculo(pantalla, vehiculo)
        if self._mostrar_recomendaciones:
            self._mostrar_recomendaciones_criticas(pantalla)

        # Orden de renderizado importante

        if self.popup_activo():

            self._popup.dibujar()
        vehiculo = self._controller.obtener_vehiculo_seleccionado()
        if vehiculo:
            self._mostrar_info_vehiculo(pantalla, vehiculo)


    def mostrar_popup_nombre_ciudad(self, x, y):
        print(f"[Popup] Creando popup en ({x}, {y})")
        self._popup = NombreCiudadPopup(self._pantalla, self._controller, x, y)
    def popup_activo(self):
        return self._popup is not None and self._popup.activo

    def manejar_evento(self, evento):
        """Procesa eventos para popup si está activo"""
        if self.popup_activo():
            self._popup.manejar_evento(evento)
            return True  # evento consumido
        else:
            # Distribuye evento a las vistas hijas si no hay popup
            self._grafo_view.manejar_evento(evento)
            self._panel_control_view.manejar_evento(evento)
            self._info_estado_view.manejar_evento(evento)
            return False

    def _mostrar_info_vehiculo(self, pantalla, vehiculo):
        fuente = pygame.font.Font(None, 22)
        x, y, ancho, alto = 10, 590, 250, 170
        fondo = pygame.Rect(x, y, ancho, alto)

        # Fondo y borde
        pygame.draw.rect(pantalla, (240, 240, 240), fondo)
        pygame.draw.rect(pantalla, NEGRO, fondo, 2)

        # Ruta completa
        ruta_str = " - ".join(nodo.nombre for nodo in vehiculo._ruta)

        # Información base
        lineas = [
            f"Tipo: {vehiculo.tipo}",
            f"Origen: {vehiculo._ruta[0].nombre if vehiculo._ruta else 'N/A'}",
            f"Destino: {vehiculo._ruta[-1].nombre if vehiculo._ruta else 'N/A'}",
            f"Velocidad: {vehiculo.velocidad_actual:.2f} px/frame",
            "Ruta: "
        ]

        # Render info base
        for i, linea in enumerate(lineas):
            texto = fuente.render(linea, True, NEGRO)
            pantalla.blit(texto, (x + 10, y + 10 + i * 25))

        # Render ruta con salto de línea
        ruta_render_y = y + 10 + len(lineas) * 25
        palabras = ruta_str.split(" ")
        linea_actual = ""

        for palabra in palabras:
            prueba = f"{linea_actual} {palabra}".strip()
            if fuente.size(prueba)[0] <= ancho - 20:
                linea_actual = prueba
            else:
                texto = fuente.render(linea_actual, True, NEGRO)
                pantalla.blit(texto, (x + 10, ruta_render_y))
                ruta_render_y += 20
                linea_actual = palabra

        # Render última línea si quedó algo
        if linea_actual:
            texto = fuente.render(linea_actual, True, NEGRO)
            pantalla.blit(texto, (x + 10, ruta_render_y))

    def alternar_mostrar_recomendaciones(self):
        self._mostrar_recomendaciones = not self._mostrar_recomendaciones
        if self._mostrar_recomendaciones:
            self._puntos_criticos_guardados = self._controller.obtener_aristas_criticas()

    def _mostrar_recomendaciones_criticas(self, pantalla):
        fuente = pygame.font.Font(None, 16)
        x, y, ancho, alto = 1100, 590, 250, 170
        fondo = pygame.Rect(x, y, ancho, alto)

        pygame.draw.rect(pantalla, (240, 240, 240), fondo)
        pygame.draw.rect(pantalla, NEGRO, fondo, 2)

        aristas = self._puntos_criticos_guardados

        if not aristas:
            lineas = ["No hay rutas críticas."]
        else:
            lineas = ["Rutas congestionadas:"]
            for nombre1, nombre2, peso in aristas:
                lineas.append(f"{nombre1} ↔ {nombre2}: peso = {int(peso)}")

        for i, linea in enumerate(lineas):
            texto = fuente.render(linea, True, NEGRO)
            pantalla.blit(texto, (x + 10, y + 10 + i * 20))

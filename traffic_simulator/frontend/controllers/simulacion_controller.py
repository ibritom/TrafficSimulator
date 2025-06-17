# frontend/controllers/simulacion_controller.py (Patrón MVC)
from traffic_simulator.backend.interfaces.observer_interface import Observer
from traffic_simulator.backend.services.simulacion_facade import SimulacionFacade
from traffic_simulator.backend.factories.vehiculo_factory import VehiculoFactory
import random
import threading
import time
from traffic_simulator.backend.models.nodo import Nodo
from traffic_simulator.frontend.views.nombre_ciudad_popup import NombreCiudadPopup

class SimulacionController(Observer):
    """Controlador principal - Patrón MVC"""

    def __init__(self):
        self._simulacion = SimulacionFacade()
        self._simulacion.agregar_observador(self)
        self._simulacion_activa = False
        self._hilo_simulacion = None
        self._vehiculos = []
        self._modo_actual = "AGREGAR_NODO"
        self._nodo_seleccionado = None
        self._mostrar_rutas = False
        self._velocidad_simulacion = 1.0
        self._view = None  # Se establecerá desde la vista
        self.nodo_origen_dijkstra=None


    def establecer_vista(self, view):
        """Establece la referencia a la vista"""
        self._view = view
        if hasattr(view, '_pantalla'):
            self._pantalla = view._pantalla

    def actualizar(self, evento, datos):
        """Implementación del patrón Observer"""
        if self._view:
            self._view.actualizar_desde_modelo(evento, datos)

    # Métodos de control de la simulación
    def cambiar_modo(self, nuevo_modo):
        """Cambia el modo de interacción"""
        self._modo_actual = nuevo_modo
        self._nodo_seleccionado = None


    def manejar_click(self, x, y, boton='izquierdo'):
        print(f"[Click] Coordenadas: ({x}, {y}) - Modo: {self._modo_actual}")
        """Maneja los clicks del usuario según el modo actual"""
        if self._modo_actual == "AGREGAR_NODO":
            return self._manejar_agregar_nodo(x, y)
        elif self._modo_actual == "CONECTAR_NODOS":
            return self._manejar_conectar_nodos(x, y)
        elif self._modo_actual == "DIJKSTRA":
            return self._manejar_dijkstra(x, y)

    def agregar_carro(self, destino_id: str) -> None:
        """Agrega un vehículo con ruta a un destino específico"""
        if not self._nodo_origen_dijkstra:
            return

        ruta = self._simulacion.obtener_ruta_entre_nodos(
            self._nodo_origen_dijkstra.identificador,
            destino_id
        )

        if ruta:
            vehiculo = VehiculoFactory.crear_vehiculo('normal', ruta)
            self._vehiculos.append(vehiculo)
            self._simulacion.notificar_observadores('vehiculo_agregado', vehiculo)


    def obtener_nodo_por_posicion(self, x: int, y: int) -> Nodo:
        """Wrapper para el método del modelo"""
        return self._simulacion.obtener_nodo_por_posicion(x, y)

    def crear_nodo_con_nombre(self, nombre, x, y):
        """Crea un nodo y lo agrega al modelo"""
        self._simulacion.crear_nodo(nombre, x, y)

    def _manejar_agregar_nodo(self, x, y):
        """Maneja la adición de nodos"""
        print(f"[Agregar Nodo] Llamando a mostrar_popup_nombre_ciudad en ({x}, {y})")
        if self._view:
            self._view.mostrar_popup_nombre_ciudad(x, y)
    def _manejar_conectar_nodos(self, x, y):

        """Maneja la conexión entre nodos"""
        nodo_clickeado = self._simulacion.obtener_nodo_por_posicion(x, y)

        if not nodo_clickeado:
            return False

        if not self._nodo_seleccionado:
            self._nodo_seleccionado = nodo_clickeado
            return True
        else:
            if nodo_clickeado != self._nodo_seleccionado:
                resultado = self._simulacion.conectar_nodos(
                    self._nodo_seleccionado.identificador,
                    nodo_clickeado.identificador
                )
                self._nodo_seleccionado = None
                return resultado
            return False

    def nombre_ya_existe(self, nombre: str) -> bool:
        """Verifica si ya existe un nodo con ese nombre"""
        for nodo in self._simulacion.obtener_todos_los_nodos():
            if nodo.nombre.lower() == nombre.lower():
                return True
        return False

    def _manejar_dijkstra(self, x, y):
        nodo_clickeado = self._simulacion.obtener_nodo_por_posicion(x, y)
        if nodo_clickeado:
            self._simulacion.calcular_rutas_optimas(nodo_clickeado.identificador)
            self._nodo_origen_dijkstra = nodo_clickeado  # <--- Agrega esto
            return True
        return False

    def generar_vehiculos_aleatorios(self, cantidad=5):
        """Genera vehículos con rutas aleatorias"""
        nodos = self._simulacion.obtener_todos_los_nodos()
        if len(nodos) < 2:
            return False

        for _ in range(cantidad):
            origen = random.choice(nodos)
            destino = random.choice(nodos)

            while destino == origen:
                destino = random.choice(nodos)

            ruta = self._simulacion.obtener_ruta_entre_nodos(
                origen.identificador,
                destino.identificador
            )

            if ruta:
                tipo_vehiculo = random.choice(['normal', 'emergencia', 'comercial'])
                vehiculo = VehiculoFactory.crear_vehiculo(tipo_vehiculo, ruta)
                self._vehiculos.append(vehiculo)

        return True

    def actualizar_simulacion(self):
        """Actualiza la simulación (llamado en cada frame)"""
        # Mover vehículos activos
        for vehiculo in self._vehiculos:
            if vehiculo.activo:
                vehiculo.mover()

        # Limpiar vehículos inactivos
        self._vehiculos = [v for v in self._vehiculos if v.activo]

    def obtener_estado_actual(self):
        """Obtiene el estado actual de la simulación"""
        return {
            'nodos': self._simulacion.obtener_todos_los_nodos(),
            'vehiculos': self._vehiculos,
            'modo': self._modo_actual,
            'nodo_seleccionado': self._nodo_seleccionado,
            'mostrar_rutas': self._mostrar_rutas
        }

    def alternar_visualizacion_rutas(self):
        """Alterna la visualización de rutas"""
        self._mostrar_rutas = not self._mostrar_rutas

    def reiniciar_simulacion(self):
        """Reinicia la simulación completa"""
        self._vehiculos.clear()
        self._simulacion.reiniciar_simulacion()
        self._nodo_seleccionado = None

print("=== REFACTORIZACIÓN COMPLETA ===")
print("✓ Interfaces implementadas (Principio DIP)")
print("✓ Patrón Strategy para algoritmos")
print("✓ Patrón Observer para comunicación")
print("✓ Patrón Facade para simplificar el backend")
print("✓ Patrón Factory para crear vehículos")
print("✓ Patrón MVC para separar responsabilidades")
print("✓ Principios SOLID aplicados")
print("✓ Encapsulación mejorada")
print("✓ Separación clara Frontend/Backend")


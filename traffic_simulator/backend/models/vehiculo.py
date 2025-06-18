# backend/models/vehiculo.py (Jerarquía de herencia)
import math


class Vehiculo:
    """Clase base para vehículos - Principio LSP"""

    def __init__(self, ruta, velocidad=2):
        self._ruta = ruta
        self._velocidad = velocidad
        self._posicion_actual = 0
        self._pos_x, self._pos_y = ruta[0].coordenadas if ruta else (0, 0)
        self._activo = True
        self._color = (255, 0, 0)  # Rojo por defecto
        self._tipo = 'normal'
        self._arista_actual = None
        self._simulacion = None  # ← se inyectará luego desde el controlador
        self._recalculo_realizado = False  # ← bandera para evitar repetir prints
        self._nodo_destino = ruta[-1] if ruta else None
        self._nodo_origen = ruta[0] if ruta else None
        self._velocidad_actual = velocidad

    @property
    def tipo(self):
        return self._tipo

    @property
    def velocidad(self):
        return self._velocidad

    @property
    def activo(self):
        return self._activo

    @property
    def ruta(self):
        return self.ruta
    @property
    def posicion(self):
        return (self._pos_x, self._pos_y)

    @property
    def color(self):
        return self._color

    @property
    def nodo_destino(self):
        return self._nodo_destino

    @property
    def velocidad_actual(self):
        return self._velocidad_actual

    def mover(self):
        """Mueve el vehículo, considerando bloqueos y congestión"""
        if not self._activo or self._posicion_actual + 1 >= len(self._ruta):
            return

        actual = self._ruta[self._posicion_actual]
        destino = self._ruta[self._posicion_actual + 1]

        dx = destino.x - self._pos_x
        dy = destino.y - self._pos_y
        distancia = math.hypot(dx, dy)

        # Obtener la arista
        arista = None
        if self._simulacion:
            arista = self._simulacion._grafo.obtener_arista(actual.identificador, destino.identificador)

        # Ingreso a nueva arista
        if self._arista_actual is None and arista:
            arista.vehiculos_actuales += 1
            self._arista_actual = arista

        if arista and (not arista.activa or arista.bloqueada or arista.peso == float('inf')):
            if not self._recalculo_realizado:
                print(
                    f"[Bloqueado] Vehículo detenido entre {actual.nombre} → {destino.nombre} (bloqueada: {arista.bloqueada}, activa: {arista.activa}, peso: {arista.peso})")
                self.recalcular_ruta()
                self._recalculo_realizado = True  # evita prints repetidos
            return

        # Reducción de velocidad por congestión
        velocidad_ajustada = self._velocidad
        if arista:
            from traffic_simulator.backend.services.calculador_peso import CalculadorPeso
            calculador = CalculadorPeso()
            peso_base = calculador.calcular_peso_base(actual, destino)
            peso_dinamico = calculador.calcular_peso_dinamico(actual, destino, arista)

            ratio = peso_dinamico / peso_base if peso_base > 0 else 1
            if ratio > 1:
                velocidad_ajustada = self._velocidad / ratio  # Más congestión → más lento

        # Asignar la velocidad ajustada al atributo del vehículo
        self._velocidad_actual = velocidad_ajustada

        # Movimiento
        if distancia < velocidad_ajustada:
            self._pos_x, self._pos_y = destino.x, destino.y
            self._posicion_actual += 1

            # Salir de la arista
            if self._arista_actual:
                self._arista_actual.vehiculos_actuales = max(0, self._arista_actual.vehiculos_actuales - 1)
                self._arista_actual = None

            if self._posicion_actual + 1 >= len(self._ruta):
                self._activo = False
        else:
            self._pos_x += velocidad_ajustada * dx / distancia
            self._pos_y += velocidad_ajustada * dy / distancia

    def obtener_prioridad(self):
        """Obtiene la prioridad del vehículo para intersecciones"""
        return 1

    def establecer_contexto_simulacion(self, simulacion):
        """Permite al vehículo acceder a la simulación para notificar paso por aristas"""
        self._simulacion = simulacion

    def recalcular_ruta(self):
        """Recalcula una ruta alternativa evitando aristas bloqueadas desde el nodo actual"""
        if not self._simulacion or not self._nodo_destino or self._posicion_actual >= len(self._ruta):
            return False

        nodo_actual = self._ruta[self._posicion_actual]
        self._simulacion.actualizar_pesos_dinamicos()

        nueva_ruta = self._simulacion._algoritmo_ruta.calcular_ruta_optima(
            self._simulacion._grafo,
            nodo_actual.identificador,
            self._nodo_destino.identificador
        )

        if nueva_ruta and len(nueva_ruta) > 1:
            # Verificación movida dentro de obtener_vecinos: no es necesaria aquí
            print(
                f"[Recalculo] Nueva ruta encontrada para vehículo de {nodo_actual.nombre} a {self._nodo_destino.nombre}")
            ruta_str = " → ".join(n.nombre for n in nueva_ruta)
            print(f"[Recalculo] Ruta nueva: {ruta_str}")

            self._ruta = nueva_ruta
            self._posicion_actual = 0
            self._pos_x, self._pos_y = self._ruta[0].coordenadas
            self._arista_actual = None
            return True

        print(f"[Recalculo] No se encontró ruta alternativa desde {nodo_actual.nombre}")
        self._activo = False
        return False


class VehiculoEmergencia(Vehiculo):
    """Vehículo de emergencia con mayor prioridad"""

    def __init__(self, ruta, velocidad=4):
        super().__init__(ruta, velocidad)
        self._color = (0, 0, 255)  # Azul para emergencia
        self._tipo = 'emergencia'  # En VehiculoEmergencia

    def obtener_prioridad(self):
        return 3  # Mayor prioridad


class VehiculoComercial(Vehiculo):
    """Vehículo comercial más lento"""

    def __init__(self, ruta, velocidad=1.5):
        super().__init__(ruta, velocidad)
        self._tipo = 'comercial'  # En VehiculoComercial

        self._color = (0, 255, 0)  # Verde para comercial

    def obtener_prioridad(self):
        return 0.5  # Menor prioridad



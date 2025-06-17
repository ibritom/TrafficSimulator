# backend/services/calculador_peso.py
import math
from traffic_simulator.backend.interfaces.calculador_peso_interface import CalculadorPesoInterface


class CalculadorPeso(CalculadorPesoInterface):
    def __init__(self):
        self.hora_actual = 8.0
        self.dia_semana = 1
        self.velocidad_simulacion = 1.0

        self.factores_horarios = [
            0.8, 0.7, 0.6, 0.6, 0.7, 0.9,
            1.4, 1.8, 2.2, 1.6, 1.2, 1.3,
            1.4, 1.3, 1.2, 1.1, 1.2, 1.8,
            2.0, 1.6, 1.3, 1.1, 1.0, 0.9
        ]

        self.factores_semanales = {
            1: 1.0, 2: 1.1, 3: 1.1, 4: 1.1,
            5: 1.2, 6: 0.8, 7: 0.7
        }

    def calcular_peso_base(self, origen, destino):
        distancia = math.sqrt((origen.x - destino.x) ** 2 + (origen.y - destino.y) ** 2)
        return max(1, int(distancia / 10))

    def calcular_peso_dinamico(self, origen, destino, arista=None):
        peso_base = self.calcular_peso_base(origen, destino)
        if arista is None:
            return peso_base

        # Lógica de cálculo dinámico
        hora_index = int(self.hora_actual) % 24
        factor_temporal = self.factores_horarios[hora_index] * self.factores_semanales.get(self.dia_semana, 1.0)

        vehiculos = getattr(arista, 'vehiculos_actuales', 0)
        capacidad = getattr(arista, 'capacidad', 10)
        ratio = vehiculos / capacidad if capacidad > 0 else 1.0

        if ratio <= 0.5:
            factor_congestion = 1.0 + ratio * 0.4
        elif ratio <= 0.8:
            factor_congestion = 1.2 + (ratio - 0.5) * 1.0
        else:
            factor_congestion = 1.5 + (ratio - 0.8) * 3.0

        penalizacion = 0
        if getattr(arista, 'accidentes', 0): penalizacion += arista.accidentes * 15
        if getattr(arista, 'construcciones', 0): penalizacion += arista.construcciones * 8
        if getattr(arista, 'operativos', 0): penalizacion += arista.operativos * 5
        if getattr(arista, 'clima_adverso', False): penalizacion += 10
        if getattr(arista, 'bloqueada', False): return 999999

        return max(1, int(peso_base * factor_temporal * factor_congestion + penalizacion))
import math
#import time


class CalculadorPeso:
    def __init__(self):
        # Configuración de la simulación
        self.hora_actual = 8.0  # Hora del día (8:00 AM por defecto)
        self.dia_semana = 1  # 1=Lunes, 7=Domingo
        self.velocidad_simulacion = 1.0  # Multiplicador de velocidad

        # Factores de congestión por hora (24 horas)
        self.factores_horarios = [
            0.8, 0.7, 0.6, 0.6, 0.7, 0.9,  # 0-5 AM (madrugada)
            1.4, 1.8, 2.2, 1.6, 1.2, 1.3,  # 6-11 AM (mañana - rush)
            1.4, 1.3, 1.2, 1.1, 1.2, 1.8,  # 12-17 PM (tarde)
            2.0, 1.6, 1.3, 1.1, 1.0, 0.9  # 18-23 PM (noche - rush)
        ]

        # Factores por día de la semana
        self.factores_semanales = {
            1: 1.0,  # Lunes
            2: 1.1,  # Martes
            3: 1.1,  # Miércoles
            4: 1.1,  # Jueves
            5: 1.2,  # Viernes
            6: 0.8,  # Sábado
            7: 0.7  # Domingo
        }

    def calcular_peso_base(self, origen, destino):
        """Calcula el peso base basado en la distancia euclidiana"""
        distancia = math.sqrt((origen.x - destino.x) ** 2 + (origen.y - destino.y) ** 2)
        return max(1, int(distancia / 10))  # Escalar la distancia

    def obtener_factor_temporal(self):
        """Obtiene el factor de congestión basado en la hora y día"""
        hora_index = int(self.hora_actual) % 24
        factor_horario = self.factores_horarios[hora_index]
        factor_semanal = self.factores_semanales.get(self.dia_semana, 1.0)
        return factor_horario * factor_semanal

    def calcular_factor_congestion(self, arista):
        """Calcula el factor de congestión basado en vehículos presentes"""
        vehiculos_actuales = arista.vehiculos_actuales if hasattr(arista, 'vehiculos_actuales') else 0
        capacidad = arista.capacidad if hasattr(arista, 'capacidad') else 10

        if capacidad == 0:
            return 1.0

        ratio_congestion = vehiculos_actuales / capacidad

        # Función cuadrática para simular congestión realista
        if ratio_congestion <= 0.5:
            return 1.0 + ratio_congestion * 0.4  # Crecimiento lento hasta 50%
        elif ratio_congestion <= 0.8:
            return 1.2 + (ratio_congestion - 0.5) * 1.0  # Crecimiento medio
        else:
            return 1.5 + (ratio_congestion - 0.8) * 3.0  # Crecimiento exponencial

    def obtener_penalizacion_eventos(self, arista):
        """Calcula penalizaciones por eventos especiales"""
        penalizacion = 0

        # Accidentes
        if hasattr(arista, 'accidentes') and arista.accidentes:
            penalizacion += arista.accidentes * 15

        # Construcciones/trabajos en la vía
        if hasattr(arista, 'construcciones') and arista.construcciones:
            penalizacion += arista.construcciones * 8

        # Operativos policiales
        if hasattr(arista, 'operativos') and arista.operativos:
            penalizacion += arista.operativos * 5

        # Clima adverso
        if hasattr(arista, 'clima_adverso') and arista.clima_adverso:
            penalizacion += 10

        # Ruta bloqueada completamente
        if hasattr(arista, 'bloqueada') and arista.bloqueada:
            return 999999  # Peso infinito

        return penalizacion

    def calcular_peso_dinamico(self, origen, destino, arista=None):
        """Calcula el peso dinámico final de una arista"""
        # Peso base (distancia)
        peso_base = self.calcular_peso_base(origen, destino)

        # Si no hay información de arista, usar solo peso base
        if arista is None:
            return peso_base

        # Factor temporal (hora del día + día de la semana)
        factor_temporal = self.obtener_factor_temporal()

        # Factor de congestión (basado en vehículos)
        factor_congestion = self.calcular_factor_congestion(arista)

        # Penalizaciones por eventos
        penalizacion_eventos = self.obtener_penalizacion_eventos(arista)

        # Si la ruta está bloqueada, retornar peso infinito
        if penalizacion_eventos >= 999999:
            return 999999

        # Cálculo final
        peso_final = peso_base * factor_temporal * factor_congestion + penalizacion_eventos

        return max(1, int(peso_final))  # Asegurar que sea al menos 1

    def obtener_color_congestion(self, peso_base, peso_actual):
        """Obtiene el color que representa el nivel de congestión"""
        if peso_actual >= 999999:
            return "BLOQUEADA"  # Negro

        ratio = peso_actual / peso_base if peso_base > 0 else 1

        if ratio <= 1.2:
            return "LIBRE"  # Verde
        elif ratio <= 1.5:
            return "LIGERA"  # Amarillo claro
        elif ratio <= 2.0:
            return "MODERADA"  # Amarillo
        elif ratio <= 3.0:
            return "ALTA"  # Naranja
        else:
            return "CRITICA"  # Rojo

    def obtener_estadisticas_congestion(self, peso_base, peso_actual):
        """Obtiene estadísticas detalladas de congestión"""
        if peso_actual >= 999999:
            return {
                'estado': 'BLOQUEADA',
                'ratio': float('inf'),
                'incremento_tiempo': float('inf'),
                'nivel': 5
            }

        ratio = peso_actual / peso_base if peso_base > 0 else 1
        incremento_porcentaje = (ratio - 1) * 100

        if ratio <= 1.2:
            estado, nivel = 'LIBRE', 0
        elif ratio <= 1.5:
            estado, nivel = 'LIGERA', 1
        elif ratio <= 2.0:
            estado, nivel = 'MODERADA', 2
        elif ratio <= 3.0:
            estado, nivel = 'ALTA', 3
        else:
            estado, nivel = 'CRITICA', 4

        return {
            'estado': estado,
            'ratio': ratio,
            'incremento_tiempo': incremento_porcentaje,
            'nivel': nivel
        }

    def avanzar_tiempo(self, minutos=15):
        """Avanza el tiempo de simulación"""
        self.hora_actual += (minutos / 60.0) * self.velocidad_simulacion
        if self.hora_actual >= 24:
            self.hora_actual -= 24
            self.dia_semana = (self.dia_semana % 7) + 1

    def establecer_hora(self, hora, dia=None):
        """Establece la hora actual de la simulación"""
        self.hora_actual = max(0, min(23.99, hora))
        if dia is not None:
            self.dia_semana = max(1, min(7, dia))

    def obtener_tiempo_formateado(self):
        """Obtiene la hora actual formateada"""
        hora = int(self.hora_actual)
        minutos = int((self.hora_actual - hora) * 60)
        dias = ['', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        return f"{dias[self.dia_semana]} {hora:02d}:{minutos:02d}"


class AristaConTrafico:
    """Clase auxiliar para representar aristas con información de tráfico"""

    def __init__(self, origen, destino, peso_base):
        self.origen = origen
        self.destino = destino
        self.peso_base = peso_base
        self.vehiculos_actuales = 0
        self.capacidad = 10  # Capacidad por defecto
        self.accidentes = 0
        self.construcciones = 0
        self.operativos = 0
        self.clima_adverso = False
        self.bloqueada = False
        self.peso_actual = peso_base
        self.historial_pesos = []

    def agregar_vehiculo(self):
        """Agrega un vehículo a la arista"""
        self.vehiculos_actuales += 1

    def remover_vehiculo(self):
        """Remueve un vehículo de la arista"""
        self.vehiculos_actuales = max(0, self.vehiculos_actuales - 1)

    def establecer_evento(self, tipo_evento, cantidad=1):
        """Establece un evento en la arista"""
        if tipo_evento == 'accidente':
            self.accidentes = cantidad
        elif tipo_evento == 'construccion':
            self.construcciones = cantidad
        elif tipo_evento == 'operativo':
            self.operativos = cantidad
        elif tipo_evento == 'clima':
            self.clima_adverso = cantidad > 0
        elif tipo_evento == 'bloqueo':
            self.bloqueada = cantidad > 0

    def limpiar_eventos(self):
        """Limpia todos los eventos de la arista"""
        self.accidentes = 0
        self.construcciones = 0
        self.operativos = 0
        self.clima_adverso = False
        self.bloqueada = False

    def actualizar_peso(self, calculador_peso):
        """Actualiza el peso actual usando el calculador"""
        nuevo_peso = calculador_peso.calcular_peso_dinamico(
            self.origen, self.destino, self
        )

        # Guardar en historial si cambió significativamente
        if abs(nuevo_peso - self.peso_actual) > 2:
            self.historial_pesos.append({
                'tiempo': calculador_peso.obtener_tiempo_formateado(),
                'peso_anterior': self.peso_actual,
                'peso_nuevo': nuevo_peso
            })

            # Mantener solo los últimos 10 cambios
            if len(self.historial_pesos) > 10:
                self.historial_pesos.pop(0)

        self.peso_actual = nuevo_peso
        return nuevo_peso
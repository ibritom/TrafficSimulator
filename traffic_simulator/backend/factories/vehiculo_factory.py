#(Patrón Factory)
from traffic_simulator.backend.models.vehiculo import Vehiculo, VehiculoEmergencia, VehiculoComercial


class VehiculoFactory:
    """Patrón Factory - Crea diferentes tipos de vehículos"""

    @staticmethod
    def crear_vehiculo(tipo,ruta, velocidad_base=1):
        """Crea un vehículo según el tipo especificado"""
        if tipo == 'normal':
            return Vehiculo(ruta, velocidad_base)
        elif tipo == 'emergencia':
            return VehiculoEmergencia(ruta, velocidad_base * 2)
        elif tipo == 'comercial':
            return VehiculoComercial(ruta, velocidad_base * 0.7)
        else:
            raise ValueError(f"Tipo de vehículo desconocido: {tipo}")


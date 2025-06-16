#!/usr/bin/env python3
"""
Traffic Simulator - Proyecto #3
Instituto Tecnológico de Costa Rica
Escuela de Ingeniería en Computadores
Algoritmos y Estructuras de Datos I (CE 1103)

Simulador de tráfico vehicular con algoritmos de grafos
"""

import sys
import pygame
from traffic_simulator.frontend.app import TrafficSimulatorApp


def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    try:
        import pygame
        print("✓ PyGame instalado correctamente")
        return True
    except ImportError:
        print("✗ Error: PyGame no está instalado")
        print("Instale con: pip install pygame")
        return False


def mostrar_banner():
    """Muestra el banner de bienvenida"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    TRAFFIC SIMULATOR                         ║
║                                                              ║
║          Instituto Tecnológico de Costa Rica                 ║
║        Algoritmos y Estructuras de Datos I (CE 1103)         ║
║                                                              ║
║  Simulador de tráfico vehicular con algoritmos de grafos     ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Función principal del programa"""
    mostrar_banner()

    if not verificar_dependencias():
        sys.exit(1)

    try:
        app = TrafficSimulatorApp()
        app.ejecutar()
    except KeyboardInterrupt:
        print("\nAplicación finalizada por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        pygame.quit()


if __name__ == "__main__":
    # Manejo básico de argumentos
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("Uso: python main.py [opciones]")
        print("Opciones:")
        print("  -h, --help  Muestra este mensaje")
        sys.exit(0)

    main()
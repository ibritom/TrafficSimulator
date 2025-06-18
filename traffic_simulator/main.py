import sys
import pygame
from traffic_simulator.frontend.app import TrafficSimulatorApp





def mostrar_banner():
    """Muestra el banner de bienvenida"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    TRAFFIC SIMULATOR                         ║
║                                                              ║
║          Instituto Tecnológico de Costa Rica                 ║
║        Algoritmos y Estructuras de Datos I (CE 1103)         ║
║                                                              ║
║                         Integrantes:                         ║
║                  Iván Ignacio Brito Medina                   ║
║                  Jeison Johel Picado Picado                  ║
║                   José Fabio Ruiz Morales                    ║
║               Antony Javier Hernández Castillo               ║
║                                                              ║
║  Simulador de tráfico vehicular con algoritmos de grafos     ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Función principal del programa"""
    mostrar_banner()



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
    main()
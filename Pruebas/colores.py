from diccionario import *

# Cache para evitar inicializar cada vez
_colores_cache = None

# Crear una instancia del diccionario personalizado con los colores
def inicializar_colores():
    colores = DiccionarioPersonalizado()

    colores.agregar("negro", (0, 0, 0))
    colores.agregar("blanco", (255, 255, 255))
    colores.agregar("rojo", (255, 0, 0))
    colores.agregar("verde", (0, 255, 0))
    colores.agregar("azul", (0, 0, 255))
    colores.agregar("amarillo", (255, 255, 0))
    colores.agregar("cian", (0, 255, 255))
    colores.agregar("magenta", (255, 0, 255))
    colores.agregar("gris", (128, 128, 128))
    colores.agregar("gris claro", (200, 200, 200))
    colores.agregar("gris oscuro", (64, 64, 64))
    colores.agregar("naranja", (255, 165, 0))
    colores.agregar("rosa", (255, 192, 203))
    colores.agregar("marrón", (139, 69, 19))
    colores.agregar("violeta", (238, 130, 238))
    colores.agregar("lila", (200, 162, 200))
    colores.agregar("turquesa", (64, 224, 208))
    colores.agregar("oliva", (128, 128, 0))
    colores.agregar("dorado", (255, 215, 0))
    colores.agregar("plateado", (192, 192, 192))
    colores.agregar("vino", (128, 0, 32))
    colores.agregar("salmon", (250, 128, 114))
    colores.agregar("aguamarina", (127, 255, 212))
    colores.agregar("lavanda", (230, 230, 250))
    colores.agregar("azul marino", (0, 0, 128))
    colores.agregar("verde lima", (50, 205, 50))
    colores.agregar("menta", (152, 255, 152))

    return colores

# Función que devuelve el color RGB desde el nombre usando el diccionario personalizado
def color_pygame(nombre_color):
    nombre_color = nombre_color.strip().lower()
    global _colores_cache
    if _colores_cache is None:
        _colores_cache = inicializar_colores()

    if _colores_cache.contiene(nombre_color):
        return _colores_cache.obtener(nombre_color)
    else:
        raise ValueError(f"Color desconocido: '{nombre_color}'. Usa uno de: {[clave for clave, _ in colores.elementos()]}")

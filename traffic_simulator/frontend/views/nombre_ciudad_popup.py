# frontend/views/nombre_ciudad_popup.py
import pygame



class NombreCiudadPopup:
    def __init__(self, pantalla, controller, x, y):
        print(f"[Popup Init] Coordenadas del nuevo nodo: ({x}, {y})")

        self.pantalla = pantalla
        self.controller = controller
        self.x = x
        self.y = y
        self.input_text = ""
        self.font = pygame.font.Font(None, 32)
        self.activo = True
        self.error = ""

        self.rect_input = pygame.Rect(500, 300, 300, 40)
        self.boton_ok = pygame.Rect(520, 360, 100, 40)
        self.boton_cancelar = pygame.Rect(650, 360, 100, 40)

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                print(f"[Popup] Tecla presionada: {evento.unicode}")
                self._confirmar()
            elif evento.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < 20:
                    self.input_text += evento.unicode
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if self.boton_ok.collidepoint(evento.pos):
                self._confirmar()
            elif self.boton_cancelar.collidepoint(evento.pos):
                self.activo = False

    def _confirmar(self):
        nombre = self.input_text.strip()
        if not nombre:
            self.error = "El nombre no puede estar vacío"
        elif self.controller.nombre_ya_existe(nombre):
            self.error = "El nombre ya existe"
        else:
            self.controller.crear_nodo_con_nombre(nombre, self.x, self.y)
            self.activo = False

    def dibujar(self):
        print("[Popup] Dibujando en pantalla")
        pygame.draw.rect(self.pantalla, (200, 200, 200), (450, 250, 400, 180))
        pygame.draw.rect(self.pantalla, (255, 255, 255), self.rect_input)
        pygame.draw.rect(self.pantalla, (0, 255, 0), self.boton_ok)
        pygame.draw.rect(self.pantalla, (255, 0, 0), self.boton_cancelar)

        texto = self.font.render(self.input_text, True, (0, 0, 0))
        self.pantalla.blit(texto, (self.rect_input.x + 5, self.rect_input.y + 5))

        ok_text = self.font.render("OK", True, (0, 0, 0))
        cancel_text = self.font.render("Cancelar", True, (0, 0, 0))
        self.pantalla.blit(ok_text, (self.boton_ok.x + 10, self.boton_ok.y + 5))
        self.pantalla.blit(cancel_text, (self.boton_cancelar.x + 10, self.boton_cancelar.y + 5))

        prompt = self.font.render("Nombre de la ciudad:", True, (0, 0, 0))
        self.pantalla.blit(prompt, (self.rect_input.x, self.rect_input.y - 30))

        if self.error:
            error_text = self.font.render(self.error, True, (255, 0, 0))
            self.pantalla.blit(error_text, (self.rect_input.x, self.rect_input.y + 50))

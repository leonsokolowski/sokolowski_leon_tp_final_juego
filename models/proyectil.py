import pygame
from auxiliar.constantes import ANCHO_VENTANA, ALTO_VENTANA

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, img_path_player = False):
        super().__init__()
        self.__load_img(img_path_player)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.direction = direction

    def __load_img(self, img_path: bool):
        if img_path:
            self.image = pygame.image.load(r"assets\img\player\proyectil\tajo_espada.png")
        else: 
            self.image = pygame.image.load(r"assets\img\enemy\proyectil\tempano.png")

    def update(self):
        
        match self.direction:
            case "right":
                self.rect.x += 20
                if self.rect.x >= ANCHO_VENTANA:
                    self.kill()
            case "left":
                self.rect.x -= 20
                if self.rect.x <= 0:
                    self.kill()
            case "up":
                self.rect.y += 20
                if self.rect.y >= ALTO_VENTANA:
                    self.kill()
            case "down":
                self.rect.y -= 20
                if self.rect.y <= 0:
                    self.kill()
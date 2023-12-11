import pygame as pg
from auxiliar.constantes import ANCHO_VENTANA, ALTO_VENTANA, DEBUG

class Proyectil(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, dict_configs_nivel : dict, velocidad_proyectil : int, flip : bool = False): 
        super().__init__()
        
        self.config_proyectil = dict_configs_nivel
        self.flip = flip
        self.__load_img()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.direction = direction
        self.velocidad_proyectil = velocidad_proyectil
        

    def __load_img(self):
        self.image = pg.image.load(self.config_proyectil.get("proyectil"))
        if self.flip:
            self.image = pg.transform.flip(self.image, True, False)

    def update(self, screen: pg.surface.Surface):
        
        match self.direction:
            case "right":
                self.rect.x += self.velocidad_proyectil
                if self.rect.x >= ANCHO_VENTANA:
                    self.kill()
            case "left":
                self.rect.x -= self.velocidad_proyectil
                if self.rect.x <= 0:
                    self.kill()
            case "up":
                self.rect.y += 15
                if self.rect.y >= ALTO_VENTANA:
                    self.kill()
            # case "down":
            #     self.rect.y -= 20
            #     if self.rect.y <= 0:
            #         self.kill()
        
        self.draw(screen)
    
    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, "red", self.rect)
            
        screen.blit(self.image, self.rect)
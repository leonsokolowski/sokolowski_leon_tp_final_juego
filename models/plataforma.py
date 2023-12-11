import pygame as pg
from auxiliar.constantes import (DEBUG)

class Plataforma(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y, ancho, alto, dict_configs_nivel : dict):
        super().__init__()
        
        self.config_plataforma = dict_configs_nivel.get("plataforma")
        self.sprite_plataforma = self.config_plataforma.get("sprites")
        self.imagen_plataforma = pg.image.load(self.sprite_plataforma.get("image"))
        self.imagen_plataforma = pg.transform.scale(self.imagen_plataforma, (ancho, alto))
        self.rect = self.imagen_plataforma.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        self.rect_limite_derecha = pg.Rect(self.rect.x + ancho - 10, self.rect.y - 35, 10, 60)
        self.rect_limite_izquierda = pg.Rect(self.rect.x, self.rect.y - 35, 10, 60)
        
        
    def update(self, screen : pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen, "red", self.rect)
            pg.draw.rect(screen, "green", self.rect_limite_derecha)
            pg.draw.rect(screen, "green", self.rect_limite_izquierda)

        self.draw(screen)

    
    def draw(self, screen : pg.surface.Surface):
        screen.blit(self.imagen_plataforma,self.rect)
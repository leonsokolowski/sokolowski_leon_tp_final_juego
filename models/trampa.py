import pygame as pg
from auxiliar.constantes import (DEBUG)

class Trampa(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y, ancho, alto, dict_configs_nivel : dict):
        super().__init__()
        
        self.config_trampa = dict_configs_nivel.get("trampa")
        self.sprite_trampa = self.config_trampa.get("sprites")
        self.imagen_trampa = pg.image.load(self.sprite_trampa.get("image"))
        self.imagen_trampa = pg.transform.scale(self.imagen_trampa, (ancho, alto))
        self.rect = self.imagen_trampa.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        
        
    def update(self, screen : pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen, "red", self.rect)

        self.draw(screen)
    
    def draw(self, screen : pg.surface.Surface):
        screen.blit(self.imagen_trampa,self.rect)
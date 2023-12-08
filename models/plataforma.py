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
        #self.rect_top_platform = pg.Rect(self.rect.x, self.rect.y - 20, self.rect.w, 5)
        
        
    def update(self, screen : pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen, "red", self.rect)

        self.draw(screen)

        # if(DEBUG):
        #     pg.draw.rect(screen,"red",self.rect_top_platform)
    
    def draw(self, screen : pg.surface.Surface):
        screen.blit(self.imagen_plataforma,self.rect)
        #screen.blit(self.imagen_plataforma, self.rect_top_platform )
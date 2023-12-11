import pygame as pg
from auxiliar.constantes import (DEBUG)

class Vacio(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y, ancho, alto):
        super().__init__()
        
        self.imagen_vacio = pg.image.load("assets/img/vacio/vacio.png")
        self.imagen_vacio = pg.transform.scale(self.imagen_vacio, (ancho, alto))
        self.rect = self.imagen_vacio.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        self.rect_hitbox = pg.Rect(self.rect.x, self.rect.y + 60, self.rect.width, self.rect.height/2)
        
    def update(self, screen : pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen, "green", self.rect)
            pg.draw.rect(screen, "red", self.rect_hitbox)

        self.draw(screen)
    
    def draw(self, screen : pg.surface.Surface):
        screen.blit(self.imagen_vacio,self.rect)
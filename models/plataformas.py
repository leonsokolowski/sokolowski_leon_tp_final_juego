import pygame as pg
from auxiliar.constantes import (ANCHO_VENTANA, ALTO_VENTANA,DEBUG)

class Plataforma(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y, ancho, alto):
        super().__init__()
        
        self.imagen_plataforma = pg.image.load(r"assets\img\plataforma\plataforma.png")
        self.imagen_plataforma = pg.transform.scale(self.imagen_plataforma, (ancho, alto))
        self.rect = self.imagen_plataforma.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        self.rect_ground_collition = pg.Rect(self.rect.x, self.rect.y, self.rect.w, 5)
        
        
    def update(self, screen : pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen, "red", self.rect)

        # screen.blit(self.imagen_plataforma ,self.rect)
        # print("Estoy imprimiendo ", self.rect)
        self.draw(screen)

        if(DEBUG):
            pg.draw.rect(screen,"green",self.rect_ground_collition)
    
    def draw(self, screen : pg.surface.Surface):
        screen.blit(self.imagen_plataforma ,self.rect)
        print("Estoy imprimiendo ", self.rect)

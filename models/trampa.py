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
        self.rect_hitbox = pg.Rect(self.rect.x + 35, self.rect.y + 20, self.rect.width - 85, self.rect.height - 45)
        self.rect_hitbox_izquierda = pg.Rect(self.rect_hitbox.x, self.rect_hitbox.y, self.rect_hitbox.width - 85, self.rect_hitbox.height)
        self.rect_hitbox_derecha = pg.Rect(self.rect_hitbox.x + 90, self.rect_hitbox.y, self.rect_hitbox.width - 85, self.rect_hitbox.height)
        
        self.collide_player = False
        self.ready = False
        self.tiempo_damage = 0
        self.recibir_damage_cooldown = 1000
        
    def hacer_damage(self) -> bool:
        if self.collide_player and self.ready:
            damage = True
            self.ready = False
            self.tiempo_damage = pg.time.get_ticks()
        else:
            damage = False
        return damage
    
    def cooldown_damage(self):
        if not self.ready:
            self.collide_player = False
            current_time = pg.time.get_ticks()
            if current_time - self.tiempo_damage >= self.recibir_damage_cooldown:
                self.ready = True
        
    def update(self, screen : pg.surface.Surface):
        if(DEBUG):
            pg.draw.rect(screen, "red", self.rect_hitbox)
            pg.draw.rect(screen, "green", self.rect_hitbox_derecha)
            pg.draw.rect(screen, "green", self.rect_hitbox_izquierda)
            

        self.draw(screen)
        self.cooldown_damage()
    
    def draw(self, screen : pg.surface.Surface):
        screen.blit(self.imagen_trampa,self.rect)
import pygame as pg
from auxiliar.constantes import DEBUG
from auxiliar.animar_sprite import SurfaceManager as sf

class Fruta(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y, dict_configs_nivel : dict, frame_rate = 70):
        super().__init__()
        
        self.config_fruta = dict_configs_nivel.get("fruta")
        #animacion
        self.sprite_fruta = self.config_fruta.get("sprites")
        self.__main = sf.get_surface_from_spritesheeet(self.sprite_fruta.get("main"), 17, 1)
        self.__fruit_animation_time = 0
        self.__actual_frame_index = 0
        self.__actual_animation = self.__main
        self.__actual_image_animation = self.__actual_animation[self.__actual_frame_index]
        self.__frame_rate = frame_rate
        #posicion
        self.rect = self.__actual_image_animation.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        
    def do_animation(self, delta_ms):
        self.__fruit_animation_time += delta_ms
        if self.__fruit_animation_time >= self.__frame_rate:
            self.__fruit_animation_time = 0
            if self.__actual_frame_index < len(self.__actual_animation) - 1:
                self.__actual_frame_index += 1
            else:
                self.__actual_frame_index = 0
                
    def update(self, delta_ms, screen: pg.surface.Surface):
        self.do_animation(delta_ms)
        self.draw(screen)
    
    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, "red", self.rect)
        self.__actual_image_animation = self.__actual_animation[self.__actual_frame_index]
        screen.blit(self.__actual_image_animation, self.rect)
        
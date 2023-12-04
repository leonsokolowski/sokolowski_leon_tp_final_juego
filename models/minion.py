from auxiliar.animar_sprite import SurfaceManager as sf
import pygame as pg
from auxiliar.constantes import ANCHO_VENTANA, ALTO_VENTANA, DEBUG
from models.proyectil import Proyectil

class Minion(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y, limite_x, dict_configs_nivel : dict, frame_rate = 100, speed_walk = 6, gravity = 20):
        super().__init__()
        
        self.config_minion = dict_configs_nivel.get("minion")
        #animacion
        self.sprites_minion = self.config_minion.get("sprites")
        self.__iddle_r = sf.get_surface_from_spritesheeet(self.sprites_minion.get("iddle"), 6, 1)
        self.__iddle_l = sf.get_surface_from_spritesheeet(self.sprites_minion.get("iddle"), 6, 1, flip = True)
        self.__walk_r = sf.get_surface_from_spritesheeet(self.sprites_minion.get("walk"), 8, 1)
        self.__walk_l = sf.get_surface_from_spritesheeet(self.sprites_minion.get("walk"), 8, 1, flip = True)
        self.__run_r = sf.get_surface_from_spritesheeet(self.sprites_minion.get("run"), 6, 1)
        self.__run_l = sf.get_surface_from_spritesheeet(self.sprites_minion.get("run"), 6, 1, flip = True)
        self.__shoot_r = sf.get_surface_from_spritesheeet(self.sprites_minion.get("shoot"), 4, 1)
        self.__shoot_l = sf.get_surface_from_spritesheeet(self.sprites_minion.get("shoot"), 4, 1, flip = True)
        self.__minion_animation_time = 0
        self.__actual_frame_index = 0 #Controla el frame de la lista de animaciones en el que nos encontramos
        self.__actual_animation = self.__iddle_r #Al aparecer el personaje aparece con esta animación
        self.__actual_image_animation = self.__actual_animation[self.__actual_frame_index] #Representa la imagen actual de la lista de animaciones que estemos recorriendo
        self.__current_time_animation = 0
        #movimiento
        self.rect = self.__actual_image_animation.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        self.move_y = 0
        self.move_x = 0
        self.__is_looking_right = True
        self.__speed_walk = self.config_minion.get("speed")
        self.__frame_rate = frame_rate
        self.__minion_move_time = 0
        self.__gravity = gravity
        self.__limite_x = limite_x
        self.rect_feet_collition = pg.Rect(self.rect.x + self.rect.w/4, self.rect.y + self.rect.h - 5, self.rect.w/2, 5)
        self.is_landing = False
        self.is_on_land = False
        
        #disparo
        self.projectile_time = 0
        self.projectile_cooldown = self.config_minion.get("shoot_cooldown")
        self.projectile_group = pg.sprite.Group()
        
        self.rect_feet_collition = pg.Rect(self.rect.x + self.rect.w/4, self.rect.y + self.rect.h - 5, self.rect.w/2, 5)

        
    def movimiento(self):  # Ajusta al minion a los limites de la pantalla
        if self.__is_looking_right and self.is_on_land:
            if (self.rect.right + self.__speed_walk ) <= self.__limite_x:
                self.__actual_animation = self.__walk_r
                self.rect.x += self.__speed_walk
                self.rect_feet_collition.x += self.__speed_walk
            else:
                self.__is_looking_right = False
        else:
            if self.rect.left - self.__speed_walk >= 0:
                self.__actual_animation = self.__walk_l
                self.rect.x -= self.__speed_walk
                self.rect_feet_collition.x -= self.__speed_walk
            else:
                self.__is_looking_right = True
        
        self.rect.y += self.__set_borders_limit_y()
        self.rect_feet_collition.y = self.__set_borders_limit_y()

    
    def __set_borders_limit_y(self): #Relacionado al movimiento
        pixels_move = 0
        if self.move_y > 0:
            pixels_move = self.move_y if self.rect.bottom < ALTO_VENTANA else 0 #- self.__actual_image_animation.get_height()
            pixels_move = self.move_y if self.rect_feet_collition.bottom < ALTO_VENTANA else 0 #- self.__actual_image_animation.get_height()
            #print(pixels_move)
        elif self.move_y < 0:
            pixels_move = self.move_y if self.rect.top > 0 else 0
            pixels_move = self.move_y if self.rect_feet_collition.top > 0 else 0
        return pixels_move
    
    @property
    def get_projectiles(self) -> list[Proyectil]:
        return self.projectile_group
    
    def shoot(self):  
        if self.cooldown_to_shoot():
            self.__current_time_animation = pg.time.get_ticks()
            self.shoot_animation()
            self.projectile_group.add(self.create_projectile())
            self.projectile_time = pg.time.get_ticks()
   
    def shoot_animation(self):
        if self.__actual_animation != self.__shoot_r and self.__actual_animation != self.__shoot_l:
                
                if self.__is_looking_right:
                    self.__actual_animation = self.__shoot_r
                else:
                    self.__actual_animation = self.__shoot_l
                #self.__actual_frame_index = 0
                
        
    def create_projectile(self):
        if self.__is_looking_right:
            rect_direction = self.rect.right
            direction = "right"
        else:
            rect_direction = self.rect.left
            direction = "left"   
        return Proyectil(rect_direction, self.rect.centery, direction, self.config_minion, not self.__is_looking_right)

    def cooldown_to_shoot (self) -> bool:
        current_time= pg.time.get_ticks()
        return current_time - self.projectile_time >= self.projectile_cooldown
    
    def do_movement(self, delta_ms):
        self.__minion_move_time += delta_ms
        if self.__minion_move_time >= self.__frame_rate:
            current_time = pg.time.get_ticks()
            self.__minion_move_time = 0
            self.shoot()
            if current_time - self.__current_time_animation > self.config_minion.get("animation_time_cooldown"):
                self.movimiento()
            # if self.rect.y < 525:
            #     self.rect.y += self.__gravity
            if not self.is_on_land:
                self.move_y += self.__gravity
                self.rect_feet_collition.y += self.__gravity
                #self.is_on_land = True
                self.is_landing = True
            else:
                self.move_y = 0

    
    def do_animation(self, delta_ms):
        self.__minion_animation_time += delta_ms
        if self.__minion_animation_time >= self.__frame_rate:
            self.__minion_animation_time = 0
            if self.__actual_frame_index < len(self.__actual_animation) - 1:
                self.__actual_frame_index += 1
            else:
                self.__actual_frame_index = 0
    
    
    
    
    def update(self, delta_ms, screen: pg.surface.Surface):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.projectile_group.update(screen)
        self.draw(screen)
    
    def draw(self, screen : pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, "red", self.rect)
            pg.draw.rect(screen, "green", self.rect_feet_collition)
        self.__actual_image_animation = self.__actual_animation[self.__actual_frame_index]
        screen.blit(self.__actual_image_animation, self.rect)
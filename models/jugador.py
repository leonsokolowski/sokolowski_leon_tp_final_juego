from auxiliar.animar_sprite import SurfaceManager as sf
import pygame as pg
from auxiliar.constantes import ANCHO_VENTANA, ALTO_VENTANA, DEBUG
from models.proyectil import Proyectil

class Jugador(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y, dict_configs_nivel : dict, frame_rate = 100, speed_walk = 6, speed_run = 12, gravity = 20, jump = 50):
        super().__init__()
        
        self.config_jugador = dict_configs_nivel.get("jugador")
        self.puntaje = 0
        self.vidas = 5
        self.is_alive = True
        #animacion
        self.sprites_jugador = self.config_jugador.get("sprites")
        self.__iddle_r = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("iddle"), 7, 1)
        self.__iddle_l = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("iddle"), 7, 1, flip = True)
        self.__walk_r = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("walk"), 8, 1)
        self.__walk_l = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("walk"), 8, 1, flip = True)
        self.__jump_r = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("jump"), 9, 1)
        self.__jump_l = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("jump"), 9, 1, flip = True)
        self.__run_r = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("run"), 10, 1)
        self.__run_l = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("run"), 10, 1, flip = True)
        self.__shoot_r = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("shoot"), 8, 1)
        self.__shoot_l = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("shoot"), 8, 1, flip = True)
        self.__die = sf.get_surface_from_spritesheeet(self.sprites_jugador.get("die"), 11, 1)
        self.__player_animation_time = 0
        self.__actual_frame_index = 0 #Controla el frame de la lista de animaciones en el que nos encontramos
        self.__actual_animation = self.__iddle_r #Al aparecer el personaje aparece con esta animación
        self.__actual_image_animation = self.__actual_animation[self.__actual_frame_index] #Representa la imagen actual de la lista de animaciones que estemos recorriendo
        
        #movimiento
        self.__move_x = 0
        self.__move_y = 0
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.is_jumping = False
        self.is_landing = False
        self.is_on_land = False
        self.rect = self.__actual_image_animation.get_rect()
        self.rect.x = coord_x
        self.rect.y = coord_y
        self.__diferencia_de_rect = 60
        self.rect_hitbox = self.__actual_image_animation.get_rect()
        self.rect_hitbox.x = coord_x
        self.rect_hitbox.y = coord_y + self.__diferencia_de_rect
        self.rect_hitbox.height = self.rect.height - self.__diferencia_de_rect
        self.__is_looking_right = True
        
        #disparo
        self.projectile_time = 0
        self.projectile_cooldown = 550
        self.projectile_group = pg.sprite.Group()

        #plataformas
        self.rect_feet_collition = pg.Rect(self.rect_hitbox.x + self.rect_hitbox.w/4, self.rect_hitbox.y + self.rect_hitbox.h - 5, self.rect_hitbox.w/2, 5)
        
    @property
    def obtener_estado_jumping (self):
        return self.is_jumping
    @property
    def obtener_estado_landing (self):
        return self.__is_landing
    @property
    def obtener_estado_on_land (self):
        return self.is_on_land

    @property
    def obtener_move_x(self):
        return self.__move_x
    
    @property
    def obtener_move_y(self):
        return self.__move_y
    @obtener_move_y.setter
    def obtener_move_y(self,move_y):
        self.__move_y = move_y
    
    def recibir_disparo_y_comprobar_vidas (self):
        self.vidas -= 1
        if self.vidas <= 0:
            self.is_alive = False
            # self.__actual_frame_index = 0
            if self.__actual_animation != self.__die and self.__actual_animation != self.__die:
                self.__actual_animation = self.__die
            
    def morir (self):
        #Aca hacemos cosas que necesitamos que pasen antes de morir.
        self.kill()
    
    def __set_x_animations_preset(self, move_x, animation_list : list[pg.surface.Surface], look_r : bool):
        self.__move_x = move_x
        self.__is_looking_right = look_r
        if self.__actual_animation != animation_list:
            self.__actual_frame_index = 0
            self.__actual_animation = animation_list
    
    def jump_animation(self):
        self.__actual_frame_index = 0
        if self.is_jumping:
            self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        elif self.is_landing:
            self.__actual_animation = self.__walk_r if self.__is_looking_right else self.__walk_l
        else:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
    
    def jump(self): 
        pixel_inicial_salto = self.rect_hitbox.top
        if (self.is_on_land == True and pixel_inicial_salto - self.__jump != 1000) and not self.is_landing and not self.is_jumping: 
            self.__move_y -= self.__jump
            self.is_jumping = True
            self.is_on_land = False
        elif pixel_inicial_salto - self.__jump >= 1000 or (self.is_jumping == False and self.is_on_land == False):
            self.is_landing = True    
        else:
            self.is_jumping = False
            self.is_landing = False
            self.is_on_land = True
            self.stay()
        
    def walk(self, direction : str = "Right"):
        match(direction):
            case "Right":
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
            case "Left":
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r = look_right)

    def run(self, direction : str = "Right"):
        match(direction):
            case "Right":
                look_right = True
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r = look_right)
            case "Left":
                look_right = False
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r = look_right)
                
    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__actual_frame_index = 0
            self.__move_x = 0
            self.__move_y = 0
      
    
    def __set_borders_limit_x(self): #Relacionado al movimiento
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.rect.right < ANCHO_VENTANA - self.__actual_image_animation.get_width()/5 else 0
            pixels_move = self.__move_x if self.rect_hitbox.right < ANCHO_VENTANA - self.__actual_image_animation.get_width()/5 else 0
            pixels_move = self.__move_x if self.rect_feet_collition.right < ANCHO_VENTANA - self.__actual_image_animation.get_width()/5 else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.rect.left > 0 else 0
            pixels_move = self.__move_x if self.rect_hitbox.left > 0 else 0
            pixels_move = self.__move_x if self.rect_feet_collition.left > 0 else 0
        return pixels_move
    
    def __set_borders_limit_y(self): #Relacionado al movimiento
        pixels_move = 0
        if self.__move_y > 0:
            pixels_move = self.__move_y if self.rect.bottom < ALTO_VENTANA else 0 #- self.__actual_image_animation.get_height()
            pixels_move = self.__move_y if self.rect_hitbox.bottom < ALTO_VENTANA else 0 #- self.__actual_image_animation.get_height()
            pixels_move = self.__move_y if self.rect_feet_collition.bottom < ALTO_VENTANA else 0 #- self.__actual_image_animation.get_height()
            #print(pixels_move)
        elif self.__move_y < 0:
            pixels_move = self.__move_y if self.rect.top > 0 else 0
            pixels_move = self.__move_y if self.rect_hitbox.top > 0 else 0
            pixels_move = self.__move_y if self.rect_feet_collition.top > 0 else 0
        return pixels_move
    @property
    def get_projectiles(self) -> list[Proyectil]:
        return self.projectile_group
    
    def shoot(self):  
        if self.cooldown_to_shoot():
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
        return Proyectil(rect_direction, self.rect.centery, direction, self.config_jugador, not self.__is_looking_right)

    def cooldown_to_shoot (self) -> bool:
        current_time= pg.time.get_ticks()
        return current_time - self.projectile_time >= self.projectile_cooldown
    
    def do_movement(self, delta_ms): #Relacionado al movimiento
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time	= 0
            self.rect.x += self.__set_borders_limit_x()
            self.rect.y += self.__set_borders_limit_y()
            self.rect_hitbox.x += self.__set_borders_limit_x()
            self.rect_hitbox.y += self.__set_borders_limit_y()
            self.rect_feet_collition.x += self.__set_borders_limit_x()
            self.rect_feet_collition.y += self.__set_borders_limit_y()
            #Parte relacionada a saltar
            if not self.is_on_land:
                self.__move_y += self.__gravity
                #self.rect_hitbox.y += self.__gravity
                #self.rect_feet_collition.y += self.__gravity
                #self.is_on_land = True
                self.is_landing = True
            else:
                self.__move_y = 0

    
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__actual_frame_index < len(self.__actual_animation) - 1:
                self.__actual_frame_index += 1
            else:
                if self.is_alive:
                    self.__actual_frame_index = 0
                else:
                    self.morir()

    
    def keyboard_events (self):
            
        lista_teclas_presionadas = pg.key.get_pressed()
        
        if lista_teclas_presionadas[pg.K_RIGHT] and lista_teclas_presionadas[pg.K_LSHIFT] and not lista_teclas_presionadas[pg.K_LEFT]:
            self.run("Right")
        if lista_teclas_presionadas[pg.K_LEFT] and lista_teclas_presionadas[pg.K_LSHIFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
            self.run("Left")
        if lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_LSHIFT]:
            self.walk("Right")
        if lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LSHIFT]:
            self.walk("Left")
        # elif lista_teclas_presionadas[pg.K_UP] and not lista_teclas_presionadas[pg.K_SPACE]:
        #     self.jump()
        if lista_teclas_presionadas[pg.K_SPACE] and not lista_teclas_presionadas[pg.K_LSHIFT] and not lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT]:
            self.shoot() 
        if not lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_SPACE]:
            self.stay()
            
    
    def update(self, delta_ms, screen: pg.surface.Surface):
        self.keyboard_events()
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.projectile_group.update(screen)
        self.draw(screen)
    
    def draw(self, screen : pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, "red", self.rect_hitbox)
            pg.draw.rect(screen, "green", self.rect_feet_collition)
        self.__actual_image_animation = self.__actual_animation[self.__actual_frame_index]
        screen.blit(self.__actual_image_animation, self.rect)   
from auxiliar.animar_sprite import SurfaceManager as sf
import pygame as pg
from auxiliar.constantes import ANCHO_VENTANA, ALTO_VENTANA, DEBUG

class Jugador:
    def __init__(self, coord_x, coord_y, frame_rate = 100, speed_walk = 6, speed_run = 12, gravity = 20, jump = 32):
        
        self.__iddle_r = sf.get_surface_from_spritesheeet(r"assets\img\player\iddle\iddle.png", 7, 1)
        self.__iddle_l = sf.get_surface_from_spritesheeet(r"assets\img\player\iddle\iddle.png", 7, 1, flip = True)
        self.__walk_r = sf.get_surface_from_spritesheeet(r"assets\img\player\walk\walk.png", 8, 1)
        self.__walk_l = sf.get_surface_from_spritesheeet(r"assets\img\player\walk\walk.png", 8, 1, flip = True)
        self.__jump_r = sf.get_surface_from_spritesheeet(r"assets\img\player\jump\jump.png", 9, 1)
        self.__jump_l = sf.get_surface_from_spritesheeet(r"assets\img\player\jump\jump.png", 9, 1, flip = True)
        self.__run_r = sf.get_surface_from_spritesheeet(r"assets\img\player\run\run.png", 10, 1)
        self.__run_l = sf.get_surface_from_spritesheeet(r"assets\img\player\run\run.png", 10, 1, flip = True)
        self.__move_x = coord_x
        self.__move_y = coord_y
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__is_jumping = False
        self.__is_landing = False
        self.__is_on_land = True
        self.__inital_frame = 0 #Controla el frame de la lista de animaciones en el que nos encontramos
        self.__actual_animation = self.__iddle_r #Al aparecer el personaje aparece con esta animación
        self.__actual_image_animation = self.__actual_animation[self.__inital_frame] #Representa la imagen actual de la lista de animaciones que estemos recorriendo
        self.__rect = self.__actual_image_animation.get_rect()
        self.__is_looking_right = True
        
    @property
    def obtener_estado_jumping (self):
        return self.__is_jumping
    @property
    def obtener_estado_landing (self):
        return self.__is_landing
    @property
    def obtener_estado_on_land (self):
        return self.__is_on_land
    
    
    def __set_x_animations_preset(self, move_x, animation_list : list[pg.surface.Surface], look_r : bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
    
    def __set_y_animations_preset(self):
        self.__move_y = -self.__jump
        self.__move_x = self.__speed_run if self.__is_looking_right else -self.__speed_run
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__inital_frame = 0
        self.__is_jumping = True
    
    def jump(self): 
        pixel_inicial_salto = self.__rect.top
        if (self.__is_on_land == True or pixel_inicial_salto < 100) and not self.__is_landing: 
            self.__set_y_animations_preset()
            self.__is_on_land = False
        elif pixel_inicial_salto > 100 or (self.__is_jumping == False and self.__is_on_land == False):
            self.__is_landing = True    
        else:
            self.__is_jumping = False
            self.__is_on_land = True
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
            self.__inital_frame = 0
            self.__move_x = 0
            self.__move_y = 0
      
    
    def __set_borders_limit_x(self): #Relacionado al movimiento
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.__rect.right < ANCHO_VENTANA else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.left > 0 else 0
        return pixels_move
    
    def __set_borders_limit_y(self): #Relacionado al movimiento
        pixels_move = 0
        if self.__move_y > 0:
            pixels_move = self.__move_y if self.__rect.bottom < ALTO_VENTANA else 0 #- self.__actual_image_animation.get_height()
        elif self.__move_y < 0:
            pixels_move = self.__move_y if self.__rect.top > 0 else 0
        return pixels_move
    
    def do_movement(self, delta_ms): #Relacionado al movimiento
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time	= 0
            self.__rect.x += self.__set_borders_limit_x()
            self.__rect.y += self.__set_borders_limit_y()
            #Parte relacionada a saltar
            if self.__rect.y < 500:
                self.__rect.y += self.__gravity

    
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__inital_frame < len(self.__actual_animation) - 1:
                self.__inital_frame += 1
            else:
                self.__inital_frame = 0
    
    def update(self, delta_ms):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
    
    def draw(self, screen : pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, "red", self.__rect)
        self.__actual_image_animation = self.__actual_animation[self.__inital_frame]
        screen.blit(self.__actual_image_animation, self.__rect)   
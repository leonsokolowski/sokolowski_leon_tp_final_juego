import pygame
import random as rd
from auxiliar.animar_sprite import SurfaceManager as sf
from models.proyectil import Proyectil

class Minion(pygame.sprite.Sprite):
    def __init__(self, coord_x, coord_y, constraint_x, constraint_y, gravity = 20):
        super().__init__()
        
        self.__percentaje_shoot = 5

        # Animacion
        self.__iddle_r = sf.get_surface_from_spritesheeet(r"assets\img\minions\iddle\iddle.png", 6, 1)
        self.__iddle_l = sf.get_surface_from_spritesheeet(r"assets\img\minions\iddle\iddle.png", 6, 1, flip = True)
        self.__walk_r = sf.get_surface_from_spritesheeet(r"assets\img\minions\walk\walk.png", 8, 1)
        self.__walk_l = sf.get_surface_from_spritesheeet(r"assets\img\minions\walk\walk.png", 8, 1, flip = True)
        self.__run_r = sf.get_surface_from_spritesheeet(r"assets\img\minions\run\run.png", 6, 1)
        self.__run_l = sf.get_surface_from_spritesheeet(r"assets\img\minions\run\run.png", 6, 1, flip = True)
        self.__shoot_r = sf.get_surface_from_spritesheeet(r"assets\img\minions\shoot\shoot.png", 4, 1)
        self.__shoot_l = sf.get_surface_from_spritesheeet(r"assets\img\minions\shoot\shoot.png", 4, 1, flip = True)
        self.__player_animation_time = 0
        self.__actual_frame_index = 0 #Controla el frame de la lista de animaciones en el que nos encontramos
        self.__actual_animation = self.__iddle_r #Al aparecer el personaje aparece con esta animación
        self.__actual_image_animation = self.__actual_animation[self.__actual_frame_index]
        self.__rect = self.__actual_image_animation.get_rect()
        self.__rect.x = coord_x
        self.__rect.y = coord_y
        
        # Atributos de movimiento
        self.__setear_velocidad()
        self.max_x_constraint = constraint_x
        self.max_y_constraint = constraint_y
        self.frame_rate = 120
        self.time_move = 0
        self.__is_looking_right = True
        self.projectile_group = pygame.sprite.Group()
        self.__gravity = gravity
        
        #Animación
        
    
    def constraint(self):  # Ajusta al jugador a los limites de la pantalla
        if self.__is_looking_right:
            if (self.__rect.right + self.speed ) < self.max_x_constraint:
                if self.speed > 6:
                    self.__actual_animation = self.__run_r
                    self.__rect.x += self.speed
                else:
                    self.__actual_animation = self.__walk_r
                    self.__rect.x += self.speed
            else:
                self.__is_looking_right = False
        else:
            if self.__rect.left - self.speed > 0:
                if self.speed > 6:
                    self.__actual_animation = self.__run_l
                    self.__rect.x -= self.speed
                else:
                    self.__actual_animation = self.__walk_l
                    self.__rect.x -= self.speed
            else:
                self.__is_looking_right = True
        
    def __setear_velocidad(self):
        self.speed = rd.randint(1, 12)

    def create_projectile(self):    
        if self.__is_looking_right:
            rect_direction = self.__rect.right
            direction = "right"
        else:
            rect_direction = self.__rect.left
            direction = "left"
        return Proyectil(rect_direction, self.__rect.centery, direction, "minion")
            
    # def shoot_animation(self):
    #     if self.__actual_animation != self.__shoot_r and self.__actual_animation != self.__shoot_l:
    #         if self.__is_looking_right:
    #             self.__actual_animation = self.__shoot_r
    #         else:
    #             self.__actual_animation = self.__shoot_l
    #         self.__actual_frame_index = 0
            
        

    # def shoot(self): 
    #     self.shoot_animation()
    #     self.projectile_group.add(self.create_projectile())
    
    # def can_shoot(self) -> bool:
    #     return rd.random() * 100 <= self.__percentaje_shoot
    
    # def is_shooting(self) -> bool:
    #     return self.can_shoot()

    def do_movement(self, delta_ms):
        self.time_move += delta_ms
        if self.time_move >= self.frame_rate:
            self.time_move = 0
            self.constraint()
            if self.__rect.y < 500:
                self.__rect.y += self.__gravity
    
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.frame_rate:
            self.__player_animation_time = 0
            if self.__actual_frame_index < len(self.__actual_animation) - 1:
                self.__actual_frame_index += 1
            else:
                self.__actual_frame_index = 0

    def update(self, delta_ms, screen: pygame.surface.Surface):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        # if self.is_shooting():
        #     self.shoot()
        self.draw(screen)
        self.projectile_group.draw(screen)
        self.projectile_group.update()

    
    def draw(self, screen: pygame.surface.Surface):
        self.__actual_image_animation = self.__actual_animation[self.__actual_frame_index]
        screen.blit(self.__actual_image_animation, self.__rect)

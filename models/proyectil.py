import pygame as pg
from auxiliar.constantes import ANCHO_VENTANA, ALTO_VENTANA

class Proyectil(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, img_path_player: str, flip : bool = False): #dict_configs_nivel : dict,
        super().__init__()
        
        #self.config_proyectil = dict_configs_nivel.get(img_path_player)
        self.flip = flip
        self.__load_img(img_path_player)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.direction = direction
        

    def __load_img(self, img_path):
        match(img_path):
            case "player":
                self.image = pg.image.load(r"assets\img\player\proyectil\tajo_espada.png")
                if self.flip:
                    self.image = pg.transform.flip(self.image, True, False)
            case "minion":
                self.image = pg.image.load(r"assets\img\minions\proyectil\bola_de_nieve.png")
            case "boss": 
                self.image = pg.image.load(r"assets\img\enemy\proyectil\tempano.png")

    # def __load_img(self):
    #     self.image = pg.image.load(self.config_proyectil.get("proyectil"))
    #     if self.flip:
    #         self.image = pg.transform.flip(self.image, True, False)

    def update(self, screen: pg.surface.Surface):
        
        match self.direction:
            case "right":
                self.rect.x += 20
                if self.rect.x >= ANCHO_VENTANA:
                    self.kill()
            case "left":
                self.rect.x -= 20
                if self.rect.x <= 0:
                    self.kill()
            case "up":
                self.rect.y += 20
                if self.rect.y >= ALTO_VENTANA:
                    self.kill()
            # case "down":
            #     self.rect.y -= 20
            #     if self.rect.y <= 0:
            #         self.kill()
        
        self.draw(screen)
    
    def draw(self, screen: pg.surface.Surface):
        screen.blit(self.image, self.rect)
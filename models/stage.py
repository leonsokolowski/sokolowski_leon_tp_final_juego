import pygame as pg
from models.main_player import Jugador
from models.minion import Minion
from models.plataformas import Plataforma
from auxiliar.constantes import open_configs

class Nivel:
    def __init__(self, pantalla : pg.surface.Surface, limite_x, nivel_actual : str) -> None:
        
        self.config_nivel = open_configs().get(nivel_actual)
        #Atributos del Jugador
        self.sprite_jugador = Jugador(0, 400, self.config_nivel, frame_rate= 70, speed_walk= 10, speed_run= 20, )
        self.jugador = pg.sprite.GroupSingle(self.sprite_jugador)
        #Atributos de los Minions
        self.minions = pg.sprite.Group()
        
        self.config_nivel_actual = self.config_nivel.get("stats_nivel")
        self.maxima_cantidad_enemigos = self.config_nivel_actual.get("cantidad_enemigos") 
        self.cordenadas_enemigos = self.config_nivel_actual.get("coords_enemigos")
        self.pantalla = pantalla
        self.limite_x = limite_x
        self.victoria = False
        self.spawnear_minions()
        
        #Atributos de las plataformas
        self.plataformas = pg.sprite.Group()
        self.maxima_cantidad_plataformas = self.config_nivel_actual.get("cantidad_plataformas") 
        self.cordenadas_plataformas = self.config_nivel_actual.get("coords_plataformas")    
        self.spawnear_plataformas()
            
    def spawnear_minions(self):
        if self.maxima_cantidad_enemigos > len(self.cordenadas_enemigos):
            for coordenada in self.cordenadas_enemigos:
                self.minions.add(Minion(coordenada.get("coord_x"), coordenada.get("coord_y"), self.limite_x, self.config_nivel))
        elif self.maxima_cantidad_enemigos <= len(self.cordenadas_enemigos):
            for coordenada in range(self.maxima_cantidad_enemigos):
                self.minions.add(Minion(self.cordenadas_enemigos[coordenada].get("coord_x"),self.cordenadas_enemigos[coordenada].get("coord_y"), self.limite_x, self.config_nivel))
    
    def spawnear_plataformas(self):
        if self.maxima_cantidad_plataformas > len(self.cordenadas_plataformas):
            for coordenada in self.cordenadas_plataformas:
                self.plataformas.add(Plataforma(coordenada.get("coord_x"), coordenada.get("coord_y"), 80, 80))
        elif self.maxima_cantidad_plataformas <= len(self.cordenadas_plataformas):
            for coordenada in range(self.maxima_cantidad_plataformas):
                self.plataformas.add(Plataforma(self.cordenadas_plataformas[coordenada].get("coord_x"),self.cordenadas_plataformas[coordenada].get("coord_y"), 80, 80))
    
    def run(self, delta_ms):
        self.jugador.update(delta_ms, self.pantalla)
        self.minions.update(delta_ms, self.pantalla)
        self.plataformas.update(self.pantalla)
        
        for projectile in self.sprite_jugador.get_projectiles:
            cantidad_antes = len(self.minions)
            if pg.sprite.spritecollide(projectile, self.minions, True):
                projectile.kill()
                cantidad_despues = len(self.minions)
                if cantidad_antes > cantidad_despues:
                    cantidad_vencido = cantidad_antes - cantidad_despues
                    self.sprite_jugador.puntaje += cantidad_vencido * 100
                    print(f'Puntaje actual: {self.sprite_jugador.puntaje} Puntos')
                if len(self.minions) == 0 and not self.victoria:
                    self.victoria = True
                    print(f'Ganaste la partida con: {self.sprite_jugador.puntaje} Puntos!')
        
    
        
        
        
         
import pygame as pg
from models.main_player import Jugador
from models.minion import Minion
from auxiliar.constantes import open_configs

class Nivel:
    def __init__(self, pantalla : pg.surface.Surface, limite_x, nivel_actual : str) -> None:
        
        self.config_nivel = open_configs().get(nivel_actual)
        #Atributos del Jugador
        self.sprite_jugador = Jugador(0, 350, self.config_nivel, frame_rate= 70, speed_walk= 10, speed_run= 20, )
        self.jugador = pg.sprite.GroupSingle(self.sprite_jugador)
        #Atributos de los Minions
        self.minions = pg.sprite.Group()
        self.config_nivel_actual = self.config_nivel.get("stats_nivel")
        self.maxima_cantidad_enemigos = self.config_nivel_actual.get("cantidad_enemigos") 
        self.cordenadas_enemigos = self.config_nivel_actual.get("coords_enemigos")
        self.pantalla = pantalla
        self.limite_x = limite_x
        self.victoria = False
        
        self.minions_class = []
        self.spawnear_minions()
        
        for minion in self.minions_class:
            self.minions.add(minion)

        
        
    def spawnear_minions(self):
        if self.maxima_cantidad_enemigos > len(self.cordenadas_enemigos):
            for coordenada in self.cordenadas_enemigos:
                self.minions_class.append(Minion(coordenada.get("coord_x"), coordenada.get("coord_y"), self.limite_x, self.config_nivel))
        elif self.maxima_cantidad_enemigos <= len(self.cordenadas_enemigos):
            for coordenada in range(self.maxima_cantidad_enemigos):
                self.minions_class.append(Minion(self.cordenadas_enemigos[coordenada].get("coord_x"),self.cordenadas_enemigos[coordenada].get("coord_y"), self.limite_x, self.config_nivel))
    
    def run(self, delta_ms):
        self.jugador.update(delta_ms, self.pantalla)
        self.minions.update(delta_ms, self.pantalla)
        
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
        
    
        
        
        
         
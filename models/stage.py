import pygame as pg
from models.main_player import Jugador
from models.minion import Minion
from models.plataformas import Plataforma
from models.fruits import Fruta
from auxiliar.constantes import open_configs

class Nivel:
    def __init__(self, pantalla : pg.surface.Surface, limite_x, nivel_actual : str) -> None:
        
        self.config_nivel = open_configs().get(nivel_actual)
        self.config_nivel_actual = self.config_nivel.get("stats_nivel")
        
        #Atributos de las plataformas
        self.plataformas = pg.sprite.Group()
        self.maxima_cantidad_plataformas = self.config_nivel_actual.get("cantidad_plataformas") 
        self.cordenadas_plataformas = self.config_nivel_actual.get("coords_plataformas")    
        self.spawnear_plataformas()

        #Atributos del Jugador
        self.sprite_jugador = Jugador(0, 300, self.config_nivel, frame_rate= 70, speed_walk= 10, speed_run= 20, )
        self.jugador = pg.sprite.GroupSingle(self.sprite_jugador)
        
        #Atributos de los Minions
        self.minions = pg.sprite.Group()
        self.maxima_cantidad_enemigos = self.config_nivel_actual.get("cantidad_enemigos") 
        self.cordenadas_enemigos = self.config_nivel_actual.get("coords_enemigos")
        self.pantalla = pantalla
        self.limite_x = limite_x
        self.victoria = False
        self.spawnear_minions()
        
        #Atributos de las frutas
        self.frutas = pg.sprite.Group()
        self.maxima_cantidad_frutas = self.config_nivel_actual.get("cantidad_frutas")
        self.cordenadas_frutas = self.config_nivel_actual.get("coords_frutas")
        self.spawnear_frutas()
        
        
            
            

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
                self.plataformas.add(Plataforma(coordenada.get("coord_x"), coordenada.get("coord_y"), coordenada.get("ancho"), coordenada.get("alto")))
        elif self.maxima_cantidad_plataformas <= len(self.cordenadas_plataformas):
            for coordenada in range(self.maxima_cantidad_plataformas):
                self.plataformas.add(Plataforma(self.cordenadas_plataformas[coordenada].get("coord_x"),self.cordenadas_plataformas[coordenada].get("coord_y"), self.cordenadas_plataformas[coordenada].get("ancho"), self.cordenadas_plataformas[coordenada].get("alto")))
    
    def spawnear_frutas(self):
        if self.maxima_cantidad_frutas > len(self.cordenadas_frutas):
            for coordenada in self.cordenadas_frutas:
                self.frutas.add(Fruta(coordenada.get("coord_x"), coordenada.get("coord_y"), self.config_nivel))
        elif self.maxima_cantidad_frutas <= len(self.cordenadas_frutas):
            for coordenada in range(self.maxima_cantidad_frutas):
                self.frutas.add(Fruta(self.cordenadas_frutas[coordenada].get("coord_x"),self.cordenadas_frutas[coordenada].get("coord_y"), self.config_nivel))     
    
    def run(self, delta_ms):
        self.plataformas.update(self.pantalla)
        self.minions.update(delta_ms, self.pantalla)
        self.frutas.update(delta_ms, self.pantalla)
        self.jugador.update(delta_ms, self.pantalla)
        self.check_collides()
    
    def check_collides(self):   
        for projectile in self.sprite_jugador.get_projectiles:
            cantidad_minions_antes = len(self.minions)
            if pg.sprite.spritecollide(projectile, self.minions, True):
                projectile.kill()
                cantidad_minions_despues = len(self.minions)
                if cantidad_minions_antes > cantidad_minions_despues:
                    cantidad_vencido = cantidad_minions_antes - cantidad_minions_despues
                    self.sprite_jugador.puntaje += cantidad_vencido * 100
                    print(f'Puntaje actual: {self.sprite_jugador.puntaje} Puntos')
                   
        for plataforma in self.plataformas:
                if self.jugador.sprite.obtener_move_y > 0:
                    #if plataforma.rect.colliderect(self.sprite_jugador.rect_feet_collition):
                    #print('hola')
                    if plataforma.rect.colliderect(self.sprite_jugador.rect_feet_collition):
                        self.sprite_jugador.is_on_land = True
                        print(self.sprite_jugador.is_on_land)
                        self.jugador.sprite.obtener_move_y = 0
                        self.sprite_jugador.rect.bottom = plataforma.rect.top + 25
                        self.sprite_jugador.rect_hitbox.bottom = plataforma.rect.top + 25
                        self.sprite_jugador.rect_feet_collition.bottom = plataforma.rect.top + 25
                else:
                    self.sprite_jugador.is_on_land = False
                    print(self.sprite_jugador.is_on_land)
                for minion in self.minions:
                    if plataforma.rect.colliderect(minion.rect):
                        minion.is_on_land = True
                        minion.rect.bottom = plataforma.rect.top + 25
                        minion.rect_feet_collition.bottom = plataforma.rect.top + 25
                    for projectile in minion.get_projectiles:
                        if pg.sprite.spritecollide(projectile, self.jugador, False):
                            self.sprite_jugador.vidas -= 1
                            print(self.sprite_jugador.vidas)
                            print(self.sprite_jugador.is_alive)
                            projectile.kill()
        
        cantidad_frutas_antes = len(self.frutas)       
        if pg.sprite.spritecollide(self.sprite_jugador, self.frutas, True):
            cantidad_frutas_despues = len(self.frutas)
            print("Fruta conseguida")
            if cantidad_frutas_antes > cantidad_frutas_despues:
                cantidad_frutas_recogidas = cantidad_frutas_antes - cantidad_frutas_despues
                self.sprite_jugador.puntaje += cantidad_frutas_recogidas * 100
                print(f'Puntaje actual: {self.sprite_jugador.puntaje} Puntos')
            
        if len(self.minions) == 0 and len(self.frutas) == 0 and not self.victoria:
            self.victoria = True
            print(f'Ganaste la partida con: {self.sprite_jugador.puntaje} Puntos!')        
        
    
        
        
        
         
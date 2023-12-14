import pygame as pg
from models.jugador import Jugador
from models.minion import Minion
from models.plataforma import Plataforma
from models.fruta import Fruta
from models.trampa import Trampa
from models.vacio import Vacio
from auxiliar.constantes import open_configs

class Nivel:
    def __init__(self, pantalla : pg.surface.Surface, limite_x, nivel_actual : str) -> None:
        
        self.config_nivel = open_configs().get(nivel_actual)
        self.config_nivel_actual = self.config_nivel.get("stats_nivel")
        self.nivel_actual = nivel_actual
        #Vacio
        match self.nivel_actual:
            case "nivel_2" | "nivel_3":
                self.sprite_vacio = Vacio(0,620,1270, 100)
                self.vacio = pg.sprite.GroupSingle(self.sprite_vacio)
        #Atributos de las plataformas
        self.plataformas = pg.sprite.Group()
        self.maxima_cantidad_plataformas = self.config_nivel_actual.get("cantidad_plataformas") 
        self.cordenadas_plataformas = self.config_nivel_actual.get("coords_plataformas")    
        self.spawnear_plataformas()
        
        #Atributos de las trampas
        self.trampas = pg.sprite.Group()
        self.maxima_cantidad_trampas = self.config_nivel_actual.get("cantidad_trampas")
        self.cordenadas_trampas = self.config_nivel_actual.get("coords_trampas")
        self.spawnear_trampas()

        #Atributos del Jugador
        match self.nivel_actual:
            case "nivel_1":
                self.sprite_jugador = Jugador(0, 600, self.config_nivel, frame_rate= 70, speed_walk= 10, speed_run= 20)
            case "nivel_2":
                self.sprite_jugador = Jugador(0, 100, self.config_nivel, frame_rate= 70, speed_walk= 10, speed_run= 20)
            case "nivel_3":
                self.sprite_jugador = Jugador(0, 500, self.config_nivel, frame_rate= 70, speed_walk= 10, speed_run= 20)
        self.jugador = pg.sprite.GroupSingle(self.sprite_jugador)
        
        #Atributos de los Minions
        self.minions = pg.sprite.Group()
        self.maxima_cantidad_enemigos = self.config_nivel_actual.get("cantidad_enemigos") 
        self.cordenadas_enemigos = self.config_nivel_actual.get("coords_enemigos")
        self.pantalla = pantalla
        self.limite_x = limite_x
        self.victoria_1 = False
        self.victoria_2 = False
        self.victoria_3 = False
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
                self.plataformas.add(Plataforma(coordenada.get("coord_x"), coordenada.get("coord_y"), coordenada.get("ancho"), coordenada.get("alto"), self.config_nivel))
        elif self.maxima_cantidad_plataformas <= len(self.cordenadas_plataformas):
            for coordenada in range(self.maxima_cantidad_plataformas):
                self.plataformas.add(Plataforma(self.cordenadas_plataformas[coordenada].get("coord_x"),self.cordenadas_plataformas[coordenada].get("coord_y"), self.cordenadas_plataformas[coordenada].get("ancho"), self.cordenadas_plataformas[coordenada].get("alto"), self.config_nivel))
    
    def spawnear_trampas(self):
        if self.maxima_cantidad_trampas > len(self.cordenadas_trampas):
            for coordenada in self.cordenadas_trampas:
                self.trampas.add(Trampa(coordenada.get("coord_x"), coordenada.get("coord_y"), coordenada.get("ancho"), coordenada.get("alto"), self.config_nivel))
        elif self.maxima_cantidad_trampas <= len(self.cordenadas_trampas):
            for coordenada in range(self.maxima_cantidad_trampas):
                self.trampas.add(Trampa(self.cordenadas_trampas[coordenada].get("coord_x"),self.cordenadas_trampas[coordenada].get("coord_y"), self.cordenadas_trampas[coordenada].get("ancho"), self.cordenadas_trampas[coordenada].get("alto"), self.config_nivel))
                
    def spawnear_frutas(self):
        if self.maxima_cantidad_frutas > len(self.cordenadas_frutas):
            for coordenada in self.cordenadas_frutas:
                self.frutas.add(Fruta(coordenada.get("coord_x"), coordenada.get("coord_y"), self.config_nivel))
        elif self.maxima_cantidad_frutas <= len(self.cordenadas_frutas):
            for coordenada in range(self.maxima_cantidad_frutas):
                self.frutas.add(Fruta(self.cordenadas_frutas[coordenada].get("coord_x"),self.cordenadas_frutas[coordenada].get("coord_y"), self.config_nivel))     
    
    def run(self, delta_ms):
        if self.nivel_actual == "nivel_2" or self.nivel_actual == "nivel_3":
            self.vacio.update(self.pantalla)
        self.plataformas.update(self.pantalla)
        self.trampas.update(self.pantalla)
        self.minions.update(delta_ms, self.pantalla)
        self.frutas.update(delta_ms, self.pantalla)
        self.jugador.update(delta_ms, self.pantalla)
        self.check_collides()
    
    def check_collides(self):   
            
            #Vacio con Jugador
            if self.nivel_actual == "nivel_2" or self.nivel_actual == "nivel_3":
                if self.sprite_jugador.is_alive:
                    if self.sprite_vacio.rect_hitbox.colliderect(self.sprite_jugador.rect_feet_collition):
                        self.sprite_jugador.vidas = 1
                        self.sprite_jugador.recibir_daño_y_comprobar_vidas()
            #Disparo Jugador a Minions
            if self.sprite_jugador.is_alive:
                for projectile in self.sprite_jugador.get_projectiles:
                    for minion in self.minions:
                        cantidad_minions_antes = len(self.minions)
                        print(f"antes{cantidad_minions_antes}")
                        if projectile.rect.colliderect(minion.rect):
                            minion.minion_recibir_daño_y_comprobar_vidas()
                            projectile.kill()
                            cantidad_minions_despues = len(self.minions) - 1
                            print(f"despues{cantidad_minions_despues}")
                            if cantidad_minions_antes > cantidad_minions_despues:
                                cantidad_vencido = cantidad_minions_antes - cantidad_minions_despues
                                self.sprite_jugador.puntaje += cantidad_vencido * 100
                                print(f'Puntaje actual: {self.sprite_jugador.puntaje} Puntos')
            
            #Disparo Minion a Jugador
            for minion in self.minions:    
                for projectile in minion.get_projectiles:
                            if projectile.rect.colliderect(self.sprite_jugador.rect_hitbox):
                                self.sprite_jugador.recibir_daño_y_comprobar_vidas()
                                # print(self.sprite_jugador.vidas)
                                # print(self.sprite_jugador.is_alive)
                                projectile.kill()
                    
            #Plataformas con Jugador
            for plataforma in self.plataformas:
                if self.sprite_jugador.is_alive:    
                    if plataforma.rect.colliderect(self.sprite_jugador.rect_feet_collition):
                        #if plataforma.rect.colliderect(self.sprite_jugador.rect_feet_collition):
                        #print('hola')
                        if self.jugador.sprite.obtener_move_y > 0:
                            self.sprite_jugador.is_on_land = True
                            #print(self.sprite_jugador.is_on_land)
                            self.jugador.sprite.obtener_move_y = 0
                            self.sprite_jugador.rect.bottom = plataforma.rect.top + 25
                            self.sprite_jugador.rect_hitbox.bottom = plataforma.rect.top + 25
                            self.sprite_jugador.rect_feet_collition.bottom = plataforma.rect.top + 25
                        else:
                            self.sprite_jugador.is_on_land = False
                            self.sprite_jugador.is_landing = True
                            #print(self.sprite_jugador.is_on_land)
            
            #Plataformas con Minion
                for minion in self.minions:
                    if plataforma.rect.colliderect(minion.rect):
                        # if minion.move_y == 0:
                        minion.is_on_land = True
                        minion.rect.bottom = plataforma.rect.top + 25
                        #print(minion.is_on_land)
                    if plataforma.rect_limite_derecha.colliderect(minion.rect):
                        minion.rect.right = plataforma.rect_limite_derecha.left
                        minion.is_looking_right = not minion.is_looking_right
                    elif plataforma.rect_limite_izquierda.colliderect(minion.rect):
                        minion.rect.left = plataforma.rect_limite_izquierda.right
                        minion.is_looking_right = not minion.is_looking_right
                        
            #Trampas con Jugador    
            for trampa in self.trampas:
                if self.sprite_jugador.is_alive:    
                    if trampa.rect_hitbox.colliderect(self.sprite_jugador.rect_feet_collition):
                        trampa.collide_player = True
                        if trampa.hacer_damage():
                            self.sprite_jugador.recibir_daño_y_comprobar_vidas()
                        
                        
                        
            
            #Trampas con Minion:            
                for minion in self.minions: 
                    if trampa.rect_hitbox_derecha.colliderect(minion.rect):
                        minion.rect.left = trampa.rect_hitbox_derecha.right
                        minion.is_looking_right = not minion.is_looking_right
                    elif trampa.rect_hitbox_izquierda.colliderect(minion.rect):
                        minion.rect.right = trampa.rect_hitbox_izquierda.left
                        minion.is_looking_right = not minion.is_looking_right
                    # else:
                    #     minion.is_on_land = False
                    #     minion.is_landing = True
                        #print(minion.is_on_land)
            
            #Frutas con Jugador            
            cantidad_frutas_antes = len(self.frutas)       
            
            for fruta in self.frutas:
                if self.sprite_jugador.is_alive:
                    if self.sprite_jugador.rect_hitbox.colliderect(fruta.rect):
                        fruta.kill()
                        self.sprite_jugador.sonido_manzana.play()
                        cantidad_frutas_despues = len(self.frutas)
                        print("Fruta conseguida")
                        if cantidad_frutas_antes > cantidad_frutas_despues:
                            cantidad_frutas_recogidas = cantidad_frutas_antes - cantidad_frutas_despues
                            self.sprite_jugador.puntaje += cantidad_frutas_recogidas * 100
                            print(f'Puntaje actual: {self.sprite_jugador.puntaje} Puntos')
                
            if len(self.minions) == 0 and len(self.frutas) == 0:
                match self.nivel_actual:
                    case "nivel_1":
                        print(self.victoria_1)
                        self.victoria_1 = True
                        print(self.victoria_1)
                    case "nivel_2":
                        self.victoria_2 = True
                    case "nivel_3":
                        self.victoria_3 = True
                print(f'Ganaste la partida con: {self.sprite_jugador.puntaje} Puntos!') 
            
            
            
                    
                        
                    
            
                         
                         
    
    
        
        
        
         
import pygame as pg
from models.stage import Nivel
from models.plataformas import Plataforma
from auxiliar.constantes import (ANCHO_VENTANA, ALTO_VENTANA, FPS)

class Juego:
    def __init__(self):
        pass
 
    def run_stage(nivel_actual : str):
        pg.init()
        pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        imagen_de_fondo = pg.image.load("assets/img/background/ice_kingdom.jpeg")
        imagen_de_fondo = pg.transform.scale(imagen_de_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
        reloj = pg.time.Clock()
        juego = Nivel(pantalla, ANCHO_VENTANA, nivel_actual)
        
        # lista_de_plataformas = []
        # lista_de_plataformas.append(Plataforma(0, 550, 800, 50))
        # lista_de_plataformas.append(Plataforma(300, 300, 80, 80))
        
        ejecucion = True
        momento_anterior = pg.time.get_ticks() // 1000
        
        
        while ejecucion:
            lista_eventos = pg.event.get()
            
            
            for event in lista_eventos:
                match event.type:
                    case pg.QUIT:
                        print("Estoy CERRANDO el juego")
                        ejecucion = False
                        break
                    # case pg.KEYDOWN:
                    #     if event.key == pg.K_UP:
                    #         juego.sprite_jugador.jump()
            
        
                        
        
            momento_actual =  pg.time.get_ticks() // 1000
            if momento_actual > momento_anterior:
                #print(momento_actual)
                pass
            
            pantalla.blit(imagen_de_fondo, imagen_de_fondo.get_rect())
            delta_ms= reloj.tick(FPS)
            # for plataforma in lista_de_plataformas:
            #     plataforma.update(pantalla)
            juego.run(delta_ms)
            pg.display.update()

    pg.quit()
import pygame as pg
from models.nivel import Nivel
from models.plataforma import Plataforma
from auxiliar.constantes import (ANCHO_VENTANA, ALTO_VENTANA, FPS, get_font, open_configs)

class Juego:
    def __init__():
        pass
    def run_stage(nivel_actual : str):
        pg.init()
        pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        # imagen_de_fondo = pg.image.load("assets/img/background/background.png")
        # imagen_de_fondo = pg.transform.scale(imagen_de_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
        config_nivel = open_configs().get(nivel_actual)
        config_background = config_nivel.get("background")
        sprite_background = config_background.get("sprites")
        imagen_de_fondo = pg.image.load(sprite_background.get("background"))
        imagen_de_fondo = pg.transform.scale(imagen_de_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
        reloj = pg.time.Clock()
        juego = Nivel(pantalla, ANCHO_VENTANA, nivel_actual)
        
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
                    case pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            juego.sprite_jugador.jump()
                            juego.sprite_jugador.jump()
                            
            
        
                        
        
            momento_actual =  pg.time.get_ticks() // 1000
            #print("hola", momento_anterior)
            #print("chau", momento_actual)
            if momento_actual > momento_anterior:
                print(momento_actual)
                momento_anterior = momento_actual
            momento_actual = str(momento_actual)
            
            
            pantalla.blit(imagen_de_fondo, imagen_de_fondo.get_rect())
            pantalla.blit(get_font(30).render(f"Tiempo: {momento_actual}", True, "red"), (10,10))
            delta_ms= reloj.tick(FPS)

            juego.run(delta_ms)
            pg.display.update()

    pg.quit()
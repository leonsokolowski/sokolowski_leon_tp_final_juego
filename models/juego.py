import pygame as pg
from models.nivel import Nivel
from auxiliar.constantes import (ANCHO_VENTANA, ALTO_VENTANA, FPS, get_font, open_configs)

class Juego:
    def __init__():
        pass
    def run_stage(nivel_actual : str):
        pg.init()
        pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        config_nivel = open_configs().get(nivel_actual)
        #imagen fondo
        config_background = config_nivel.get("background")
        sprite_background = config_background.get("sprites")
        imagen_de_fondo = pg.image.load(sprite_background.get("background"))
        imagen_de_fondo = pg.transform.scale(imagen_de_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
        #reloj
        reloj = pg.time.Clock()
        #nivel
        juego = Nivel(pantalla, ANCHO_VENTANA, nivel_actual)
        #gui
        config_fuentes = config_nivel.get("fuentes")
        fuente_palabras = get_font(config_fuentes.get("palabras"), 35)
        fuente_numeros = get_font(config_fuentes.get("numeros"), 30)
        palabra_tiempo = fuente_palabras.render("Tiempo", True, "white")
        palabra_puntos = fuente_palabras.render("Puntos", True, "white")
        palabra_vidas = fuente_palabras.render("Vidas", True, "white")
        
        configs_gui = config_nivel.get("gui")
        config_images_gui = configs_gui.get("images")
        tablon_madera_tiempo = pg.image.load(config_images_gui.get("tablon_madera"))
        tablon_madera_tiempo = pg.transform.scale(tablon_madera_tiempo, (tablon_madera_tiempo.get_width() / 2.4, tablon_madera_tiempo.get_height() / 3.5))
        tablon_madera_puntos = pg.image.load(config_images_gui.get("tablon_madera"))
        tablon_madera_puntos = pg.transform.scale(tablon_madera_puntos, (tablon_madera_puntos.get_width() / 2.3, tablon_madera_puntos.get_height() / 3.5))
        tablon_madera_vidas = pg.image.load(config_images_gui.get("tablon_madera"))
        tablon_madera_vidas = pg.transform.scale(tablon_madera_vidas, (tablon_madera_vidas.get_width() / 2.4, tablon_madera_vidas.get_height() / 3.5))
        
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
            delta_ms= reloj.tick(FPS)
            juego.run(delta_ms)
            pantalla.blit(tablon_madera_vidas, (-1,0)) #(-1,0)
            pantalla.blit(palabra_vidas, (25,8))#(25,8)
            pantalla.blit(fuente_numeros.render(str(juego.sprite_jugador.vidas), True, "white"), (175, 10)) #(175, 10)
            
            pantalla.blit(tablon_madera_puntos, (225,0))
            pantalla.blit(palabra_puntos, (250,8))
            pantalla.blit(fuente_numeros.render(str(juego.sprite_jugador.puntaje), True, "white"), (390, 10))
            
            pantalla.blit(tablon_madera_tiempo, (460, 0))
            pantalla.blit(palabra_tiempo, (485,8))
            pantalla.blit(fuente_numeros.render(momento_actual, True, "white"), (625, 10))
            
            
            

            pg.display.update()

    pg.quit()
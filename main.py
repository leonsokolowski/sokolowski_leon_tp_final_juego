from models.game import Juego

if __name__ == "__main__":
    Juego.run_stage("nivel_1")
# import pygame as pg
# from auxiliar.constantes import (ANCHO_VENTANA, ALTO_VENTANA, FPS)
# from models.main_player import Jugador
# from models.boss import Boss
# from models.minion import Minion

# pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
# pg.init()
# reloj = pg.time.Clock()
# imagen_de_fondo = pg.image.load("assets/img/background/ice_kingdom.jpeg")
# imagen_de_fondo = pg.transform.scale(imagen_de_fondo, (ANCHO_VENTANA, ALTO_VENTANA))


# ejecucion = True


# gunter = Minion(0, 525, ANCHO_VENTANA)
# bandera_tiempo = True

# momento_anterior = pg.time.get_ticks() // 1000
# while ejecucion:
#     #print(delta_ms)
#     lista_eventos = pg.event.get()
    
    
#     for event in lista_eventos:
        
#         match event.type:
#             case pg.QUIT:
#                 print("Estoy CERRANDO el juego")
#                 ejecucion = False
#                 break
        
        
        
#     pantalla.blit(imagen_de_fondo, imagen_de_fondo.get_rect())
#     delta_ms= reloj.tick(FPS)
#     rey_helado.update(delta_ms)
#     rey_helado.draw(pantalla)
#     gunter.update(delta_ms, pantalla)
#     finn.update(delta_ms, pantalla)
    
    
#     pg.display.update()

# pg.quit()
                
            
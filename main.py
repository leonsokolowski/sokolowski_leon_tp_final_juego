import pygame as pg
from auxiliar.constantes import (ANCHO_VENTANA, ALTO_VENTANA, FPS)
from models.main_player import Jugador
from models.enemy import Enemigo

pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pg.init()
reloj = pg.time.Clock()
imagen_de_fondo = pg.image.load("assets/img/background/ice_kingdom.jpeg")
imagen_de_fondo = pg.transform.scale(imagen_de_fondo, (ANCHO_VENTANA, ALTO_VENTANA))


ejecucion = True

finn = Jugador(700, 350,  frame_rate= 70, speed_walk= 10, speed_run= 20)
rey_helado = Enemigo(0,0, frame_rate=70, speed_walk= 10, speed_run=20)
bandera_tiempo = True

momento_anterior = pg.time.get_ticks() // 1000
while ejecucion:
    #print(delta_ms)
    lista_eventos = pg.event.get()
    lista_teclas_presionadas = pg.key.get_pressed()
    
    for event in lista_eventos:
        
        match event.type:
            case pg.QUIT:
                print("Estoy CERRANDO el juego")
                ejecucion = False
                break
    
    if lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT]:
        finn.walk("Right")
    if lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        finn.walk("Left")
    if not lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_SPACE]:
        finn.stay()
    if lista_teclas_presionadas[pg.K_RIGHT] and lista_teclas_presionadas[pg.K_LSHIFT] and not lista_teclas_presionadas[pg.K_LEFT]:
        finn.run("Right")
    if lista_teclas_presionadas[pg.K_LEFT] and lista_teclas_presionadas[pg.K_LSHIFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        finn.run("Left")
    if lista_teclas_presionadas[pg.K_UP]:
        finn.jump()
    if lista_teclas_presionadas[pg.K_SPACE]:
        finn.shoot()
        
        
    #print("Is on land: ", finn.obtener_estado_on_land)
    #print("Is landing: ", finn.obtener_estado_landing)
    #print("Is jumping: ", finn.obtener_estado_jumping)
    
    momento_actual =  pg.time.get_ticks() // 1000
    if momento_actual > momento_anterior:
        #print(momento_actual)
        if momento_actual % 6 == 0:
            if bandera_tiempo:
                bandera_tiempo = False
            elif bandera_tiempo == False:
                bandera_tiempo = True
        momento_anterior = momento_actual
    
    if bandera_tiempo == True:
        rey_helado.walk("Right")
    if bandera_tiempo == False:
        rey_helado.walk("Left") 
        
    pantalla.blit(imagen_de_fondo, imagen_de_fondo.get_rect())
    delta_ms= reloj.tick(FPS)
    finn.update(delta_ms)
    finn.draw(pantalla)
    finn.projectile_group.draw(pantalla)
    rey_helado.update(delta_ms)
    rey_helado.draw(pantalla)
    pg.display.update()

pg.quit()
                
            
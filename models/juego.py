import pygame as pg
from models.nivel import Nivel
from GUI.gui_boton import Boton
from auxiliar.constantes import (ANCHO_VENTANA, ALTO_VENTANA, FPS, get_font, open_configs)

class Juego:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Hora de Aventura: Recoje las manzanas para Tronquitos")
        self.icono = pg.image.load("assets/gui/icono.png")
        pg.display.set_icon(self.icono)
        self.pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.nivel_actual = "nivel_1"
        self.puntacion_1 = 0
        self.puntacion_2 = 0
        self.puntacion_3 = 0
        self.musica = open_configs().get("musica")
        self.musica_pausada = False
        self.volumen_musica = 0.2
        
    def run_stage(self):
        #nivel
        config_nivel = open_configs().get(self.nivel_actual)
        juego = Nivel(self.pantalla, ANCHO_VENTANA, self.nivel_actual)
        
        #imagen fondo
        config_background = config_nivel.get("background")
        sprite_background = config_background.get("sprites")
        imagen_de_fondo = pg.image.load(sprite_background.get("background"))
        imagen_de_fondo = pg.transform.scale(imagen_de_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
        #musica
        if self.musica_pausada == False:
            pg.mixer.music.load(self.musica.get("level"))
            pg.mixer.music.set_volume(self.volumen_musica)
            pg.mixer.music.play(-1)
        #reloj
        reloj = pg.time.Clock()
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
        cerrar_juego = False
        momento_anterior = pg.time.get_ticks() // 1000
        while ejecucion:
            if juego.victoria_1 == True:
                self.puntacion_1 = juego.sprite_jugador.puntaje
                self.nivel_actual = "nivel_2"
                juego = Nivel(self.pantalla, ANCHO_VENTANA, self.nivel_actual)
            
            if juego.victoria_2 == True:
                self.puntacion_2 = juego.sprite_jugador.puntaje
                self.nivel_actual = "nivel_3"
                juego = Nivel(self.pantalla, ANCHO_VENTANA, self.nivel_actual)
            
            if juego.victoria_3 == True:
                self.puntacion_3 == juego.sprite_jugador.puntaje
                print(self.puntacion_1)
                print(self.puntacion_2)
                print(self.puntacion_3)
                self.victoria_juego()
                ejecucion = False
                
            lista_eventos = pg.event.get()
            
            for event in lista_eventos:
                match event.type:
                    case pg.QUIT:
                        print("Estoy CERRANDO el juego")
                        ejecucion = False
                        cerrar_juego = True
                        break
                    case pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            juego.sprite_jugador.sonido_salto.play()
                            juego.sprite_jugador.jump()
                            juego.sprite_jugador.jump()
                                      
        
            momento_actual =  pg.time.get_ticks() // 1000
            #print("hola", momento_anterior)
            #print("chau", momento_actual)
            if momento_actual > momento_anterior:
                #print(momento_actual)
                momento_anterior = momento_actual
            momento_actual = str(momento_actual)
            
            
            self.pantalla.blit(imagen_de_fondo, imagen_de_fondo.get_rect())
            delta_ms= reloj.tick(FPS)
            juego.run(delta_ms)
            self.pantalla.blit(tablon_madera_vidas, (-1,0)) #(-1,0)
            self.pantalla.blit(palabra_vidas, (25,8))#(25,8)
            self.pantalla.blit(fuente_numeros.render(str(juego.sprite_jugador.vidas), True, "white"), (175, 10)) #(175, 10)
            
            self.pantalla.blit(tablon_madera_puntos, (225,0))
            self.pantalla.blit(palabra_puntos, (250,8))
            self.pantalla.blit(fuente_numeros.render(str(juego.sprite_jugador.puntaje), True, "white"), (390, 10))
            
            self.pantalla.blit(tablon_madera_tiempo, (460, 0))
            self.pantalla.blit(palabra_tiempo, (485,8))
            self.pantalla.blit(fuente_numeros.render(momento_actual, True, "white"), (625, 10))
            
            pg.display.update()
        
        if cerrar_juego:
            pg.quit()
            
    def menu (self):
        configs_menu = open_configs().get("menu")
        imagen_de_fondo = pg.image.load(configs_menu.get("fondo"))
        imagen_boton = pg.image.load(configs_menu.get("boton"))
        imagen_boton = pg.transform.scale(imagen_boton, (270, 80))
        imagen_boton_opciones = pg.image.load(configs_menu.get("boton"))
        imagen_boton_opciones = pg.transform.scale(imagen_boton_opciones, (350, 80))
        fuente_menu = configs_menu.get("fuentes")
        lista_de_botones = []
        if self.musica_pausada == False:
            pg.mixer.music.load(self.musica.get("menu"))
            pg.mixer.music.set_volume(self.volumen_musica)
            pg.mixer.music.play(-1)
        menu_corriendo = True
        cerrar_juego = False
        while menu_corriendo:
            self.pantalla.blit(imagen_de_fondo, (0,0))
            
            posicion_del_mouse = pg.mouse.get_pos()
            
            boton_jugar = Boton(imagen_boton, (649,295), "Jugar", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            lista_de_botones.append(boton_jugar)
            boton_opciones = Boton(imagen_boton_opciones, (649,411), "Opciones", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            lista_de_botones.append(boton_opciones)
            boton_salir = Boton(imagen_boton, (649,531), "Salir", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            lista_de_botones.append(boton_salir)
            
            for boton in lista_de_botones:
                boton.change_color(posicion_del_mouse)
                boton.update(self.pantalla)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    menu_corriendo = False
                    cerrar_juego = True
                    pg.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if boton_jugar.check_for_input(posicion_del_mouse):
                        self.run_stage()
                        menu_corriendo = False
                    if boton_opciones.check_for_input(posicion_del_mouse):
                        self.opciones()
                        menu_corriendo = False
                    if boton_salir.check_for_input(posicion_del_mouse):
                        menu_corriendo = False
                        cerrar_juego = True
                        
            pg.display.update()
            
        if cerrar_juego:
            pg.quit()
        
    def opciones(self):
        configs_opciones = open_configs().get("menu")
        imagen_de_fondo = pg.image.load(configs_opciones.get("opciones"))
        imagen_boton = pg.image.load(configs_opciones.get("boton"))
        imagen_boton_mas = pg.image.load(configs_opciones.get("boton_mas"))
        imagen_boton_menos = pg.image.load(configs_opciones.get("boton_menos"))
        imagen_boton = pg.transform.scale(imagen_boton, (270, 80))
        fuente_menu = configs_opciones.get("fuentes")
        lista_de_botones = []
        primer_presion = False
        opciones_corriendo = True
        cerrar_juego = False
        
        while opciones_corriendo:
            self.pantalla.blit(imagen_de_fondo, (0,0))
            
            posicion_del_mouse = pg.mouse.get_pos()
            
            boton_musica = Boton(imagen_boton, (649,295), "Musica", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            lista_de_botones.append(boton_musica)
            #boton_mas_volumen = Boton(imagen_boton_mas, (852,295), "", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            #lista_de_botones.append(boton_mas_volumen)
            #boton_menos_volumen = Boton(imagen_boton_menos, (445,295), "", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            #lista_de_botones.append(boton_menos_volumen)
            boton_menu = Boton(imagen_boton, (649,531), "menu", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            lista_de_botones.append(boton_menu)
            
            for boton in lista_de_botones:
                boton.change_color(posicion_del_mouse)
                boton.update(self.pantalla)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    opciones_corriendo = False
                    cerrar_juego = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.run_stage()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if boton_menu.check_for_input(posicion_del_mouse):
                        self.menu()
                        opciones_corriendo = False
                    if boton_musica.check_for_input(posicion_del_mouse):
                        if primer_presion == False:
                            pg.mixer_music.pause()
                            self.musica_pausada = True
                            primer_presion = True
                        else:
                            pg.mixer_music.unpause()
                            primer_presion = False
                    # if boton_mas_volumen.check_for_input(posicion_del_mouse):
                    #     if self.volumen_musica < 1.0:
                    #         self.volumen_musica += 0.1
                    # if boton_menos_volumen.check_for_input(posicion_del_mouse):
                    #     if self.volumen_musica > 0.0:
                    #         self.volumen_musica -= 0.1
                                   
            pg.display.update()
        
        if cerrar_juego:
            pg.quit()  
              
    def victoria_juego(self):
        configs_opciones = open_configs().get("menu")
        imagen_victoria = pg.image.load(configs_opciones.get("victoria"))
        corriendo_victoria = True
        
        while corriendo_victoria:
            pg.mixer.music.stop()
            self.pantalla.blit(imagen_victoria, (0,0))
            pg.display.update()
        
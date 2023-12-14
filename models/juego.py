import pygame as pg
from models.nivel import Nivel
from GUI.gui_boton import Boton
from auxiliar.constantes import (ANCHO_VENTANA, ALTO_VENTANA, FPS, get_font, open_configs)

class Juego:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Hora de Aventura: ¡Derrota al Rey Helado y salva a la princesa!")
        self.icono = pg.image.load("assets/gui/icono.png")
        pg.display.set_icon(self.icono)
        self.pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.nivel_actual = "nivel_1"
        self.puntacion_1 = 0
        self.puntacion_2 = 0
        self.puntacion_3 = 0
        self.musica = open_configs().get("musica")
        
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
        
        pg.mixer.music.load(self.musica.get("level"))
        pg.mixer.music.set_volume(0.3)
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
        momento_anterior = pg.time.get_ticks() // 1000
        while ejecucion:
            if juego.victoria_1 == True:
                print("caca")
                
                self.nivel_actual = "nivel_2"
                juego = Nivel(self.pantalla, ANCHO_VENTANA, self.nivel_actual)
            
            if juego.victoria_2 == True:
                self.nivel_actual = "nivel_3"
                juego = Nivel(self.pantalla, ANCHO_VENTANA, self.nivel_actual)
            
            lista_eventos = pg.event.get()
            
            for event in lista_eventos:
                match event.type:
                    case pg.QUIT:
                        print("Estoy CERRANDO el juego")
                        ejecucion = False
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
        
        pg.quit()
            
    def menu (self):
        configs_menu = open_configs().get("menu")
        imagen_de_fondo = pg.image.load(configs_menu.get("fondo"))
        imagen_boton = pg.image.load(configs_menu.get("boton"))
        imagen_boton = pg.transform.scale(imagen_boton, (270, 80))
        imagen_boton_opciones = pg.image.load(configs_menu.get("boton"))
        imagen_boton_opciones = pg.transform.scale(imagen_boton_opciones, (350, 80))
        fuente_menu = configs_menu.get("fuentes")
        pg.mixer.music.load(self.musica.get("menu"))
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(-1)
        menu_corriendo = True
        cerrar_juego = False
        while menu_corriendo:
            self.pantalla.blit(imagen_de_fondo, (0,0))
            
            posicion_del_mouse = pg.mouse.get_pos()
            
            boton_jugar = Boton(imagen_boton, (649,295), "Jugar", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            boton_opciones = Boton(imagen_boton_opciones, (649,411), "Opciones", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            boton_salir = Boton(imagen_boton, (649,531), "Salir", get_font(fuente_menu.get("palabras"), 60), "white", "red")
            
            for boton in [boton_jugar, boton_opciones, boton_salir]:
                boton.change_color(posicion_del_mouse)
                boton.update(self.pantalla)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.run_stage()

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
        configs_menu = open_configs().get("menu")
        fuente_menu = configs_menu.get("fuentes")
        opciones_corriendo = True
        
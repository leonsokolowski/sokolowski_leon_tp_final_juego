import json
import pygame as pg

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60
DEBUG = False

def open_configs() -> dict:
    with open("auxiliar\configs.json", 'r', encoding='utf-8') as config:
        return json.load(config)

def get_font(tamaño : int):
    return pg.font.Font(r"assets\font\adventure_time_font.ttf", tamaño)


import json
import pygame as pg

ANCHO_VENTANA = 1270
ALTO_VENTANA = 720
FPS = 60
DEBUG = False

def open_configs() -> dict:
    with open("auxiliar\configs.json", 'r', encoding='utf-8') as config:
        return json.load(config)

def get_font(ubicacion : str, tamaño : int):
    return pg.font.Font(ubicacion, tamaño)


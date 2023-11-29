import json

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60
DEBUG = True

def open_configs() -> dict:
    with open("auxiliar\configs.json", 'r', encoding='utf-8') as config:
        return json.load(config)


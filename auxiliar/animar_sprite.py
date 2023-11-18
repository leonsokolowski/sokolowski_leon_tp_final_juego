import pygame as pg
class SurfaceManager:
    
    @staticmethod
    def get_surface_from_spritesheeet(img_path : str, cols : int, rows : int, step = 1, flip : bool = False) -> list[pg.surface.Surface]:
        """
        Divide la superficie del sprite en subsuperficies.
        """
        sprites_list =  list()
        surface_img = pg.image.load(img_path) #Carga el sprite entero
        frame_width = int(surface_img.get_width() / cols) 
        frame_height = int(surface_img.get_height() / rows) 
        
        for row in range(rows):
            
            for column in range(0, cols, step):
                x_axis = column * frame_width #Busca el punto (0,x) de cada una de las subsuperficies
                y_axis = row * frame_height #Busca el punto (x,0) de cada una de las subsuperficies 
                
                frame_surface = surface_img.subsurface(x_axis, y_axis, frame_width, frame_height) #Crea la subsuperficie
                
                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        
        return sprites_list
                
#imports
import pygame
from src.validate import Validate
from src.gameinterfacecomponent import GameInterfaceComponent

class GridCell(GameInterfaceComponent):
    def __init__(self, name="GridCell", position=(0,0), coords=(0,0), size=(8,8), border_thickness=1, border_color=(255, 255, 255)):
        self.set_coords(coords)
        self.set_border_thickness(border_thickness)
        self.set_border_color(border_color)
        self.set_tile_size(size, border_thickness)
        super().__init__(name=name, position=position, size=size, color=(0,0,0))

    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #COORDINATE METHODS:
    def set_coords(self, coords):
        Validate.grid_coords(coords)
        self.__coords = coords

    def get_coords(self):
        return self.__coords
    
    #TILE SIZE METHODS:
    def set_tile_size(self, size, border_thickness):
        width, height = size
        self.__tile_size = (
            width - (border_thickness * 2),
            height - (border_thickness * 2)
        )
    
    def get_tile_size(self):
        return self.__tile_size
    
    #BORDER THICKNESS METHODS:
    def set_border_thickness(self, border_thickness):
        Validate.cell_border_thickness(border_thickness)
        self.__border_thickness = border_thickness
    
    def get_border_thickness(self):
        return self.__border_thickness
    
    #BORDER COLOR METHODS:
    def set_border_color(self, border_color):
        Validate.color(border_color)
        self.__border_color = border_color

    def get_border_color(self):
        return self.__border_color

    #RENDER SURFACE METHODS:
    def set_surface(self):
        alpha = self.get_alpha()
        border_thickness = self.get_border_thickness()
        
        tile_surface = pygame.Surface(self.get_tile_size(), pygame.SRCALPHA)
        tile_surface.fill((*self.get_color(), alpha))
        self.__surface = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        self.__surface.fill((*self.get_border_color(), alpha))
        self.__surface.blit(tile_surface, (border_thickness, border_thickness))
    
    def get_surface(self):
        return self.__surface
    
    #GAMELOOP METHODS:
    #def render(self, screen):
    #    pass

    def handle_event(self, event, input):
        return False
    

#imports
from src.validate import Validate
from src.gameinterfacecomponent import GameInterfaceComponent

class GridCell(GameInterfaceComponent):
    def __init__(self, name="GridCell", priority=0, position=(0,0), coords=(0,0), size=(8,8)):
        self.set_coords(coords)
        super().__init__(name=name, priority=priority, position=position, size=size)

    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #COORDINATE METHODS:
    def set_coords(self, coords):
        Validate.grid_coords(coords)
        self.__coords = coords

    def get_coords(self):
        return self.__coords
    
    #GAMELOOP METHODS:
    #def render(self, screen):
    #    pass

    def handle_event(self, event, mouse_button_held):
        return False

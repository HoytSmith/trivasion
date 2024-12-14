#imports
from src.validate import Validate

class GridCell:
    def __init__(self, position=(0,0)):
        self.set_position(position)

    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #POSITION METHODS:
    def set_position(self, position):
        Validate.grid_coords(position)
        self.__position = position

    def get_position(self):
        return self.__position
    
#imports
from src.validate import Validate
from src.gridcell import GridCell

class Grid:
    def __init__(self, size=(1,1)):
        self.set_size(size)
        self.reset()
    
    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #SIZE METHODS:
    def set_size(self, size):
        Validate.grid_coords(size)
        self.__size = size
    
    def get_size(self):
        return self.__size
    
    def validate_coordinates(self, coords):
        return coords[0] <= self.__size[0] and coords[1] <= self.__size[1]

    #CELLS METHODS:
    def reset(self):
        width, height = self.get_size()
        self.__cells = [[GridCell((x, y)) for x in range(width)] for y in range(height)]
    
    def get_cell(self, position):
        Validate.grid_coords(position)
        self.validate_coordinates(position)
        x, y = position
        return self.__cells[y][x]

#imports
from src.validate import Validate
from src.gameinterfacecomponent import GameInterfaceComponent
from src.gridcell import GridCell

class Grid(GameInterfaceComponent):
    def __init__(self, name="Grid", priority=0, position=(0,0), grid_size=(1,1), cell_size=(8,8)):
        self.set_grid_size(grid_size)
        self.set_cell_size(cell_size)
        self.reset()
        super().__init__(name=name, priority=priority, position=position)
    
    #VALIDATION METHOD:
    @staticmethod
    def validate_grid(grid):
        if not isinstance(grid, Grid):
            raise TypeError("Grid must be of class Grid or a subclass!")
    
    @staticmethod
    def calc_cell_position(grid_coords, cell_size):
        Validate.grid_coords(grid_coords)
        Validate.cell_size(cell_size)
        x, y = grid_coords
        w, h = cell_size
        return (
            x*w,
            h*y
        )

    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #GRID SIZE METHODS:
    def set_grid_size(self, grid_size):
        Validate.grid_coords(grid_size)
        self.__grid_size = grid_size
    
    def get_grid_size(self):
        return self.__grid_size
    
    def validate_coordinates(self, coords):
        return coords[0] <= self.__grid_size[0] and coords[1] <= self.__grid_size[1]
    
    #CELL SIZE METHODS:
    def set_cell_size(self, cell_size):
        Validate.cell_size(cell_size)
        self.__cell_size = cell_size
    
    def get_cell_size(self):
        return self.__cell_size

    #CELLS METHODS:
    def reset(self):
        width, height = self.get_grid_size()
        cell_size = self.get_cell_size()
        self.__cells = [[
                GridCell(name=f"GridCell({x},{y})", priority=1, position=Grid.calc_cell_position((x, y), cell_size), coords=(x, y), size=cell_size) 
                for x in range(width)] for y in range(height)]
    
    def get_cell(self, coords):
        Validate.grid_coords(coords)
        self.validate_coordinates(coords)
        x, y = coords
        return self.__cells[y][x]

    #GAMELOOP METHODS:
    def render(self, screen):
        width, height = self.get_grid_size()
        for x in range(width):
            for y in range(height):
                self.__cells[y][x].render(screen)

    def handle_event(self, event, mouse_button_held):
        width, height = self.get_grid_size()
        for x in range(width):
            for y in range(height):
                if self.__cells[y][x].handle_event(event, mouse_button_held):
                    return True
        return False

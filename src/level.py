#imports
from src.validate import Validate
from src.gameinterfacecomponent import GameInterfaceComponent
from src.gridcell import GridCell
from src.grid import Grid

class Level():
    def __init__(self, waves = 10, difficulty = "Normal"):
        self.set_waves(waves)
        self.set_difficulty(difficulty)
        self.create_grid()

    #VALIDATION METHOD:
    @staticmethod
    def validate_level(level):
        if not isinstance(level, Level):
            raise TypeError("Level must be of class Level or a subclass!")
    
    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #WAVES METHODS:
    def set_waves(self, waves):
        Validate.waves(waves)
        self.__waves = waves

    def get_waves(self):
        return self.__waves

    #DIFFICULTY METHODS:
    def set_difficulty(self, difficulty):
        Validate.difficulty(difficulty)
        self.__difficulty = difficulty

    def get_difficulty(self):
        return self.__difficulty
    
    #GRID METHODS:
    def set_grid(self, grid):
        Grid.validate_grid(grid)
        self.__grid = grid

    def get_grid(self):
        return self.__grid
    
    def calc_grid_size():
        pass

    def create_grid(self):
        pass
    
    #GAMELOOP METHODS:
    def render(self, screen):
        self.__grid.render(screen)

    def handle_event(self, event, mouse_button_held):
        return self.__grid.handle_event(event, mouse_button_held)

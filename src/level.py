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
    
    def calc_grid_size(self):
        waves = self.get_waves()
        waves_modifier = round(waves / 5) - 1

        diff = self.get_difficulty()
        diff_modifier = 1

        if diff == "Easy":
            diff_modifier = 0
        if diff == "Hard":
            diff_modifier = 2
        
        size_modifier = 4 + waves_modifier + diff_modifier
        return (
            size_modifier * 8,
            size_modifier * 4
        )

    def create_grid(self):
        grid_size = self.calc_grid_size()
        self.set_grid(Grid(name="Gameplay_Grid", position=(0, 0), grid_size=grid_size, cell_size=(32, 32)))
    
    #GAMELOOP METHODS:
    def render(self, screen):
        self.__grid.render(screen)

    def handle_event(self, event, input):
        return self.__grid.handle_event(event, input)

    def update(self, delta_time):
        pass

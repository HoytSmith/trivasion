from src.gamestates import GameState
from src.alignment import Alignment
from src.buttonstate import ButtonState

class Validate():
    #static variables
    priority_minimum = 0
    position_length = 2
    size_length = 2
    size_minimum = 0
    padding_length = 2
    padding_minimum = 0
    color_length = 3
    color_minimum = 0
    color_maximum = 255
    alpha_minimum = 0
    alpha_maximum = 255
    font_size_minimum = 8
    font_size_maximum = 100
    grid_coords_length = 2
    grid_coords_minimum = 0
    grid_coords_maximum = 100
    cell_size_length = 2
    cell_size_minimum = 4
    cell_size_maximum = 256
    cell_border_thickness_minimum = 1
    cell_border_thickness_maximum = 16
    waves_options = [5, 10, 15]
    difficulty_options = ["Easy", "Normal", "Hard"]

    @staticmethod
    def name(name):
        if not isinstance(name, str):
            raise TypeError("Name must be of type String!")
        if name == "":
            raise ValueError("Name can not be empty!")
    
    @staticmethod
    def priority(priority):
        if not isinstance(priority, int):
            raise TypeError("Priority must be an integer!")
        if priority < Validate.priority_minimum:
            raise ValueError(f"Priority must be at least {Validate.priority_minimum}!")
    
    @staticmethod
    def position(position):
        if not isinstance(position, tuple):
            raise TypeError("Position must be a tuple!")
        if len(position) != Validate.position_length:
            raise IndexError(f"Position must contain exactly {Validate.position_length} elements!")
        if not all(isinstance(c, int) for c in position):
            raise ValueError("Position must only contain integers!")
    
    @staticmethod
    def size(size):
        if not isinstance(size, tuple):
            raise TypeError("Size must be a tuple!")
        if len(size) != Validate.size_length:
            raise IndexError(f"Size must contain exactly {Validate.size_length} elements!")
        if not all(isinstance(d, int) and d > Validate.size_minimum for d in size):
            raise ValueError(f"Size must only contain integers greater than {Validate.size_minimum}!")
    
    @staticmethod
    def padding(padding):
        if not isinstance(padding, tuple):
            raise TypeError("Padding must be a tuple!")
        if len(padding) != Validate.padding_length:
            raise IndexError(f"Padding must contain exactly {Validate.padding_length} elements!")
        if not all(isinstance(d, int) and d >= Validate.padding_minimum for d in padding):
            raise ValueError(f"Padding must only contain integers greater than {Validate.padding_minimum}!")
    
    @staticmethod
    def color(color):
        if not isinstance(color, tuple):
            raise TypeError("Color must be a tuple!")
        if len(color) != Validate.color_length:
            raise IndexError(f"Color must contain exactly {Validate.color_length} elements!")
        if not all(isinstance(c, int) and Validate.color_minimum <= c <= Validate.color_maximum for c in color):
            raise ValueError(f"Color values must be at least {Validate.color_minimum} and at most {Validate.color_maximum}!")
    
    @staticmethod
    def alpha(alpha):
        if not isinstance(alpha, int):
            raise TypeError("Alpha must be an integer!")
        if alpha < Validate.alpha_minimum or alpha > Validate.alpha_maximum:
            raise ValueError(f"Alpha value must be at least {Validate.alpha_minimum} and at most {Validate.alpha_maximum}!")
    
    @staticmethod
    def text_content(text_content):
        if not isinstance(text_content, str):
            raise TypeError("Text content must be of type string!")
        if text_content == "":
            raise ValueError("Text content can not be empty!")
    
    @staticmethod
    def font_size(font_size):
        if not isinstance(font_size, int):
            raise TypeError("Font size must be of type integer!")
        if font_size < Validate.font_size_minimum or font_size > Validate.font_size_maximum:
            raise ValueError(f"Font size must be greater than {Validate.font_size_minimum} and at most {Validate.font_size_maximum}!")
    
    @staticmethod
    def grid_coords(coords):
        if not isinstance(coords, tuple):
            raise TypeError("Grid Coordinates must be a tuple!")
        if len(coords) != Validate.grid_coords_length:
            raise IndexError(f"Grid Coordinates must contain exactly {Validate.grid_coords_length} elements!")
        if not all((isinstance(c, int) and Validate.grid_coords_minimum <= c <= Validate.grid_coords_maximum) for c in coords):
            raise ValueError(f"Grid Coordinates must be integers of at least {Validate.grid_coords_minimum} and up to {Validate.grid_coords_maximum}!")
    
    @staticmethod
    def cell_size(cell_size):
        if not isinstance(cell_size, tuple):
            raise TypeError("Grid Cell Size must be a tuple!")
        if len(cell_size) != Validate.cell_size_length:
            raise IndexError(f"Grid Cell Size must contain exactly {Validate.cell_size_length} elements!")
        if not all((isinstance(d, int) and Validate.cell_size_minimum <= d <= Validate.cell_size_maximum) for d in cell_size):
            raise ValueError(f"Grid Cell Size must be integers of at least {Validate.cell_size_minimum} and up to {Validate.cell_size_maximum}!")
    
    @staticmethod
    def cell_border_thickness(border_thickness):
        if not isinstance(border_thickness, int):
            raise TypeError("Grid cell border thickness must be an integer!")
        if Validate.cell_border_thickness_minimum < border_thickness < Validate.cell_border_thickness_maximum:
            raise ValueError(f"Grid cell border thickness must be at least {Validate.cell_border_thickness_minimum} and at most {Validate.cell_border_thickness_maximum}!")
    
    @staticmethod
    def difficulty(difficulty):
        if not isinstance(difficulty, str):
            raise TypeError("Difficulty must be a string!")
        if not difficulty in Validate.difficulty_options:
            raise ValueError(f"{difficulty} is an invalid Difficulty option!")
    
    def waves(waves):
        if not isinstance(waves, int):
            raise TypeError("Waves must be an integer!")
        if not waves in Validate.waves_options:
            raise ValueError(f"{waves} is an invalid Waves option!")

    @staticmethod
    def callback(callback):
        if not callable(callback):
            raise TypeError("Callback must be a callable function!")
    
    @staticmethod
    def game_state(state):
        if not isinstance(state, GameState):
            raise TypeError("Invalid GameState!")

    @staticmethod
    def alignment(alignment):
        if not isinstance(alignment, Alignment):
            raise TypeError("Invalid Alignment!")
    
    @staticmethod
    def button_state(state):
        if not isinstance(state, ButtonState):
            raise TypeError("Invalid ButtonState!")
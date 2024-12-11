from src.gamestates import GameState
from src.gameinterfacecomponent import GameInterfaceComponent
from src.alignment import Alignment
from src.box import Box
from src.label import Label
from src.button import Button
from src.buttonstate import ButtonState

class Validate():
    #static variables
    priority_minimum = 0
    position_length = 2
    size_length = 2
    size_minimum = 0
    color_length = 3
    color_minimum = 0
    color_maximum = 255
    alpha_minimum = 0
    alpha_maximum = 255
    font_size_minimum = 8
    font_size_maximum = 100

    #static methods
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
    def component(component):
        if not isinstance(component, GameInterfaceComponent):
            raise TypeError("Component must be of class GameInterfaceComponent or a subclass!")
    
    @staticmethod
    def box(box):
        if not isinstance(box, Box):
            raise TypeError("Box must be of class Box or a subclass!")
    
    @staticmethod
    def label(label):
        if not isinstance(label, Label):
            raise TypeError("Label must be of class Label or a subclass!")
    
    @staticmethod
    def button(button):
        if not isinstance(button, Button):
            raise TypeError("Button must be of class Button or a subclass!")
    
    @staticmethod
    def game_state(state):
        if not isinstance(state, ButtonState):
            raise TypeError("Invalid GameState!")

    @staticmethod
    def alignment(alignment):
        if not isinstance(alignment, Alignment):
            raise TypeError("Invalid Alignment!")
    
    @staticmethod
    def button_state(state):
        if not isinstance(state, GameState):
            raise TypeError("Invalid ButtonState!")
    
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
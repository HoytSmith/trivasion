import pygame
from src.gameinterfacecomponent import GameInterfaceComponent

class Label(GameInterfaceComponent):
    def __init__(self, name="Label", content="Text here...", position=(0,0), size=24, color=(255, 255, 255)):
        super().__init__(name, position, size)
        self.set_content(content)
        self.set_color(color)
        self.update_label()
    
    def set_content(self, content):
        if not isinstance(content, str):
            raise TypeError("Label text content must be of type string!")
        self.__content = content
    
    def get_content(self):
        return self.__content

    def set_size(self, size=24):
        if not isinstance(size, int):
            raise TypeError("Label text size must be of type integer!")
        self.__size = size
    
    def get_size(self):
        return self.__size

    def set_color(self, color=(255, 255, 255)):
        if not isinstance(color, tuple) and len(color) != 3:
            raise TypeError("Label text color must be a tuple with 3 values!")
        for c in color:
            if not isinstance(c, int):
                raise TypeError("Label text color must contain integer values only!")
            if c < 0 or c > 255:
                raise ValueError("Label text color must contain values between 0 and 255!")
        self.__color = color
    
    def get_color(self):
        return self.__color
    
    def set_font(self):
        self.__font = pygame.font.Font(None, self.get_size())
    
    def get_font(self):
        return self.__font
    
    def set_render(self):
        self.__render = self.get_font().render(self.get_content(), True, self.get_color())
    
    def get_render(self):
        return self.__render
    
    def update_label(self):
        self.set_font()
        self.set_render()
    
    def update_content(self, content):
        self.set_content(content)
        self.update_label()
    
    def update_size(self, size):
        self.set_size(size)
        self.update_label()
    
    def update_color(self, color):
        self.set_color(color)
        self.update_label()

    def render(self, screen):
        #Render logic
        screen.blit(self.get_render(), (self.get_x(), self.get_y()))
    
    def handle_event(self, event):
        # Labels are always non-interactive
        return False
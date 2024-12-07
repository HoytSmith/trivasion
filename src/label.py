import pygame
from src.gameinterfacecomponent import GameInterfaceComponent

class Label(GameInterfaceComponent):
    def __init__(self, name="Label", content="Text here...", position=(0,0), size=24, color=(255, 255, 255)):
        super().__init__(name, position, size)
        self.set_content(content)
        self.set_color(color)
    
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
        for c in color:
            if not isinstance(c, int):
                raise TypeError("Label text color must contain integer values only!")
            if c < 0 or c > 255:
                raise ValueError("Label text color must contain values between 0 and 255!")
        self.__color = color
    
    def get_color(self):
        return self.__color

    def render(self, screen):
        #Render logic
        font = pygame.font.Font(None, self.get_size())
        text_surface = font.render(self.get_content(), True, self.get_color())
        screen.blit(text_surface, (self.get_x(), self.get_y()))
    
    def handle_event(self, event):
        # Labels are always non-interactive
        return False
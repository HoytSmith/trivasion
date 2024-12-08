import pygame
from src.gameinterfacecomponent import GameInterfaceComponent

class Label(GameInterfaceComponent):
    def __init__(self, name="Label", priority=0, content="Text here...", position=(0,0), color=(255, 255, 255), font_size=24):
        self.set_content(content)
        self.set_font_size(font_size)
        super().__init__(name=name, priority=priority, position=position, color=color)
    
    def set_content(self, content):
        if not isinstance(content, str):
            raise TypeError("Label text content must be of type string!")
        self.__content = content
    
    def get_content(self):
        return self.__content

    def set_font_size(self, font_size=24):
        if not isinstance(font_size, int):
            raise TypeError("Label text size must be of type integer!")
        self.__font_size = font_size
    
    def get_font_size(self):
        return self.__font_size
    
    def set_font(self):
        self.__font = pygame.font.Font(None, self.get_font_size())
    
    def get_font(self):
        return self.__font
    
    def set_render(self):
        self.__render = self.get_font().render(self.get_content(), True, self.get_color())
    
    def get_render(self):
        return self.__render
    
    def update_content(self, content):
        self.set_content(content)
        self.update_component()
    
    def update_size(self, size):
        self.set_font_size(size)
        self.update_component()

    def render(self, screen):
        #Render cached text surface
        screen.blit(self.get_render(), (self.get_x(), self.get_y()))
    
    def handle_event(self, event, mouse_button_held):
        # Labels are always non-interactive
        return False
    
    def update_component(self):
        self.set_font()
        self.set_render()
        super().update_component()
import pygame
from src.gameinterfacecomponent import GameInterfaceComponent

class Label(GameInterfaceComponent):
    def __init__(self, name="Label", priority=0, content="Text here...", position=(0,0), color=(255, 255, 255), alpha=255, font_size=24):
        self.set_content(content)
        self.set_alpha(alpha)
        self.set_font_size(font_size)
        super().__init__(name=name, priority=priority, position=position, color=color)
    
    def set_content(self, content):
        if not isinstance(content, str):
            raise TypeError("Label text content must be of type string!")
        self.__content = content
    
    def get_content(self):
        return self.__content

    def set_alpha(self, alpha):
        if not (isinstance(alpha, int) and alpha >= 0 and alpha <= 255):
            raise TypeError("Alpha must be an integer of at least 0 and at most 255!")
        self.__alpha = alpha

    def get_alpha(self):
        return self.__alpha

    def set_font_size(self, font_size=24):
        if not isinstance(font_size, int):
            raise TypeError("Label font size must be of type integer!")
        self.__font_size = font_size
    
    def get_font_size(self):
        return self.__font_size
    
    def set_font(self):
        self.__font = pygame.font.Font(None, self.get_font_size())
    
    def get_font(self):
        return self.__font
    
    def set_text_surface(self):
        self.__text_surface = self.get_font().render(self.get_content(), True, self.get_color())
        self.set_size(self.__text_surface.get_rect().size)

    def get_text_surface(self):
        return self.__text_surface

    def set_render(self):
        self.__render = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        self.__render.blit(self.get_text_surface(), (0,0))
        self.__render.set_alpha(self.get_alpha())
    
    def get_render(self):
        return self.__render
    
    def render(self, screen):
        #Render cached text surface
        screen.blit(self.get_render(), self.get_position())
    
    def handle_event(self, event, mouse_button_held):
        # Labels are always non-interactive
        return False
    
    def update_component(self):
        self.set_font()
        self.set_text_surface()
        self.set_render()
        super().update_component()
    
    # THE FOLLOWING ARE THE UPDATE METHODS - EACH CALLS UPDATE_COMPONENT AT THE END
    # EACH OF THESE METHODS INCLUDES A FLAG 'UPDATE_COMPONENT' THAT CAN BE SET TO FALSE
    # TO REDUCE REDUNDANT UPDATE_COMPONENT CALLS FOR CHILD ELEMENTS
    def update_content(self, content, update_component = True):
        if not isinstance(content, str):
            raise TypeError("Label text content must be of type string!")
        self.set_content(content)
        if update_component:
            self.update_component()
    
    def update_alpha(self, alpha, update_component = True):
        if not (isinstance(alpha, int) and alpha >= 0 and alpha <= 255):
            raise TypeError("Alpha must be an integer of at least 0 and at most 255!")
        self.set_alpha(alpha)
        if update_component:
            self.update_component()
    
    def update_font_size(self, font_size, update_component = True):
        if not isinstance(font_size, int):
            raise TypeError("Label font size must be of type integer!")
        self.set_font_size(font_size)
        if update_component:
            self.update_component()
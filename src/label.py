import pygame
from src.gameinterfacecomponent import GameInterfaceComponent

class Label(GameInterfaceComponent):
    def __init__(self, name="Label", priority=0, content="Text here...", position=(0,0), color=(255, 255, 255), alpha=255, font_size=24):
        self.set_content(content)
        self.set_alpha(alpha)
        self.set_font_size(font_size)
        super().__init__(name=name, priority=priority, position=position, color=color)
    
    #VALIDATION METHODS:
    def validate_content(self, content):
        if not isinstance(content, str):
            raise TypeError("Label text content must be of type string!")
    
    def validate_alpha(self, alpha):
        if not isinstance(alpha, int):
            raise TypeError("Alpha must be an integer!")
        if alpha < 0 or alpha > 255:
            raise ValueError("Alpha value must be at least 0 and at most 255!")
    
    def validate_font_size(self, font_size):
        if not isinstance(font_size, int):
            raise TypeError("Label font size must be of type integer!")
        if font_size < 8 or font_size > 100:
            raise ValueError("Label font size must be greater than 7 and at most 100!")
    
    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #CONTENT METHODS:
    def set_content(self, content):
        self.validate_content(content)
        self.__content = content
    
    def get_content(self):
        return self.__content
    
    #ALPHA METHODS:
    def set_alpha(self, alpha):
        self.validate_alpha(alpha)
        self.__alpha = alpha

    def get_alpha(self):
        return self.__alpha
    
    #FONT SIZE METHODS:
    def set_font_size(self, font_size=24):
        self.validate_font_size(font_size)
        self.__font_size = font_size
    
    def get_font_size(self):
        return self.__font_size
    
    #FONT METHODS:
    def set_font(self, font_path=None):
        self.__font = pygame.font.Font(font_path, self.get_font_size())
    
    def get_font(self):
        return self.__font
    
    #TEXT SURFACE METHODS:
    def set_text_surface(self):
        self.__text_surface = self.get_font().render(self.get_content(), True, self.get_color())
        self.set_size(self.__text_surface.get_rect().size)

    def get_text_surface(self):
        return self.__text_surface
    
    #RENDER SURFACE METHODS:
    def set_render(self):
        self.__render = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        self.__render.blit(self.get_text_surface(), (0,0))
        self.__render.set_alpha(self.get_alpha())
    
    def get_render(self):
        return self.__render
    
    #GAMELOOP METHODS:
    def render(self, screen):
        screen.blit(self.get_render(), self.get_position())
    
    def handle_event(self, event, mouse_button_held):
        # Labels are always non-interactive
        return False
    
    #MAIN UPDATE METHOD
    def update_component(self):
        self.set_font()
        self.set_text_surface()
        self.set_render()
        super().update_component()
    
    # THE FOLLOWING ARE THE UPDATE METHODS - EACH CALLS UPDATE_COMPONENT AT THE END
    # EACH OF THESE METHODS INCLUDES A FLAG 'UPDATE_COMPONENT' THAT CAN BE SET TO FALSE
    # TO REDUCE REDUNDANT UPDATE_COMPONENT CALLS FOR CHILD ELEMENTS
    def update_content(self, content, update_component = True):
        self.set_content(content)
        if update_component:
            self.update_component()
    
    def update_alpha(self, alpha, update_component = True):
        self.set_alpha(alpha)
        if update_component:
            self.update_component()
    
    def update_font_size(self, font_size, update_component = True):
        self.set_font_size(font_size)
        if update_component:
            self.update_component()
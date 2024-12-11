import pygame
from src.gameinterfacecomponent import GameInterfaceComponent
from src.validate import Validate

class Label(GameInterfaceComponent):
    def __init__(self, name="Label", priority=0, content="Text here...", position=(0,0), color=(255, 255, 255), alpha=255, font_size=24):
        self.set_content(content)
        self.set_font_size(font_size)
        super().__init__(name=name, priority=priority, position=position, color=color, alpha=alpha)
    
    #VALIDATION METHOD:
    @staticmethod
    def validate_label(label):
        if not isinstance(label, Label):
            raise TypeError("Label must be of class Label or a subclass!")
    
    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #CONTENT METHODS:
    def set_content(self, content):
        Validate.text_content(content)
        self.__content = content
    
    def get_content(self):
        return self.__content
    
    #FONT SIZE METHODS:
    def set_font_size(self, font_size=24):
        Validate.font_size(font_size)
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
    
    #LABEL SURFACE METHODS:
    def set_label_surface(self):
        self.__render = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        self.__render.blit(self.get_text_surface(), (0,0))
        self.__render.set_alpha(self.get_alpha())
    
    def get_label_surface(self):
        return self.__render
    
    #GAMELOOP METHODS:
    def render(self, screen):
        screen.blit(self.get_label_surface(), self.get_position())
    
    def handle_event(self, event, mouse_button_held):
        # Labels are always non-interactive
        return False
    
    #MAIN UPDATE METHOD
    def update_component(self):
        self.set_font()
        self.set_text_surface()
        self.set_label_surface()
        super().update_component()
    
    # THE FOLLOWING ARE THE UPDATE METHODS - EACH CALLS UPDATE_COMPONENT AT THE END
    # EACH OF THESE METHODS INCLUDES A FLAG 'UPDATE_COMPONENT' THAT CAN BE SET TO FALSE
    # TO REDUCE REDUNDANT UPDATE_COMPONENT CALLS FOR CHILD ELEMENTS
    def update_content(self, content, update_component = True):
        self.set_content(content)
        if update_component:
            self.update_component()
    
    def update_font_size(self, font_size, update_component = True):
        self.set_font_size(font_size)
        if update_component:
            self.update_component()
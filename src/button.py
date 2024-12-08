import pygame
from src.gameinterfacecomponent import GameInterfaceComponent
from src.label import Label
from src.box import Box

class Button(GameInterfaceComponent):
    def __init__(self, name="Button", priority=0, position=(0,0), size=(10,10), callback=None, label=None, styles=None):
        self.set_state("idle")
        self.reset_styles()
        self.set_callback(callback)
        self.set_label(label)
        self.set_styles(styles)
        super().__init__(name=name, priority=priority, position=position, size=size)
    
    def set_callback(self, callback):
        self.__callback = callback
    
    def get_callback(self):
        return self.__callback
    
    def set_label(self, label):
        if label:
            if not isinstance(label, Label):
                raise TypeError("Button label must be object of Label class!")
        self.__label = label
    
    def get_label(self):
        return self.__label
    
    def set_state(self, state):
        if not isinstance(state, str):
            raise TypeError("Button state must be string!")
        self.__state = state
    
    def get_state(self):
        return self.__state
    
    def is_state(self, state):
        return self.__state == state

    def reset_styles(self):
        self.__styles = {
            "idle" : None,
            "hover" : None,
            "active" : None
        }
    
    def set_style(self, key, style):
        if not isinstance(style, Box):
            raise TypeError("Button style must be object of Box class!")
        if key not in self.__styles:
            raise KeyError("Button style name not recognized.")
        self.__styles[key] = style
    
    def set_styles(self, styles):
        if (isinstance(styles, dict)):
            for style in styles:
                self.set_style(style, styles[style])
    
    def get_style(self, key):
        if key not in self.__styles:
            raise KeyError("Button style name not recognized.")
        return self.__styles[key]
    
    def get_styles(self):
        return self.__styles
    
    def change_state(self, newstate):
        if not self.is_state(newstate):
            self.set_state(newstate)
            for style in self.__styles:
                if style == newstate:
                    self.__styles[style].activate()
                    self.__styles[style].show()
                else:
                    self.__styles[style].deactivate()
                    self.__styles[style].hide()
    
    def render(self, screen):
        self.get_style(self.get_state()).render(screen)
        self.get_label().render(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.mouse_over(event.pos):
                self.on_click()
                return True
        elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_over(event.pos):
                self.change_state("hover")
            else:
                self.change_state("idle")
        return False
    
    def on_click(self):
        if callable(self.get_callback()) and not self.is_state("active"):
            self.get_callback()()
        self.change_state("active")
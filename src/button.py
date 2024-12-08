import pygame
from src.gameinterfacecomponent import GameInterfaceComponent
from src.buttonstate import ButtonState
from src.label import Label
from src.box import Box

class Button(GameInterfaceComponent):
    def __init__(self, name="Button", priority=0, position=(0,0), size=(10,10), callback=None, label=None, styles=None):
        self.set_state(ButtonState.IDLE)
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
        if not isinstance(state, ButtonState):
            raise TypeError("Button State must be a valid ButtonState!")
        self.__state = state
    
    def get_state(self):
        return self.__state
    
    def is_state(self, state):
        return self.__state == state

    def reset_styles(self):
        self.__styles = {
            ButtonState.IDLE : None,
            ButtonState.HOVER : None,
            ButtonState.ACTIVE : None
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
    
    def get_active_style(self):
        return self.get_style(self.get_state())
    
    def change_state(self, new_state):
        if not isinstance(new_state, ButtonState):
            raise TypeError("New Button State must be a valid ButtonState!")
        if not self.is_state(new_state):
            self.set_state(new_state)
            for style_state, style in self.__styles.items():
                if style_state == new_state:
                    style.activate()
                    style.show()
                else:
                    style.deactivate()
                    style.hide()
    
    def render(self, screen):
        style = self.get_active_style()
        label = self.get_label()
        if style:
            style.render(screen)
        if label:
            label.render(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.mouse_over(event.pos):
                self.on_click()
                return True
        elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_over(event.pos):
                self.change_state(ButtonState.HOVER)
            else:
                self.change_state(ButtonState.IDLE)
        return False
    
    def on_click(self):
        if callable(self.get_callback()) and not self.is_state(ButtonState.ACTIVE):
            self.get_callback()()
        self.change_state(ButtonState.ACTIVE)
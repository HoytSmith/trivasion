import pygame
from src.gameinterfacecomponent import GameInterfaceComponent
from src.alignment import Alignment
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
    
    def get_current_style(self):
        return self.get_style(self.get_state())
    
    def change_state(self, new_state):
        if not isinstance(new_state, ButtonState):
            raise TypeError("New Button State must be a valid ButtonState!")
        if not self.is_state(new_state):
            self.set_state(new_state)
            for style_state, style in self.__styles.items():
                if style:
                    if style_state == new_state:
                        style.activate()
                        style.show()
                    else:
                        style.deactivate()
                        style.hide()
    
    def render(self, screen):
        style = self.get_current_style()
        label = self.get_label()
        if style:
            style.render(screen)
        if label:
            label.render(screen)

    def handle_event(self, event, mouse_button_held):
        if event.type == pygame.MOUSEBUTTONDOWN and not mouse_button_held:
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
    
    @staticmethod
    def quick_create(name="Button", priority=0, text="Button", position=(0,0), size=(0,0), text_color=(255, 255, 255), 
                     text_size=24, button_color=(0,0,1), callback=None):
        def clamp_color_value(value=0):
            if value > 0:
                return 1
            else:
                return 0
        def calc_style_colors(color=(0,0,0), intensity=0):
            return (
                clamp_color_value(color[0]) * intensity,
                clamp_color_value(color[1]) * intensity,
                clamp_color_value(color[2]) * intensity
            )
        def calc_button_size(button_size = (0,0), label_size = (0,0)):
            return ( max( button_size[0], label_size[0] ) , max( button_size[1], label_size[1] ) )
        #create button label
        label = Label(name=f"{name}_Label", priority=priority+1, content=text, position=position, color=text_color, font_size=text_size)
        label_size = label.get_size()
        #prepare sizing
        button_size = calc_button_size(size, label_size)
        #setup style colors
        idle_intensity = 192    #buttons are moderately bright when idle
        hover_intensity = 255   #buttons are brightest when hovered over
        active_intensity = 128  #buttons are darkest when clicked
        idle_colors = calc_style_colors(button_color, idle_intensity)
        hover_colors = calc_style_colors(button_color, hover_intensity)
        active_colors = calc_style_colors(button_color, active_intensity)
        #create button styles
        idle = Box(name=f"{name}_Idle", priority=priority, position=position, size=button_size, color=idle_colors)
        hover = Box(name=f"{name}_Hover", priority=priority, position=position, size=button_size, color=hover_colors)
        active = Box(name=f"{name}_Active", priority=priority, position=position, size=button_size, color=active_colors)
        #create the button
        button = Button(name=name, priority=priority, position=position, size=button_size, callback=callback, label=label, styles={
            ButtonState.IDLE: idle,
            ButtonState.HOVER: hover,
            ButtonState.ACTIVE: active
        })
        #correctly center the label within the button
        button.position_component_relative(component=label, position=(50,50), percent_flag=True, h_align=Alignment.MIDDLE, v_align=Alignment.MIDDLE)
        return button
import pygame
from src.gameinterfacecomponent import GameInterfaceComponent
from src.alignment import Alignment
from src.buttonstate import ButtonState
from src.label import Label
from src.box import Box
from src.validate import Validate

class Button(GameInterfaceComponent):
    def __init__(self, name="Button", priority=0, position=(0,0), size=(10,10), callback=None, label=None, styles=None):
        self.set_state(ButtonState.IDLE)
        self.reset_styles()
        self.set_callback(callback)
        self.set_label(label)
        self.set_styles(styles)
        super().__init__(name=name, priority=priority, position=position, size=size)

    #VALIDATION METHOD
    @staticmethod
    def validate_button(button):
        if not isinstance(button, Button):
            raise TypeError("Button must be of class Button or a subclass!")
    
    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #CALLBACK METHODS:
    def set_callback(self, callback):
        if callback:
            Validate.callback(callback)
        self.__callback = callback
    
    def get_callback(self):
        return self.__callback
    
    #LABEL METHODS:
    def set_label(self, label):
        if label:
            Label.validate_label(label)
        self.__label = label
    
    def get_label(self):
        return self.__label
    
    def maintain_label_position(self, new_size):
        def calc_new_label_position(label_position, label_size, button_position, button_size, new_button_size):
            # Calculate label's new position to maintain alignment
            label_offset_ratio = 0
            if button_size != label_size:
                label_offset_ratio = (label_position - button_position) / (button_size - label_size) if button_size - label_size != 0 else 0
            return (button_position + round(label_offset_ratio * (new_button_size - label_size)))
        label = self.get_label()
        if label:
            label_width, label_height = label.get_size()

            # make sure the button doesn't become smaller than the label itself
            new_button_width = max(new_size[0], label_width)
            new_button_height = max(new_size[1], label_height)

            new_label_x = calc_new_label_position(label.get_x(), label_width, self.get_x(), self.get_width(), new_button_width)
            new_label_y = calc_new_label_position(label.get_y(), label_height, self.get_y(), self.get_height(), new_button_height)
            
            # apply everything
            label.update_position((new_label_x, new_label_y), update_component=False)
            new_size = (new_button_width, new_button_height)
        return new_size
    
    #BUTTONSTATE METHODS:
    def set_state(self, state):
        Validate.button_state(state)
        self.__state = state
    
    def get_state(self):
        return self.__state
    
    def is_state(self, state):
        return self.__state == state
    
    def change_state(self, new_state):
        Validate.button_state(new_state)
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
    
    #STYLE METHODS:
    def validate_style(self, key):
        if key not in self.__styles:
            raise KeyError("Button style name not recognized.")
    
    def reset_styles(self):
        self.__styles = {
            ButtonState.IDLE : None,
            ButtonState.HOVER : None,
            ButtonState.ACTIVE : None
        }
    
    def set_style(self, key, style):
        Box.validate_box(style)
        self.validate_style(key)
        self.__styles[key] = style
    
    def set_styles(self, styles):
        if (isinstance(styles, dict)):
            for style in styles:
                self.set_style(style, styles[style])
    
    def get_style(self, key):
        self.validate_style(key)
        return self.__styles[key]
    
    def get_styles(self):
        return self.__styles
    
    def get_current_style(self):
        return self.get_style(self.get_state())
    
    #GAMELOOP METHODS:
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
    
    #EVENT METHODS:
    def on_click(self):
        if callable(self.get_callback()) and not self.is_state(ButtonState.ACTIVE):
            self.get_callback()()
        self.change_state(ButtonState.ACTIVE)
    
    #MAIN UPDATE METHOD
    def update_component(self):
        self.__label.update_component()
        for state in self.__styles:
            self.__styles[state].update_component()
        super().update_component()

    # THE FOLLOWING ARE THE UPDATE METHODS - EACH CALLS UPDATE_COMPONENT AT THE END
    # EACH OF THESE METHODS INCLUDES A FLAG 'UPDATE_COMPONENT' THAT CAN BE SET TO FALSE
    # TO REDUCE REDUNDANT UPDATE_COMPONENT CALLS FOR CHILD ELEMENTS
    def update_position(self, new_position, relative = False, update_component = True):
        for state in self.__styles:
            self.__styles[state].update_position(new_position=new_position, relative=relative, update_component=False)
        super().update_position(new_position=new_position, relative=relative, update_component=update_component)
    
    def move(self, movement=(0,0), update_component = True):
        self.update_position(movement, relative=True, update_component=update_component)
    
    def update_size(self, new_size, update_component = True):
        # if a label is present, we wish to preserve its positioning
        # if the new_size is smaller than the label, it will be corrected
        new_size = self.maintain_label_position(new_size)
        
        for state in self.__styles:
            self.__styles[state].update_size(new_size=new_size, update_component=update_component)
        super().update_size(new_size=new_size, update_component=update_component)
    
    #THE FOLLOWING ARE ANY STATIC METHODS
    @staticmethod
    def quick_create(name="Button", priority=0, text="Button", position=(0,0), h_align=Alignment.MIDDLE, v_align=Alignment.MIDDLE, 
                     size=(1,1), padding=(4,2), text_color=(255, 255, 255), text_size=36, button_color=(0,0,1), callback=None):
        #helper function only useful for this specific method
        def calc_style_colors(color=(0,0,0), intensity=0):
            return tuple((1 if c > 0 else 0) * intensity for c in color)
        # validate parameters
        # only parameters that aren't directly passed without
        # modification are validated to avoid redundant checks
        Validate.name(name)
        Validate.priority(priority)
        Validate.alignment(h_align)
        Validate.alignment(v_align)
        Validate.size(size)
        Validate.padding(padding)
        Validate.color(button_color)
        #create button label
        label = Label(name=f"{name}_Label", priority=priority+1, content=text, position=position, color=text_color, font_size=text_size)
        label_size = label.get_size()
        #prepare sizing
        button_size = (
            max(size[0], label_size[0]+(padding[0]*2)),
            max(size[1], label_size[1]+(padding[1]*2))
        )
        #prepare positioning
        btn_pos_x, btn_pos_y = position
        if h_align == Alignment.MIDDLE:
            btn_pos_x -= round(button_size[0]/2)
        if h_align == Alignment.END:
            btn_pos_x -= button_size[0]
        if v_align == Alignment.MIDDLE:
            btn_pos_y -= round(button_size[1]/2)
        if v_align == Alignment.END:
            btn_pos_y -= button_size[1]
        button_pos = (btn_pos_x, btn_pos_y)
        #setup style colors
        idle_intensity = 192    #buttons are moderately bright when idle
        hover_intensity = 255   #buttons are brightest when hovered over
        active_intensity = 128  #buttons are darkest when clicked
        idle_colors = calc_style_colors(button_color, idle_intensity)
        hover_colors = calc_style_colors(button_color, hover_intensity)
        active_colors = calc_style_colors(button_color, active_intensity)
        #create button styles
        idle = Box(name=f"{name}_Idle", priority=priority, position=button_pos, size=button_size, color=idle_colors)
        hover = Box(name=f"{name}_Hover", priority=priority, position=button_pos, size=button_size, color=hover_colors)
        active = Box(name=f"{name}_Active", priority=priority, position=button_pos, size=button_size, color=active_colors)
        #create the button
        button = Button(name=name, priority=priority, position=button_pos, size=button_size, callback=callback, label=label, styles={
            ButtonState.IDLE: idle,
            ButtonState.HOVER: hover,
            ButtonState.ACTIVE: active
        })
        #correctly center the label within the button
        button.position_component_relative(component=label, position=(50,50), percent_flag=True, h_align=Alignment.MIDDLE, v_align=Alignment.MIDDLE)
        return button
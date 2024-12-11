import pygame
from src.alignment import Alignment

class GameInterfaceComponent():
    def __init__(self, name="Component", priority=0, position=(0,0), size=(10,10), color=(255,255,255)):
        self.set_name(name)
        self.set_priority(priority)
        self.set_position(position)
        self.set_size(size)
        self.set_color(color)
        self.deactivate()
        self.hide()
        self.update_component()
    
    #VALIDATION METHODS:
    def validate_name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be of type String!")
        if name == "":
            raise ValueError("Name can not be empty!")
    
    def validate_priority(self, priority):
        if not isinstance(priority, int):
            raise TypeError("Priority must be an integer!")
        if priority < 0:
            raise ValueError("Priority must be at least 0!")
    
    def validate_position(self, position):
        if not isinstance(position, tuple):
            raise TypeError("Position must be a tuple!")
        if len(position) != 2:
            raise IndexError("Position must contain exactly 2 elements!")
        if not all(isinstance(c, int) for c in position):
            raise ValueError("Position must only contain integers!")
    
    def validate_size(self, size):
        if not isinstance(size, tuple):
            raise TypeError("Size must be a tuple!")
        if len(size) != 2:
            raise IndexError("Size must contain exactly 2 elements!")
        if not all(isinstance(d, int) and d > 0 for d in size):
            raise ValueError("Size must only contain integers greater than 0!")
    
    def validate_color(self, color):
        if not isinstance(color, tuple):
            raise TypeError("Color must be a tuple!")
        if len(color) != 3:
            raise IndexError("Color must contain exactly 3 elements!")
        if not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            raise ValueError("Color must only contain integers greater than 0!")
    
    def validate_component(self, component):
        if not isinstance(component, GameInterfaceComponent):
            raise TypeError("Component must be of class GameInterfaceComponent or a subclass!")
    
    def validate_alignment(self, alignment):
        if not isinstance(alignment, Alignment):
            raise TypeError("Invalid Alignment!")

    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #ACTIVITY METHODS:
    def deactivate(self):
        self.__active = False
    
    def activate(self):
        self.__active = True

    def is_active(self):
        return self.__active

    #VISIBILITY METHODS:
    def hide(self):
        self.__visible = False
    
    def show(self):
        self.__visible = True
    
    def is_visible(self):
        return self.__visible
    
    #NAME METHODS:
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.validate_name(name)
        self.__name = name
    
    def is_named(self, name):
        self.validate_name(name)
        return self.__name == name
    
    #PRIORITY METHODS:
    def set_priority(self, priority):
        self.validate_priority(priority)
        self.__priority = priority
    
    def get_priority(self):
        return self.__priority
    
    #POSITION METHODS:
    def set_position(self, position=(0,0)):
        self.validate_position(position)
        self.__position = position
    
    def get_position(self):
        return self.__position
    
    #positions the given component relative to this component
    #given position coordinates are treated as percentages if percent_flag = True
    def position_component_relative(self, component, position = (0,0), percent_flag = False, h_align=Alignment.START, v_align=Alignment.START):
        #check validity of parameters
        self.validate_component(component)
        self.validate_position(position)
        self.validate_alignment(h_align)
        self.validate_alignment(v_align)
        #setup relevant variables
        pos_x, pos_y = position
        new_x, new_y = self.get_position()
        self_w, self_h = self.get_size()
        comp_w, comp_h = component.get_size()
        #transform percentages into absolute coordinates
        if percent_flag:
            pos_x = round((pos_x/100) * self_w)
            pos_y = round((pos_y/100) * self_h)
        #apply alignments
        if h_align == Alignment.MIDDLE:
            pos_x -= round(comp_w/2)
        if h_align == Alignment.END:
            pos_x -= comp_w
        if v_align == Alignment.MIDDLE:
            pos_y -= round(comp_h/2)
        if v_align == Alignment.END:
            pos_y -= comp_h
        #apply results to component position
        new_x += pos_x
        new_y += pos_y
        component.set_position((new_x, new_y))

    def get_x(self):
        return self.__position[0]
    
    def get_y(self):
        return self.__position[1]
    
    #SIZE METHODS:
    def set_size(self, size=(10,10)):
        self.validate_size(size)
        self.__size = size
    
    def get_size(self):
        return self.__size
    
    def get_width(self):
        return self.__size[0]
    
    def get_height(self):
        return self.__size[1]
    
    def calculate_boundaries(self):
        self.__boundaries = {
            "top" : self.get_y(),
            "left" : self.get_x(),
            "right" : self.get_x() + self.get_width(),
            "bottom" : self.get_y() + self.get_height()
        }

    def get_boundaries(self):
        return self.__boundaries
    
    #COLOR METHODS:
    def set_color(self, color=(255, 255, 255)):
        self.validate_color(color)
        self.__color = color
    
    def get_color(self):
        return self.__color
    
    #VARIOUS LOGIC METHODS:
    def collides(self, component):
        self.validate_component(component)
        
        # Get boundaries for self
        self_boundaries = self.get_boundaries()

        # Get boundaries for component
        component_boundaries = component.get_boundaries()

        # Check for overlap
        vertical_overlap = self_boundaries["top"] <= component_boundaries["bottom"] and self_boundaries["bottom"] >= component_boundaries["top"]
        horizontal_overlap = self_boundaries["left"] <= component_boundaries["right"] and self_boundaries["right"] >= component_boundaries["left"]

        return horizontal_overlap and vertical_overlap
    
    def mouse_over(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return (self.get_x() <= mouse_x <= self.get_x() + self.get_width() and self.get_y() <= mouse_y <= self.get_y() + self.get_height())

    #GAMELOOP METHODS:
    def render(self, screen):
        #Default component is a rectangle
        pygame.draw.rect(screen, self.get_color(), (self.get_x(), self.get_y(), self.get_width(), self.get_height()))
    
    def handle_event(self, event, mouse_button_held):
        # Default Component doesn't handle events
        return False
    
    #EVENT METHODS:
    def on_click(self):
        # Override in subclasses for specific behavior
        pass
    
    #MAIN UPDATE METHOD
    def update_component(self):
        self.calculate_boundaries()

    # THE FOLLOWING ARE THE UPDATE METHODS - EACH CALLS UPDATE_COMPONENT AT THE END
    # EACH OF THESE METHODS INCLUDES A FLAG 'UPDATE_COMPONENT' THAT CAN BE SET TO FALSE
    # TO REDUCE REDUNDANT UPDATE_COMPONENT CALLS FOR CHILD ELEMENTS
    def update_position(self, new_position, relative = False, update_component = True):
        if relative:
            #Validation necessary to ensure calculations can be made
            self.validate_position(new_position)
            current_position = self.get_position()
            self.validate_position(current_position)
            new_position = (
                current_position[0] + new_position[0],
                current_position[1] + new_position[1]
            )
        self.set_position(new_position)
        if update_component:
            self.update_component()
    
    def move(self, movement=(0,0), update_component = True):
        self.update_position(movement, relative=True, update_component=update_component)
    
    def update_size(self, newsize, update_component = True):
        self.set_size(newsize)
        if update_component:
            self.update_component()
    
    def update_color(self, color, update_component = True):
        self.set_color(color)
        if update_component:
            self.update_component()

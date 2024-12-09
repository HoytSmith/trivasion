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
    
    def is_active(self):
        return self.__active
    
    def deactivate(self):
        self.__active = False
    
    def activate(self):
        self.__active = True

    def hide(self):
        self.__visible = False
    
    def show(self):
        self.__visible = True
    
    def is_visible(self):
        return self.__visible
    
    def is_named(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be of type String!")
        return self.__name == name
    
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be of type String!")
        self.__name = name
    
    def set_priority(self, priority):
        if not (isinstance(priority, int) and priority >= 0):
            raise TypeError("Priority must be an integer of at least 0!")
        self.__priority = priority
    
    def get_priority(self):
        return self.__priority
    
    def set_position(self, position=(0,0)):
        if not (isinstance(position, tuple) and len(position) == 2 and all(isinstance(c, int) for c in position)):
            raise TypeError("Position must be a tuple containing 2 integers!")
        self.__position = position
    
    def get_position(self):
        return self.__position
    
    #positions the given component relative to this component
    #given position coordinates are treated as percentages if percent_flag = True
    def position_component_relative(self, component, position = (0,0), percent_flag = False, h_align=Alignment.START, v_align=Alignment.START):
        #check validity of parameters
        if not isinstance(component, GameInterfaceComponent):
            raise TypeError("Component being positioned relatively must be of class GameInterfaceComponent or a subclass!")
        if not (isinstance(h_align, Alignment) and isinstance(v_align, Alignment)):
            raise TypeError("Alignments must be of class Alignment!")
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
        if len(self.__position) != 2:
            raise IndexError("Position is not properly set!")
        return self.__position[0]
    
    def get_y(self):
        if len(self.__position) != 2:
            raise IndexError("Position is not properly set!")
        return self.__position[1]
    
    def move(self, movement=(0,0)):
        if not (isinstance(movement, tuple) and len(movement) == 2 and all(isinstance(c, int) for c in movement)):
            raise TypeError("Movement must be a tuple containing 2 integers!")
        self.set_position(self.get_x()+movement[0], self.get_y()+movement[1])
        self.update_component()

    def set_size(self, size=(10,10)):
        if not (isinstance(size, tuple) and len(size) == 2 and all(isinstance(d, int) and d > 0 for d in size)):
            raise TypeError("Size must be a tuple containing 2 integers greater than 0!")
        self.__size = size
    
    def get_size(self):
        return self.__size
    
    def get_width(self):
        if len(self.__size) != 2:
            raise IndexError("Size is not properly set!")
        return self.__size[0]
    
    def get_height(self):
        if len(self.__size) != 2:
            raise IndexError("Size is not properly set!")
        return self.__size[1]
    
    def update_size(self, newsize):
        self.set_size(newsize)
        self.update_component()
    
    def calculate_boundaries(self):
        if not (len(self.__position) == 2 and len(self.__size) == 2):
            raise ValueError("Position and Size must be properly set before boundaries can be calculated!")
        self.__boundaries = {
            "top" : self.get_y(),
            "left" : self.get_x(),
            "right" : self.get_x()+self.get_width(),
            "bottom" : self.get_y()+self.get_height()
        }

    def get_boundaries(self):
        return self.__boundaries

    def set_color(self, color=(255, 255, 255)):
        if not (isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color)):
            raise TypeError("Color must be a tuple with 3 integers between 0 and 255!")
        self.__color = color
    
    def get_color(self):
        return self.__color
    
    def update_color(self, color):
        self.set_color(color)
        self.update_component()
    
    def collides(self, component):
        if not isinstance(component, GameInterfaceComponent):
            raise TypeError("Component must be object of GameInterfaceComponent class or subclass!")
        
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

    def render(self, screen):
        #Default component is a rectangle
        pygame.draw.rect(screen, self.get_color(), (self.get_x(), self.get_y(), self.get_width(), self.get_height()))
    
    def handle_event(self, event, mouse_button_held):
        # Default Component doesn't handle events
        return False

    def update_component(self):
        self.calculate_boundaries()

    def on_click(self):
        # Override in subclasses for specific behavior
        pass

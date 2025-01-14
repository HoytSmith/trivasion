import pygame
from src.alignment import Alignment
from src.validate import Validate

class GameInterfaceComponent():
    def __init__(self, name="Component", priority=0, position=(0,0), size=(10,10), color=(255,255,255), alpha=255):
        self.set_name(name)
        self.set_priority(priority)
        self.set_position(position)
        self.set_size(size)
        self.set_color(color)
        self.set_alpha(alpha)
        self.deactivate()
        self.hide()
        self.update_component()
    
    #VALIDATION METHOD:
    @staticmethod
    def validate_component(component):
        if not isinstance(component, GameInterfaceComponent):
            raise TypeError("Component must be of class GameInterfaceComponent or a subclass!")

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
        Validate.name(name)
        self.__name = name
    
    def is_named(self, name):
        Validate.name(name)
        return self.__name == name
    
    #PRIORITY METHODS:
    def set_priority(self, priority):
        Validate.priority(priority)
        self.__priority = priority
    
    def get_priority(self):
        return self.__priority
    
    #POSITION METHODS:
    def set_position(self, position=(0,0)):
        Validate.position(position)
        self.__position = position
    
    def get_position(self):
        return self.__position
    
    def get_x(self):
        return self.__position[0]
    
    def get_y(self):
        return self.__position[1]

    # positions the given component relative to this component
    # given position coordinates are treated as percentages if percent_flag = True
    def position_component_relative(self, component, position = (0,0), percent_flag = False, h_align=Alignment.START, v_align=Alignment.START):
        #check validity of parameters
        GameInterfaceComponent.validate_component(component)
        Validate.position(position)
        Validate.alignment(h_align)
        Validate.alignment(v_align)
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
    
    # maintains the positioning of a component relative to self,
    # when self is being scaled to the given new_size.
    # if scale_component = True, then the component will resize appropriately.
    # this method implicitly assumes that both values in new_size will not be 
    # smaller than the component's size, unless scale_component = True.
    def maintain_relative_position(self, component, new_size, scale_component = False, update_component = False):
        # validate parameters
        GameInterfaceComponent.validate_component(component)
        Validate.size(new_size)
        # get the basic variables
        self_left, self_top = self.get_position()
        self_width, self_height = self.get_size()
        comp_width, comp_height = component.get_size()
        new_width, new_height = new_size
        # calculate the offset ratios first
        left_offset_ratio = GameInterfaceComponent.calc_offset_ratio(self_left, self_width, component.get_x(), comp_width)
        top_offset_ratio = GameInterfaceComponent.calc_offset_ratio(self_top, self_height, component.get_y(), comp_height)
        # if the component is being scaled, do that prior to updating the position
        if scale_component:
            width_scale = comp_width / self_width
            height_scale = comp_height / self_height
            comp_width = new_width * width_scale
            comp_height = new_height * height_scale
            component.update_size((comp_width, comp_height), update_component=False)
        # calculate the new positions and update component position
        new_position = (
            GameInterfaceComponent.calc_new_position(self_left, comp_width, new_width, left_offset_ratio),
            GameInterfaceComponent.calc_new_position(self_top, comp_height, new_height, top_offset_ratio)
        )
        component.update_position(new_position, update_component=update_component)
    
    #SIZE METHODS:
    def set_size(self, size=(10,10)):
        Validate.size(size)
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
        Validate.color(color)
        self.__color = color
    
    def get_color(self):
        return self.__color
    
    #ALPHA METHODS:
    def set_alpha(self, alpha=255):
        Validate.alpha(alpha)
        self.__alpha = alpha

    def get_alpha(self):
        return self.__alpha
    
    #RENDER SURFACE METHODS:
    def set_surface(self):
        self.__surface = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        self.__surface.fill((*self.get_color(), self.get_alpha()))
    
    def get_surface(self):
        return self.__surface
    
    #VARIOUS LOGIC METHODS:
    def collides(self, component):
        GameInterfaceComponent.validate_component(component)
        
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
        screen.blit(self.get_surface(), self.get_position())
    
    def handle_event(self, event, input):
        # Default Component doesn't handle events
        return False
    
    #EVENT METHODS:
    def on_click(self):
        # Override in subclasses for specific behavior
        pass
    
    #MAIN UPDATE METHOD
    def update_component(self):
        self.calculate_boundaries()
        self.set_surface()

    # THE FOLLOWING ARE THE UPDATE METHODS - EACH CALLS UPDATE_COMPONENT AT THE END
    # EACH OF THESE METHODS INCLUDES A FLAG 'UPDATE_COMPONENT' THAT CAN BE SET TO FALSE
    # TO REDUCE REDUNDANT UPDATE_COMPONENT CALLS FOR CHILD ELEMENTS
    def update_position(self, new_position, relative = False, update_component = True):
        if relative:
            #Validation necessary to ensure calculations can be made
            Validate.position(new_position)
            current_position = self.get_position()
            Validate.position(current_position)
            new_position = (
                current_position[0] + new_position[0],
                current_position[1] + new_position[1]
            )
        self.set_position(new_position)
        if update_component:
            self.update_component()
    
    def move(self, movement=(0,0), update_component = True):
        self.update_position(movement, relative=True, update_component=update_component)
    
    def update_size(self, new_size, update_component = True):
        self.set_size(new_size)
        if update_component:
            self.update_component()
    
    def update_color(self, color, update_component = True):
        self.set_color(color)
        if update_component:
            self.update_component()
    
    def update_alpha(self, alpha, update_component = True):
        self.set_alpha(alpha)
        if update_component:
            self.update_component()

    #THE FOLLOWING ARE ANY STATIC METHODS:

    # calc_offset_ratio calculates the offset ratio of the left or top position
    # between a parent component and its child component
    # implicitly assumes that child_size <= parent_size
    # implicitly assumes that child_position >= parent_position
    @staticmethod
    def calc_offset_ratio(parent_position, parent_size, child_position, child_size):
        if parent_size == child_size:
            # assume a centered alignment if there is no offset on either side
            return 0.5
        elif parent_position == child_position:
            # if given positions align, all the offset goes to the opposite side
            return 0
        else:
            # there is some offset, calculate the ratio and return it
            absolute_offset = child_position - parent_position
            total_offset = parent_size - child_size
            return absolute_offset / total_offset

    # calc_new_child_position calculates the new position that a child component
    # should have relative to its parent based on the given offset_ratio when
    # a resizing is done on the parent with the given new_size value.
    # implicitly assumes that child_size <= new_size
    @staticmethod
    def calc_new_position(parent_position, child_size, new_size, offset_ratio):
        return parent_position + round(offset_ratio * (new_size - child_size))

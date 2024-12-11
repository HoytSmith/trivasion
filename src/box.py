import pygame
from src.gameinterfacecomponent import GameInterfaceComponent
from src.alignment import Alignment
from src.label import Label

class Box(GameInterfaceComponent):
    def __init__(self, name="Box", priority=0, position=(0,0), size=(10,10), color=(255, 255, 255), alpha=255, children=None):
        self.reset_children()
        if children:
            self.add_children(children)
        self.set_alpha(alpha)
        super().__init__(name=name, priority=priority, position=position, size=size, color=color)
    
    def deactivate(self):
        super().deactivate()
        for child in self.__children:
            child.deactivate()
    
    def activate(self):
        super().activate()
        for child in self.__children:
            child.activate()

    def hide(self):
        super().hide()
        for child in self.__children:
            child.hide()
    
    def show(self):
        super().show()
        for child in self.__children:
            child.show()
    
    def set_alpha(self, alpha):
        if not (isinstance(alpha, int) and alpha >= 0 and alpha <= 255):
            raise TypeError("Alpha must be an integer of at least 0 and at most 255!")
        self.__alpha = alpha

    def get_alpha(self):
        return self.__alpha

    def reset_children(self):
        self.__children = []

    def add_child(self, child, sort=True):
        if not isinstance(child, GameInterfaceComponent):
            raise TypeError("Child must be object of GameInterfaceComponent class or subclass!")
        self.__children.append(child)
        if sort:
            self.sort_children()
    
    def add_children(self, children):
        for child in children:
            if isinstance(child, GameInterfaceComponent):
                self.add_child(child, sort=False)
        self.sort_children()
    
    def remove_child(self, child, sort=True):
        if not isinstance(child, GameInterfaceComponent):
            raise TypeError("Child must be object of GameInterfaceComponent class or subclass!")
        if child in self.__children:
            self.__children.remove(child)
        if sort:
            self.sort_children()
    
    def remove_children(self, children):
        for child in children:
            if isinstance(child, GameInterfaceComponent):
                self.remove_child(child, sort=False)
        self.sort_children()
    
    def sort_children(self):
        self.__children.sort(key=lambda child: child.get_priority())

    def get_child(self, name):
        for child in self.__children:
            if child.is_named(name):
                return child
        return None
    
    def get_children(self, names):
        children = []
        for name in names:
            child = self.get_child(name)
            if child:
                children.append(child)
        return children
    
    def set_surface(self):
        self.__surface = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        self.__surface.fill((*self.get_color(), self.get_alpha()))
    
    def get_surface(self):
        return self.__surface

    def render(self, screen):
        screen.blit(self.get_surface(), self.get_position())
        #Children should be rendered after the box itself
        for child in self.__children:
            if child.is_visible():
                child.render(screen)
    
    def handle_event(self, event, mouse_button_held):
        # Children might be interactive
        for child in self.__children:
            if child.is_active():
                if child.handle_event(event, mouse_button_held):
                    break
        # Boxes themselves are non-interactive
        return False
    
    def update_component(self):
        self.set_surface()
        super().update_component()
    
    # THE FOLLOWING ARE THE UPDATE METHODS - EACH CALLS UPDATE_COMPONENT AT THE END
    # EACH OF THESE METHODS INCLUDES A FLAG 'UPDATE_COMPONENT' THAT CAN BE SET TO FALSE
    # TO REDUCE REDUNDANT UPDATE_COMPONENT CALLS FOR CHILD ELEMENTS
    def move(self, movement=(0,0), update_component = True):
        if not (isinstance(movement, tuple) and len(movement) == 2 and all(isinstance(c, int) for c in movement)):
            raise TypeError("Movement must be a tuple containing 2 integers!")
        for child in self.__children:
            child.move(movement, False)
        super().move(movement, update_component)

    def update_alpha(self, alpha, update_component = True):
        if not (isinstance(alpha, int) and alpha >= 0 and alpha <= 255):
            raise TypeError("Alpha must be an integer of at least 0 and at most 255!")
        self.set_alpha(alpha)
        if update_component:
            self.update_component()

    #THE FOLLOWING ARE ANY STATIC METHODS
    @staticmethod
    def create_text_box(name="Text_Box", priority=0, text="Text Box", position=(0,0), h_align=Alignment.MIDDLE, v_align=Alignment.MIDDLE, 
                        size=(0,0), padding=(4,2), box_color=(128,128,128), text_color=(255, 255, 255), text_size=36):
        #create button label
        label = Label(name=f"{name}_Label", priority=priority+1, content=text, position=position, color=text_color, font_size=text_size)
        label_size = label.get_size()
        #prepare sizing
        box_size = (
            max(size[0], label_size[0]+(padding[0]*2)),
            max(size[1], label_size[1]+(padding[1]*2))
        )
        #prepare positioning
        box_pos_x, box_pos_y = position
        if h_align == Alignment.MIDDLE:
            box_pos_x -= round(box_size[0]/2)
        if h_align == Alignment.END:
            box_pos_x -= box_size[0]
        if v_align == Alignment.MIDDLE:
            box_pos_y -= round(box_size[1]/2)
        if v_align == Alignment.END:
            box_pos_y -= box_size[1]
        box_pos = (box_pos_x, box_pos_y)
        #create the button
        text_box = Box(name=name, priority=priority, position=box_pos, size=box_size, color=box_color, children=[label])
        #correctly center the label within the button
        text_box.position_component_relative(component=label, position=(50,50), percent_flag=True, h_align=Alignment.MIDDLE, v_align=Alignment.MIDDLE)
        return text_box
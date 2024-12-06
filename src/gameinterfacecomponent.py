import pygame

class GameInterfaceComponent():
    def __init__(self, name="", position=(0,0), size=(0,0)):
        self.set_name(name)
        self.set_position(position)
        self.set_size(size)
        self.deactivate()
        self.hide()
    
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
    
    def set_position(self, position=(0,0)):
        for coordinate in position:
            if not isinstance(coordinate, int):
                raise ValueError("Position must contain integer values only!")
        self.__position = position
    
    def get_position(self):
        return self.__position
    
    def get_x(self):
        if len(self.__position) != 2:
            raise IndexError("Position is not properly set!")
        return self.__position[0]
    
    def get_y(self):
        if len(self.__position) != 2:
            raise IndexError("Position is not properly set!")
        return self.__position[1]
    
    def set_size(self, size=(0,0)):
        for dimension in size:
            if not isinstance(dimension, int):
                raise ValueError("Size must contain integer values only!")
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
    
    def render(self, screen):
        if self.is_visible():
            #Render logic
            # Example: Draw a placeholder rectangle
            pygame.draw.rect(screen, (200, 200, 200), (self.get_x(), self.get_y(), self.get_width(), self.get_height()))
    
    def handle_event(self, event):
        # Example: Check if a mouse click is within the component
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.get_x() <= mouse_x <= self.get_x() + self.get_width() and self.get_y() <= mouse_y <= self.get_y() + self.get_height():
                self.on_click()

    def on_click(self):
        # Override in subclasses for specific behavior
        pass

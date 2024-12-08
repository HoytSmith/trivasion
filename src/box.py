import pygame
from src.gameinterfacecomponent import GameInterfaceComponent

class Box(GameInterfaceComponent):
    def __init__(self, name="Box", priority=0, position=(0,0), size=(10,10), color=(255, 255, 255), children=None):
        self.reset_children()
        if children:
            self.add_children(children)
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

    def render(self, screen):
        pygame.draw.rect(screen, self.get_color(), (self.get_x(), self.get_y(), self.get_width(), self.get_height()))
        #Children should be rendered after the box itself
        for child in self.__children:
            if child.is_visible():
                child.render(screen)
    
    def handle_event(self, event):
        # Children might be interactive
        for child in self.__children:
            if child.is_active():
                if child.handle_event(event):
                    break
        # Boxes themselves are non-interactive
        return False
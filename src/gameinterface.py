from src.validate import Validate
from src.gameinterfacecomponent import GameInterfaceComponent
from src.grid import Grid

class GameInterface():
    def __init__(self, priority=0, initial_components=None, grid=None):
        self.reset_components()
        self.set_priority(priority)
        if initial_components:
            self.add_components(initial_components)
        self.set_grid(grid)
        self.deactivate()
        self.hide()
    
    #VALIDATION METHOD:
    @staticmethod
    def validate_interface(interface):
        if not isinstance(interface, GameInterface):
            raise TypeError("Interface must be of class GameInterface or a subclass!")

    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #ACTIVITY METHODS:
    def deactivate(self):
        for component in self.__components:
            component.deactivate()
        if self.__grid:
            self.__grid.deactivate()
        self.__active = False
    
    def activate(self):
        for component in self.__components:
            component.activate()
        if self.__grid:
            self.__grid.activate()
        self.__active = True
    
    def is_active(self):
        return self.__active
    
    #VISIBILITY METHODS:
    def hide(self):
        for component in self.__components:
            component.hide()
        if self.__grid:
            self.__grid.hide()
        self.__visible = False
    
    def show(self):
        for component in self.__components:
            component.show()
        if self.__grid:
            self.__grid.show()
        self.__visible = True
    
    def is_visible(self):
        return self.__visible
    
    #PRIORITY METHODS:
    def set_priority(self, priority):
        Validate.priority(priority)
        self.__priority = priority
    
    def get_priority(self):
        return self.__priority
    
    #COMPONENT METHODS:
    def reset_components(self):
        self.__components = []
    
    def add_component(self, component, sort=True):
        GameInterfaceComponent.validate_component(component)
        self.__components.append(component)
        if sort:
            self.sort_components()
    
    def add_components(self, components=[]):
        for component in components:
            if isinstance(component, GameInterfaceComponent):
                self.add_component(component, sort=False)
        self.sort_components()
    
    def remove_component(self, component, sort=True):
        GameInterfaceComponent.validate_component(component)
        if component in self.__components:
            self.__components.remove(component)
        if sort:
            self.sort_components()
    
    def remove_components(self, components):
        for component in components:
            if isinstance(component, GameInterfaceComponent):
                self.remove_component(component, sort=False)
        self.sort_components()
    
    def get_component(self, name):
        for component in self.__components:
            if component.is_named(name):
                return component
        return None
    
    def sort_components(self):
        self.__components.sort(key=lambda component: component.get_priority())
    
    #GRID METHODS:
    def set_grid(self, grid):
        if grid:
            Grid.validate_grid(grid)
        self.__grid = grid

    def get_grid(self):
        return self.__grid

    #GAMELOOP METHODS:
    def render(self, screen):
        if self.__grid and self.__grid.is_visible():
            self.__grid.render(screen)
        for component in self.__components:
            if component.is_visible():
                component.render(screen)
    
    def handle_event(self, event, mouse_button_held):
        for component in self.__components:
            if component.is_active():
                if component.handle_event(event, mouse_button_held):
                    return True
        if self.__grid and self.__grid.is_active():
            if self.__grid.handle_event(event, mouse_button_held):
                return True
        return False

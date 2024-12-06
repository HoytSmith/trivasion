from gameinterfacecomponent import GameInterfaceComponent

class GameInterface():
    def __init__(self, initial_components=[]):
        self.reset_components()
        self.add_components(initial_components)
        self.deactivate()
        self.hide()
    
    def is_active(self):
        return self.__active
    
    def deactivate(self):
        for component in self.__components:
            component.deactivate()
        self.__active = False
    
    def activate(self):
        for component in self.__components:
            component.activate()
        self.__active = True
    
    def hide(self):
        self.__visible = False
    
    def show(self):
        self.__visible = True
    
    def is_visible(self):
        return self.__visible
    
    def reset_components(self):
        self.__components = []
    
    def add_component(self, component):
        if not isinstance(component, GameInterfaceComponent):
            raise TypeError("Component must be object of class GameInterfaceComponent!")
        self.__components.append(component)
    
    def add_components(self, components=[]):
        for component in components:
            if isinstance(component, GameInterfaceComponent):
                self.add_component(component)
    
    def remove_component(self, component):
        if not isinstance(component, GameInterfaceComponent):
            raise TypeError("Component must be object of class GameInterfaceComponent!")
        if component in self.__components:
            self.__components.remove(component)
    
    def remove_components(self, components):
        for component in components:
            if isinstance(component, GameInterfaceComponent):
                self.remove_component(component)
    
    def get_component(self, name):
        for component in self.__components:
            if component.is_named(name):
                return component
        return None
    
    def render(self, screen):
        if self.is_visible():
            for component in self.__components:
                component.render(screen)
    
    def handle_event(self, event):
        if self.is_active():
            for component in self.__components:
                if component.handle_event(event):
                    break

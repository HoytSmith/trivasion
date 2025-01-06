from src.validate import Validate
from src.gameinterfacecomponent import GameInterfaceComponent

class GameInterface():
    def __init__(self, priority=0, initial_components=None):
        self.reset_components()
        self.set_priority(priority)
        if initial_components:
            self.add_components(initial_components)
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
        self.__active = False
    
    def activate(self):
        for component in self.__components:
            component.activate()
        self.__active = True
    
    def is_active(self):
        return self.__active
    
    #VISIBILITY METHODS: (ALSO AFFECTS ACTIVITY)
    def hide(self):
        for component in self.__components:
            component.hide()
            component.deactivate()
        self.__visible = False
        self.__active = False
    
    def show(self):
        for component in self.__components:
            component.show()
            component.activate()
        self.__visible = True
        self.__active = True
    
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

    #GAMELOOP METHODS:
    def render(self, screen):
        for component in self.__components:
            if component.is_visible():
                component.render(screen)
    
    def handle_event(self, event, input):
        for component in self.__components:
            if component.is_active():
                if component.handle_event(event, input):
                    return True
        return False

from src.gameinterfacecomponent import GameInterfaceComponent

class GameInterface():
    def __init__(self, priority=0, initial_components=None):
        self.reset_components()
        self.set_priority(priority)
        if initial_components:
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
        for component in self.__components:
            component.hide()
        self.__visible = False
    
    def show(self):
        for component in self.__components:
            component.show()
        self.__visible = True
    
    def is_visible(self):
        return self.__visible
    
    def set_priority(self, priority):
        if not (isinstance(priority, int) and priority >= 0):
            raise TypeError("Priority must be an integer of at least 0!")
        self.__priority = priority
    
    def get_priority(self):
        return self.__priority
    
    def reset_components(self):
        self.__components = []
    
    def add_component(self, component, sort=True):
        if not isinstance(component, GameInterfaceComponent):
            raise TypeError("Component must be object of class GameInterfaceComponent!")
        self.__components.append(component)
        if sort:
            self.sort_components()
    
    def add_components(self, components=[]):
        for component in components:
            if isinstance(component, GameInterfaceComponent):
                self.add_component(component, sort=False)
        self.sort_components()
    
    def remove_component(self, component, sort=True):
        if not isinstance(component, GameInterfaceComponent):
            raise TypeError("Component must be object of class GameInterfaceComponent!")
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

    def render(self, screen):
        for component in self.__components:
            if component.is_visible():
                component.render(screen)
    
    def handle_event(self, event, mouse_button_held):
        for component in self.__components:
            if component.is_active():
                if component.handle_event(event, mouse_button_held):
                    break

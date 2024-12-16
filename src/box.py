from src.gameinterfacecomponent import GameInterfaceComponent
from src.alignment import Alignment
from src.label import Label
from src.validate import Validate

class Box(GameInterfaceComponent):
    def __init__(self, name="Box", priority=0, position=(0,0), size=(10,10), color=(255, 255, 255), alpha=255, children=None):
        self.reset_children()
        if children:
            self.add_children(children)
        super().__init__(name=name, priority=priority, position=position, size=size, color=color, alpha=alpha)
    
    #VALIDATION METHOD:
    @staticmethod
    def validate_box(box):
        if not isinstance(box, Box):
            raise TypeError("Box must be of class Box or a subclass!")
    
    #SETTERS, GETTERS AND OTHER CLASS METHODS:
    #ACTIVITY METHODS:
    def deactivate(self):
        super().deactivate()
        for child in self.__children:
            child.deactivate()
    
    def activate(self):
        super().activate()
        for child in self.__children:
            child.activate()
    
    #VISIBILITY METHODS:
    def hide(self):
        super().hide()
        for child in self.__children:
            child.hide()
    
    def show(self):
        super().show()
        for child in self.__children:
            child.show()
    
    #CHILD METHODS:
    def reset_children(self):
        self.__children = []

    def add_child(self, child, sort=True):
        GameInterfaceComponent.validate_component(child)
        self.__children.append(child)
        if sort:
            self.sort_children()
    
    def add_children(self, children):
        for child in children:
            if isinstance(child, GameInterfaceComponent):
                self.add_child(child, sort=False)
        self.sort_children()
    
    def remove_child(self, child, sort=True):
        GameInterfaceComponent.validate_component(child)
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
    
    #GAMELOOP METHODS:
    def render(self, screen):
        super().render(screen)
        #Children should be rendered after the box itself
        for child in self.__children:
            if child.is_visible():
                child.render(screen)
    
    def handle_event(self, event, mouse_button_held):
        # Children might be interactive
        for child in self.__children:
            if child.is_active():
                if child.handle_event(event, mouse_button_held):
                    return True
        # Boxes themselves are non-interactive
        return False
    
    #MAIN UPDATE METHOD
    def update_component(self):
        for child in self.__children:
            child.update_component()
        super().update_component()
    
    # THE FOLLOWING ARE THE UPDATE METHODS - EACH CALLS UPDATE_COMPONENT AT THE END
    # EACH OF THESE METHODS INCLUDES A FLAG 'UPDATE_COMPONENT' THAT CAN BE SET TO FALSE
    # TO REDUCE REDUNDANT UPDATE_COMPONENT CALLS FOR CHILD ELEMENTS
    def update_position(self, new_position, relative = False, update_component = True):
        for child in self.__children:
            child.update_position(new_position=new_position, relative=relative, update_component=False)
        super().update_position(new_position=new_position, relative=relative, update_component=update_component)
    
    def move(self, movement=(0,0), update_component = True):
        self.update_position(movement, relative=True, update_component=update_component)

    def update_alpha(self, alpha, propogate_children = False, update_component = True):
        if propogate_children:
            for child in self.__children:
                if (hasattr(child, "update_alpha") and callable(getattr(child, "update_alpha"))):
                    if hasattr(child, "__children") or hasattr(child, "__styles"):
                        child.update_alpha(alpha, propogate_children=propogate_children, update_component=False)
                    else:
                        child.update_alpha(alpha, update_component=False)
        super().update_alpha(alpha, update_component=update_component)

    #THE FOLLOWING ARE ANY STATIC METHODS
    @staticmethod
    def create_text_box(name="Text_Box", priority=0, text="Text Box", position=(0,0), h_align=Alignment.MIDDLE, v_align=Alignment.MIDDLE, 
                        size=(1,1), padding=(4,2), box_color=(128,128,128), alpha=255, text_color=(255, 255, 255), text_size=36):
        # validate parameters
        # only parameters that aren't directly passed without
        # modification are validated to avoid redundant checks
        Validate.name(name)
        Validate.priority(priority)
        Validate.alignment(h_align)
        Validate.alignment(v_align)
        Validate.size(size)
        Validate.padding(padding)
        Validate.alpha(alpha)
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
        text_box = Box(name=name, priority=priority, position=box_pos, size=box_size, color=box_color, alpha=alpha, children=[label])
        #correctly center the label within the button
        text_box.position_component_relative(component=label, position=(50,50), percent_flag=True, h_align=Alignment.MIDDLE, v_align=Alignment.MIDDLE)
        return text_box
#imports
from src.validate import Validate
from src.alignment import Alignment
from src.gamestates import GameState
from src.gameinterface import GameInterface
from src.gameinterfacecomponent import GameInterfaceComponent
from src.box import Box
from src.button import Button
from src.label import Label

class GameInterfaceManager():
    def __init__(self, screen_size):
        self.init_dimensions(screen_size)
        self.init_interfaces()

    #SCREEN DIMENSIONS METHODS:
    def init_dimensions(self, screen_size):
        self.__screen_positions = {
            "left" : 0,
            "top" : 0,
            "center_x" : screen_size[0] // 2,
            "center_y" : screen_size[1] // 2,
            "right" : screen_size[0],
            "bottom" : screen_size[1]
        }
        self.__tithe = {
            "x" : screen_size[0] // 10,
            "y" : screen_size[1] // 10
        }

    #INTERFACES METHODS:
    def init_interfaces(self):
        self.__interfaces = {
            GameState.MENU : self.init_menu_interface(),
            GameState.PLAY : self.init_gameplay_interface(),
            GameState.PAUSE : self.init_gamepause_interface(),
            GameState.END : self.init_gameover_interface()
        }
    
    def get_interface(self, state):
        return self.__interfaces[state]
    
    def get_all(self):
        return self.__interfaces

    def init_menu_interface(self):
        menu_interface = GameInterface(priority=0)
        # menu screen title:
        menu_title = self.create_title(title_name = "Menu", title_text = "TriVasion!", bg_color = (100, 100, 100), text_size = 64)
        # menu options panel: 
        menu_options_panel = self.create_options_panel()
        # menu buttons:
        menu_start_button = Button.quick_create(
            name = "Menu_Start_Button", 
            text = "Start Game", 
            position = self.multiply_tithes(8, 5), 
            v_align = Alignment.END,
            size = self.multiply_tithes()
        )
        menu_quit_button = Button.quick_create(
            name = "Menu_Quit_Button", 
            text = "Quit Game", 
            position = self.multiply_tithes(8, 7), 
            v_align = Alignment.START,
            size = self.multiply_tithes()
        )
        # add components to interface and return:
        menu_interface.add_components([
            menu_title, 
            menu_options_panel,
            menu_start_button,
            menu_quit_button
        ])
        return menu_interface

    def init_gameplay_interface(self):
        gameplay_interface = GameInterface(priority=0)
        # tower picker panel:
        tower_picker_panel = self.create_towers_panel()
        # game information panel:
        information_panel = self.create_information_panel()
        # add components to interface and return:
        gameplay_interface.add_components([
            tower_picker_panel,
            information_panel
        ])
        return gameplay_interface

    def init_gamepause_interface(self):
        gamepause_interface = GameInterface(priority=10)
        # gamepause screen overlay:
        gamepause_background = self.create_background(name = "Gamepause_Background")
        # gamepause title:
        gamepause_title = self.create_title(
            title_name = "Gamepause", 
            title_text = "Game Paused", 
            bg_color = (64, 64, 64), 
            text_color = (200, 200, 200),
            text_size = 50
        )
        # resume game button:
        gamepause_resume_button = Button.quick_create(
            name = "Gamepause_Resume_Button", 
            priority = 1, 
            text = "Resume Game", 
            position = (
                self.__screen_positions["center_x"], 
                self.__screen_positions["center_y"] 
            ), 
            padding = (10, 5), 
            button_color = (0, 1, 0)
        )
        # add components to interface and return:
        gamepause_interface.add_components([
            gamepause_background,
            gamepause_title,
            gamepause_resume_button
        ])
        return gamepause_interface

    def init_gameover_interface(self):
        gameover_interface = GameInterface(priority=10)
        # gameover screen overlay:
        gameover_background = self.create_background(name = "Gameover_Background")
        # gameover title:
        gameover_title = self.create_title(
            title_name = "Gameover", 
            title_text = "Game Over", 
            bg_color = (64, 64, 64), 
            text_color = (200, 200, 200),
            text_size = 50
        )
        # retry button:
        gameover_retry_button = Button.quick_create(
            name = "Gameover_Retry_Button", 
            priority = 1, 
            text = "Try Again", 
            position = (
                self.__screen_positions["center_x"], 
                self.__screen_positions["center_y"] 
            ), 
            padding = (10, 5), 
            button_color = (0, 1, 0)
        )
        # add components to interface and return:
        gameover_interface.add_components([
            gameover_background,
            gameover_title,
            gameover_retry_button
        ])
        return gameover_interface

    #GAMELOOP METHODS:
    def render(self, screen):
        for interface in self.__interfaces.values():
            if interface.is_visible():
                interface.render(screen)

    def handle_event(self, event, mouse_button_held):
        for interface in self.__interfaces.values():
            if interface.is_active():
                if interface.handle_event(event, mouse_button_held):
                    return True
        return False

    #GENERAL INTERFACE HELPERS:
    def multiply_tithes(self, x_multiplier = 1, y_multiplier = 1):
        return (
            round(self.__tithe["x"] * x_multiplier),
            round(self.__tithe["y"] * y_multiplier)
        )
    
    def generate_element_position(self, init_position = (0, 0), offset = (0, 0)):
        return (
            init_position[0] + offset[0],
            init_position[1] + offset[1]
        )

    def generate_title_position(self):
        return (
            self.__screen_positions["center_x"], 
            self.__tithe["y"]
        )
    
    def generate_title_dimension(self):
        return (
            self.__screen_positions["right"], 
            self.__tithe["y"]
        )
    
    def create_title(self, title_name, title_text, priority = 1, bg_color = (100, 100, 100), text_color = (255, 255, 255), text_size = 64):
        return Box.create_text_box(
            name = f"{title_name}_Title", 
            priority = priority,
            text = title_text, 
            position = self.generate_title_position(), 
            v_align = Alignment.START, 
            size = self.generate_title_dimension(), 
            box_color = bg_color, 
            text_color = text_color, 
            text_size = text_size
        )
    
    def create_background(self, name = "Background", color = (0, 0, 0), transparency = 128):
        return Box(
            name = name, 
            priority = 0, 
            position = (
                self.__screen_positions["left"], 
                self.__screen_positions["top"]
            ), 
            size = (
                self.__screen_positions["right"], 
                self.__screen_positions["bottom"]
            ), 
            color = color,
            alpha = transparency
        )

    #MENU INTERFACE HELPERS:
    def generate_options_row_position(self, row):
        row += 2
        return self.multiply_tithes(y_multiplier=row)

    def generate_options_row_dimension(self):
        return self.multiply_tithes(x_multiplier=5)

    def generate_options_row(self, option, row, bg_color = (255, 0, 0), label_color = (0, 0, 228), transparency = 128, text_size = 30):
        # options row container
        row_position = self.generate_options_row_position(row)
        options_row = Box(
            name = f"Menu_Options_{option}_Row",
            position = row_position,
            size = self.generate_options_row_dimension(),
            color = bg_color,
            alpha = transparency
        )
        # options row title:
        title = Box.create_text_box(
            name = f"Menu_Options_{option}_Title", 
            priority = 1,
            text = f"{option}:", 
            position = self.generate_element_position(init_position=row_position, offset=self.multiply_tithes(1, 0)), 
            v_align = Alignment.START, 
            size = self.multiply_tithes(x_multiplier = 2),
            box_color = label_color, 
            alpha = transparency, 
            text_size = text_size
        )
        # options row selected:
        selected = Box.create_text_box(
            name = f"Menu_Options_{option}_Selected", 
            priority = 1,
            text = option, 
            position = self.generate_element_position(init_position=row_position, offset=self.multiply_tithes(4, 0)), 
            v_align = Alignment.START, 
            size = self.multiply_tithes(),
            box_color = label_color, 
            alpha = transparency, 
            text_size = text_size
        )
        # options row previous button: 
        previous_button = Button.quick_create(
            name = f"Menu_Options_{option}_Previous_Button", 
            text = "<", 
            position = self.generate_element_position(init_position=row_position, offset=self.multiply_tithes(3, 0)), 
            h_align = Alignment.START, 
            v_align = Alignment.START, 
            size = self.multiply_tithes(x_multiplier = 0.5)
        )
        # options row next button:
        next_button = Button.quick_create(
            name = f"Menu_Options_{option}_Next_Button", 
            text = ">", 
            position = self.generate_element_position(init_position=row_position, offset=self.multiply_tithes(5, 0)), 
            h_align = Alignment.END, 
            v_align = Alignment.START, 
            size = self.multiply_tithes(x_multiplier = 0.5)
        )
        # finalize and return
        options_row.add_children([
            title,
            selected,
            previous_button,
            next_button
        ])
        return options_row

    def create_options_panel(self):
        # options panel
        options_panel = Box(
            name = "Menu_Options_Panel",
            position = self.multiply_tithes(1, 3),
            size = self.multiply_tithes(5, 6),
            color = (255, 64, 64)
        )
        # options panel title
        options_panel_title = Box.create_text_box(
            name = "Menu_Options_Panel_Title", 
            text = "Options", 
            position = self.multiply_tithes(2.5, 2), 
            h_align = Alignment.START, 
            v_align = Alignment.START, 
            size = self.multiply_tithes(2, 1), 
            box_color = (0, 0, 228), 
            text_size = 42
        )
        # options panel save button
        options_panel_save = Button.quick_create(
            name = "Menu_Options_Panel_Save", 
            text = "Save", 
            position = self.multiply_tithes(2.5, 9), 
            h_align = Alignment.START, 
            v_align = Alignment.START, 
            size = self.multiply_tithes(2, 1)
        )
        # options panel rows
        options_waves_row = self.generate_options_row("Waves", 1)
        options_difficulty_row = self.generate_options_row("Difficulty", 2)
        options_volume_row = self.generate_options_row("Volume", 3)
        options_fullscreen_row = self.generate_options_row("Fullscreen", 4)
        options_resolution_row = self.generate_options_row("Resolution", 5)
        options_fps_row = self.generate_options_row("Fps", 6)
        # add components to options_panel
        options_panel.add_children([
            options_panel_title,
            options_panel_save,
            options_waves_row,
            options_difficulty_row,
            options_volume_row,
            options_fullscreen_row,
            options_resolution_row,
            options_fps_row
        ])
        return options_panel

    #GAMEPLAY INTERFACE HELPERS:
    def generate_tower_picker(self, pos, name, cost):
        #Tower Picker Button
        picker_button = Button.quick_create(
            name = f"{name}_Tower_Picker", 
            text = f"{name} Tower", 
            position = self.multiply_tithes(9, (2 * pos - 1)), 
            size = self.multiply_tithes()
        )
        #Tower Cost Label
        cost_label = Box.create_text_box(
            name = f"{name}_Tower_Cost", 
            text = f"Cost: {cost}", 
            position = self.multiply_tithes(9, (2 * pos)),
            v_align = Alignment.END, 
            size = self.multiply_tithes(1, 0.5), 
            box_color = (0, 0, 0), 
            alpha = 128, 
            text_color = (255, 255, 255), 
            text_size = 24
        )

        return [picker_button, cost_label]

    def create_towers_panel(self):
        # Tower Panel
        tower_panel = Box(
            name = "Tower_Panel", 
            priority = 1, 
            position = self.multiply_tithes(8, 0),
            size = self.multiply_tithes(2, 8),
            color = (0, 0, 0),
            alpha = 255
        )
        # Circle Tower
        tower_panel.add_children(self.generate_tower_picker(1, "Circle", 10))
        # Square Tower
        tower_panel.add_children(self.generate_tower_picker(2, "Square", 25))
        # Hexagon Tower
        tower_panel.add_children(self.generate_tower_picker(3, "Hexagon", 25))
        # Octagon Tower
        tower_panel.add_children(self.generate_tower_picker(4, "Octagon", 50))
        # Return Tower Panel
        return tower_panel

    def generate_information_label(self, name, text, row=0, col=0, width=1, height=1, label_color=(0, 0, 0), 
                                   transparency=255, text_color=(255, 255, 255), text_size=30):
        row += 8
        label_position = self.multiply_tithes(col, row)
        label_size = self.multiply_tithes(width, height)
        return Box.create_text_box(
            name = name, 
            text = text, 
            position = label_position, 
            h_align = Alignment.START, 
            v_align = Alignment.START, 
            size = label_size, 
            box_color = label_color, 
            alpha = transparency, 
            text_color = text_color, 
            text_size = text_size
        )

    def generate_information_button(self, name, text, row=0, col=0, width=1, height=1, padding = (4, 2)):
        row += 8
        button_position = self.multiply_tithes(col, row)
        button_size = self.multiply_tithes(width, height)
        return Button.quick_create(
            name = name, 
            text = text, 
            position = button_position, 
            h_align = Alignment.START, 
            v_align = Alignment.START, 
            size = button_size,
            padding = padding
        )

    def create_information_panel(self):
        # Information Panel
        information_panel = Box(
            name = "Information_Panel", 
            priority = 1, 
            position = self.multiply_tithes(0, 8),
            size = self.multiply_tithes(10, 2),
            color = (0, 0, 0),
            alpha = 255
        )
        # Lives Label
        lives_Label = self.generate_information_label("Lives_Label", "Lives: 10", width=3)
        # Credits Label
        credits_label = self.generate_information_label("Credits_Label", "Credits: 100", row=1, width=3)
        # Play Pause Button
        playpause_button = self.generate_information_button("Playpause_Button", "||", col=4)
        # Fast Forward Button
        fastforward_button = self.generate_information_button("Fastforward_Button", ">>", col=5)
        # Waves Label
        waves_Label = self.generate_information_label("Waves_Label", "Wave: 1/10", row=1, col=4, width=2)
        # Main Menu Button
        main_manu_button = self.generate_information_button("Main_Menu_Button", "Main Menu", col=7, width=3)
        # Quit Game Button
        quit_game_button = self.generate_information_button("Quit_Game_Button", "Quit Game", row=1, col=7, width=3)
        # Add Information Panel Components and return
        information_panel.add_children([
            lives_Label,
            credits_label,
            playpause_button,
            fastforward_button,
            waves_Label,
            main_manu_button,
            quit_game_button
        ])
        return information_panel

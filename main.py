#imports
import pygame
from src.gamesettings import GameSettings
from src.gamestates import GameState
from src.gameinterface import GameInterface
from src.gameinterfacecomponent import GameInterfaceComponent
from src.alignment import Alignment
from src.label import Label
from src.box import Box
from src.buttonstate import ButtonState
from src.button import Button
from src.level import Level
from src.grid import Grid
from src.gridcell import GridCell

#globals
game_is_running = True
game_settings = GameSettings("settings", "DEFAULT_SETTINGS.json", "GAME_SETTINGS.json", "OPTIONS_SETTINGS.json")
current_state = GameState.START
pending_state = None
interfaces = {}
screen = None
clock = None
screen_positions = {
    "top" : None,
    "left" : None,
    "center_x" : None,
    "center_y" : None,
    "right" : None,
    "bottom" : None,
}
mouse_button_held = False
pause_keys = [pygame.K_p, pygame.K_ESCAPE]
level = None

#initializes the game. resets everything when called again later
def init_game():
    init_settings()
    init_interfaces()
    change_state(GameState.MENU)

#initializes the game's level
def init_level():
    global game_settings, level
    level = Level(waves=game_settings.get_setting("waves"), difficulty=game_settings.get_setting("difficulty"))

#initializes settings
def init_settings():
    global game_settings
    if not game_settings:
        game_settings = GameSettings("settings", "DEFAULT_SETTINGS.json", "GAME_SETTINGS.json", "OPTIONS_SETTINGS.json")
    game_settings.load_selected_options()

#initialize everything related to pygame
def init_pygame():
    global clock
    pygame.init()
    init_display()
    clock = pygame.time.Clock()

#(re)initialize the display and related variables
def init_display():
    global game_settings, screen, screen_positions
    fullscreen = game_settings.get_setting("fullscreen")
    resolution = game_settings.get_setting("resolution")
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode(resolution, flags)
    screen_positions = {
        "top" : 0,
        "left" : 0,
        "tithe_x" : resolution[0]//10,
        "tithe_y" : resolution[1]//10,
        "center_x" : resolution[0]//2,
        "center_y" : resolution[1]//2,
        "right" : resolution[0],
        "bottom" : resolution[1],
    }

#(re)set main menu interface
def init_menu_interface():
    def generate_options_row(option, row_number):
        global game_settings
        row_number += 2
        capitalized = option.capitalize()
        row = Box(
            name = f"Menu_Options_{capitalized}_Row",
            position = (
                screen_positions["tithe_x"],
                screen_positions["tithe_y"] * row_number
            ),
            size = (
                screen_positions["tithe_x"] * 5,
                screen_positions["tithe_y"]
            ),
            color = (255, 0, 0),
            alpha = 128
        )
        title = Box.create_text_box(
            name = f"Menu_Options_{capitalized}_Title", 
            priority = 1,
            text = f"{capitalized}:", 
            position = (
                screen_positions["tithe_x"] * 2,
                screen_positions["tithe_y"] * row_number
            ), 
            h_align = Alignment.MIDDLE, 
            v_align = Alignment.START, 
            size = (
                screen_positions["tithe_x"] * 2,
                screen_positions["tithe_y"]
            ), 
            padding = (4, 2), 
            box_color = (0, 0, 228), 
            alpha = 128, 
            text_size = 30
        )
        selected = Box.create_text_box(
            name = f"Menu_Options_{capitalized}_Selected", 
            priority = 1,
            text = game_settings.get_selected_option_text(option), 
            position = (
                screen_positions["tithe_x"] * 5,
                screen_positions["tithe_y"] * row_number
            ), 
            h_align = Alignment.MIDDLE, 
            v_align = Alignment.START, 
            size = (
                screen_positions["tithe_x"],
                screen_positions["tithe_y"]
            ), 
            padding = (4, 2), 
            box_color = (0, 0, 228), 
            alpha = 128, 
            text_size = 30
        )
        selected_label = selected.get_child(f"Menu_Options_{capitalized}_Selected_Label")
        previous_button = Button.quick_create(
            name = f"Menu_Options_{capitalized}_Previous_Button", 
            text = "<", 
            position = (
                screen_positions["tithe_x"] * 4,
                screen_positions["tithe_y"] * row_number
            ), 
            h_align = Alignment.START, 
            v_align = Alignment.START, 
            size = (
                screen_positions["tithe_x"]//2, 
                screen_positions["tithe_y"]
            ), 
            padding = (4, 2), 
            callback = lambda : selected_label.update_content(game_settings.select_previous_option(option))
        )
        next_button = Button.quick_create(
            name = f"Menu_Options_{capitalized}_Next_Button", 
            text = ">", 
            position = (
                screen_positions["tithe_x"] * 6,
                screen_positions["tithe_y"] * row_number
            ), 
            h_align = Alignment.END, 
            v_align = Alignment.START, 
            size = (
                screen_positions["tithe_x"]//2, 
                screen_positions["tithe_y"]
            ), 
            padding = (4, 2), 
            callback = lambda : selected_label.update_content(game_settings.select_next_option(option))
        )
        row.add_children([
            title,
            selected,
            previous_button,
            next_button
        ])
        return row
    
    global screen_positions, game_settings
    menu_interface = GameInterface(priority=0)

    #menu title stuff
    menu_title_box = Box.create_text_box(
        name = "Menu_Title_Box", 
        text = "TriVasion!", 
        position = (
            screen_positions["center_x"],
            screen_positions["tithe_y"]
        ), 
        v_align = Alignment.START, 
        size = (
            screen_positions["right"], 
            screen_positions["tithe_y"]
        ), 
        padding = (10, 5), 
        box_color = (100, 100, 100), 
        text_size = 64
    )

    # menu options panel: 
    # options_title 
    menu_options_title = Box.create_text_box(
        name = "Menu_Options_Title", 
        text = "Options", 
        position = (
            screen_positions["center_x"]//2,
            screen_positions["tithe_y"]*2
        ), 
        h_align = Alignment.START, 
        v_align = Alignment.START, 
        size = (
            screen_positions["tithe_x"]*2,
            screen_positions["tithe_y"]
        ), 
        padding = (4, 2), 
        box_color = (0, 0, 228), 
        text_size = 42
    )
    # options_panel 
    menu_options_panel = Box(
        name = "Menu_Options_Panel",
        position = (
            screen_positions["tithe_x"],
            screen_positions["tithe_y"] * 3
        ),
        size = (
            screen_positions["tithe_x"] * 5,
            screen_positions["tithe_y"] * 6
        ),
        color = (255, 64, 64)
    )
    # save options button
    menu_options_save_button = Button.quick_create(
        name = "Menu_Options_Save_Button", 
        text = "Save", 
        position = (
            screen_positions["center_x"]//2,
            screen_positions["tithe_y"] * 9
        ), 
        h_align = Alignment.START, 
        v_align = Alignment.START, 
        size = (
            screen_positions["tithe_x"]*2, 
            screen_positions["tithe_y"]
        ), 
        padding = (4, 2), 
        callback = lambda : game_settings.apply_selection_options()
    )
    # options_waves 
    menu_options_waves_row = generate_options_row("waves", 1)
    # options_difficulty 
    menu_options_difficulty_row = generate_options_row("difficulty", 2)
    # options_volume 
    menu_options_volume_row = generate_options_row("volume", 3)
    # options_fullscreen 
    menu_options_fullscreen_row = generate_options_row("fullscreen", 4)
    # options_resolution 
    menu_options_resolution_row = generate_options_row("resolution", 5)
    # options_fps
    menu_options_fps_row = generate_options_row("fps", 6)
    # add components to menu_options_panel
    menu_options_panel.add_children([
        menu_options_waves_row,
        menu_options_difficulty_row,
        menu_options_volume_row,
        menu_options_fullscreen_row,
        menu_options_resolution_row,
        menu_options_fps_row
    ])

    #menu buttons
    menu_start_button = Button.quick_create(
        name = "Menu_Start_Button", 
        text = "Start Game", 
        position = (
            screen_positions["right"] - (screen_positions["tithe_x"] * 2), 
            screen_positions["center_y"]
        ), 
        v_align = Alignment.END,
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"]
        ), 
        padding = (10, 5), 
        callback = lambda: queue_state(GameState.PLAY)
    )
    menu_quit_button = Button.quick_create(
        name = "Menu_Quit_Button", 
        text = "Quit Game", 
        position = (
            screen_positions["right"] - (screen_positions["tithe_x"] * 2), 
            screen_positions["center_y"] + (screen_positions["tithe_y"] * 2)
        ), 
        v_align = Alignment.START,
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"]
        ), 
        padding = (10, 5), 
        callback = lambda: queue_state(GameState.QUIT)
    )

    #add components to interface
    menu_interface.add_components([
        menu_title_box, 
        menu_options_title, 
        menu_options_panel, 
        menu_options_save_button, 
        menu_start_button, 
        menu_quit_button
    ])
    return menu_interface

#(re)set gameplay interface
def init_gameplay_interface():
    global screen_positions, game_settings
    gameplay_interface = GameInterface(priority=0)

    #gameplay grid
    #gameplay_grid = Grid(name="Gameplay_Grid", position=(0, 0), grid_size=(20, 12), cell_size=(32, 32))
    #gameplay_interface.set_grid(gameplay_grid)

    #Tower Panel
    tower_panel = Box(
        name="Tower_Panel", 
        priority=1, 
        position=(
            screen_positions["tithe_x"] * 8, 
            0
        ),
        size=(
            screen_positions["tithe_x"] * 2, 
            screen_positions["tithe_y"] * 8
        ),
        color=(100, 100, 100),
        alpha=128
    )
    # Circle Tower Button
    circle_tower_picker = Button.quick_create(
        name = "Circle_Tower_Picker", 
        text = "Circle Tower", 
        position = (
            screen_positions["tithe_x"] * 9, 
            screen_positions["tithe_y"]
        ), 
        h_align = Alignment.MIDDLE, 
        v_align = Alignment.MIDDLE, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"]
        ),
        callback = None
    )
    # Circle Tower Cost Label
    circle_tower_cost = Box.create_text_box(
        name = "Circle_Tower_Cost", 
        text = "Cost: 10", 
        position = (
            screen_positions["tithe_x"] * 9, 
            screen_positions["tithe_y"] * 2
        ), 
        h_align = Alignment.MIDDLE, 
        v_align = Alignment.END, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"] // 2
        ), 
        box_color = (0, 0, 0), 
        alpha = 128, 
        text_color = (255, 255, 255), 
        text_size = 24
    )
    # Square Tower Button
    square_tower_picker = Button.quick_create(
        name = "Square_Tower_Picker", 
        text = "Square Tower", 
        position = (
            screen_positions["tithe_x"] * 9, 
            screen_positions["tithe_y"] * 3
        ), 
        h_align = Alignment.MIDDLE, 
        v_align = Alignment.MIDDLE, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"]
        ),
        callback = None
    )
    # Square Tower Cost Label
    square_tower_cost = Box.create_text_box(
        name = "Square_Tower_Cost", 
        text = "Cost: 25", 
        position = (
            screen_positions["tithe_x"] * 9, 
            screen_positions["tithe_y"] * 4
        ), 
        h_align = Alignment.MIDDLE, 
        v_align = Alignment.END, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"] // 2
        ), 
        box_color = (0, 0, 0), 
        alpha = 128, 
        text_color = (255, 255, 255), 
        text_size = 24
    )
    # Hexagon Tower Button
    hexagon_tower_picker = Button.quick_create(
        name = "Hexagon_Tower_Picker", 
        text = "Hexagon Tower", 
        position = (
            screen_positions["tithe_x"] * 9, 
            screen_positions["tithe_y"] * 5
        ), 
        h_align = Alignment.MIDDLE, 
        v_align = Alignment.MIDDLE, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"]
        ),
        callback = None
    )
    # Hexagon Tower Cost Label
    hexagon_tower_cost = Box.create_text_box(
        name = "Hexagon_Tower_Cost", 
        text = "Cost: 25", 
        position = (
            screen_positions["tithe_x"] * 9, 
            screen_positions["tithe_y"] * 6
        ), 
        h_align = Alignment.MIDDLE, 
        v_align = Alignment.END, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"] // 2
        ), 
        box_color = (0, 0, 0), 
        alpha = 128, 
        text_color = (255, 255, 255), 
        text_size = 24
    )
    # Octagon Tower Button
    octagon_tower_picker = Button.quick_create(
        name = "Octagon_Tower_Picker", 
        text = "Octagon Tower", 
        position = (
            screen_positions["tithe_x"] * 9, 
            screen_positions["tithe_y"] * 7
        ), 
        h_align = Alignment.MIDDLE, 
        v_align = Alignment.MIDDLE, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"]
        ),
        callback = None
    )
    # Octagon Tower Cost Label
    octagon_tower_cost = Box.create_text_box(
        name = "Octagon_Tower_Cost", 
        text = "Cost: 50", 
        position = (
            screen_positions["tithe_x"] * 9, 
            screen_positions["tithe_y"] * 8
        ), 
        h_align = Alignment.MIDDLE, 
        v_align = Alignment.END, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"] // 2
        ), 
        box_color = (0, 0, 0), 
        alpha = 128, 
        text_color = (255, 255, 255), 
        text_size = 24
    )
    # Add Tower Panel Components
    tower_panel.add_children([
        circle_tower_picker,
        circle_tower_cost,
        square_tower_picker,
        square_tower_cost,
        hexagon_tower_picker,
        hexagon_tower_cost,
        octagon_tower_picker,
        octagon_tower_cost
    ])

    #Information Panel
    information_panel = Box(
        name="Information_Panel", 
        priority=1, 
        position=(
            0, 
            screen_positions["tithe_y"] * 8
        ),
        size=(
            screen_positions["right"], 
            screen_positions["tithe_y"] * 2
        ),
        color=(100, 100, 100),
        alpha=128
    )
    # Lives Label
    lives_label = Box.create_text_box(
        name = "Lives_Label", 
        text = "Lives: 10", 
        position = (
            0, 
            screen_positions["tithe_y"] * 8
        ), 
        h_align = Alignment.START, 
        v_align = Alignment.START, 
        size = (
            screen_positions["tithe_x"] * 3, 
            screen_positions["tithe_y"]
        ), 
        box_color = (0, 0, 0), 
        alpha = 128, 
        text_color = (255, 255, 255), 
        text_size = 30
    )
    # Credits Label
    credits_label = Box.create_text_box(
        name = "Credits_Label", 
        text = "Credits: 100", 
        position = (
            0, 
            screen_positions["tithe_y"] * 9
        ), 
        h_align = Alignment.START, 
        v_align = Alignment.START, 
        size = (
            screen_positions["tithe_x"] * 3, 
            screen_positions["tithe_y"]
        ), 
        box_color = (0, 0, 0), 
        alpha = 128, 
        text_color = (255, 255, 255), 
        text_size = 30
    )
    # Play Pause Button
    play_pause_button = Button.quick_create(
        name = "Play_Pause_Button", 
        text = "||", 
        position = (
            screen_positions["tithe_x"] * 4, 
            screen_positions["tithe_y"] * 8
        ), 
        h_align = Alignment.START, 
        v_align = Alignment.START, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"]
        ),
        padding = (4, 2), 
        callback = lambda: queue_state(GameState.PAUSE)
    )
    # Fast Forward Button
    fast_forward_button = Button.quick_create(
        name = "Fast_Foward_Button", 
        text = ">>", 
        position = (
            screen_positions["tithe_x"] * 5, 
            screen_positions["tithe_y"] * 8
        ), 
        h_align = Alignment.START, 
        v_align = Alignment.START, 
        size = (
            screen_positions["tithe_x"], 
            screen_positions["tithe_y"]
        ),
        padding = (4, 2), 
        callback = None
    )
    # Waves Label
    waves_label = Box.create_text_box(
        name = "Waves_Label", 
        text = "Wave: 1/10", 
        position = (
            screen_positions["tithe_x"] * 4, 
            screen_positions["tithe_y"] * 9
        ), 
        h_align = Alignment.START, 
        v_align = Alignment.START, 
        size = (
            screen_positions["tithe_x"] * 2, 
            screen_positions["tithe_y"]
        ), 
        box_color = (0, 0, 0), 
        alpha = 128, 
        text_color = (255, 255, 255), 
        text_size = 24
    )
    # Main Menu Button
    main_menu_button = Button.quick_create(
        name = "Main_Menu_Button", 
        text = "Main Menu", 
        position = (
            screen_positions["tithe_x"] * 7, 
            screen_positions["tithe_y"] * 8
        ), 
        h_align = Alignment.START, 
        v_align = Alignment.START, 
        size = (
            screen_positions["tithe_x"] * 3, 
            screen_positions["tithe_y"]
        ),
        padding = (4, 2), 
        callback = lambda: queue_state(GameState.START)
    )
    # Quit Game Button
    quit_game_button = Button.quick_create(
        name = "Quit_Game_Button", 
        text = "Quit Game", 
        position = (
            screen_positions["tithe_x"] * 7, 
            screen_positions["tithe_y"] * 9
        ), 
        h_align = Alignment.START, 
        v_align = Alignment.START, 
        size = (
            screen_positions["tithe_x"] * 3, 
            screen_positions["tithe_y"]
        ),
        padding = (4, 2), 
        callback = lambda: queue_state(GameState.QUIT)
    )
    # Add Information Panel Components
    information_panel.add_children([
        lives_label,
        credits_label,
        play_pause_button,
        fast_forward_button,
        waves_label,
        main_menu_button,
        quit_game_button
    ])

    #add components to interface
    gameplay_interface.add_components([
        tower_panel,
        information_panel
    ])

    return gameplay_interface

#(re)set paused game interface overlay
def init_gamepause_interface():
    global screen_positions
    gamepause_interface = GameInterface(priority=10)

    #gamepause screen overlay
    gamepause_background_box = Box(
        name = "Gamepause_Background", 
        priority = 0, 
        position = (
            screen_positions["left"], 
            screen_positions["top"]
        ), 
        size = (
            screen_positions["right"], 
            screen_positions["bottom"]
        ), 
        color = (0, 0, 0),
        alpha = 128
    )

    #gamepause title stuff
    gamepause_title_box = Box.create_text_box(
        name = "Gamepause_Title_Box", 
        priority = 1, 
        text = "Game Paused", 
        position = (
            screen_positions["center_x"], 
            50
        ), 
        v_align = Alignment.START, 
        size = (
            screen_positions["right"], 
            50
        ), 
        padding = (10, 5), 
        box_color = (64, 64, 64), 
        text_color = (200, 200, 200),
        text_size = 50
    )

    #gameplay button stuff
    gamepause_resume_button = Button.quick_create(
        name = "Gamepause_Resume_Button", 
        priority = 1, 
        text = "Resume Game", 
        position = (
            screen_positions["center_x"], 
            screen_positions["center_y"] 
        ), 
        padding = (10, 5), 
        button_color = (0, 1, 0), 
        callback = lambda: queue_state(GameState.PLAY)
    )
    
    #add components to interface
    gamepause_interface.add_components([
        gamepause_background_box,
        gamepause_title_box,
        gamepause_resume_button
    ])
    return gamepause_interface

#(re)set game-over interface overlay
def init_gameover_interface():
    global screen_positions
    gameover_interface = GameInterface(priority=10)

    #gamepause screen overlay
    gameover_background_box = Box(
        name = "Gameover_Background", 
        priority = 0, 
        position = (
            screen_positions["left"], 
            screen_positions["top"]
        ), 
        size = (
            screen_positions["right"], 
            screen_positions["bottom"]
        ), 
        color = (0, 0, 0),
        alpha = 128
    )

    #gamepause title stuff
    gameover_title_box = Box.create_text_box(
        name = "Gameover_Title_Box", 
        priority = 1, 
        text = "Game Over", 
        position = (
            screen_positions["center_x"], 
            50
        ), 
        v_align = Alignment.START, 
        size = (
            screen_positions["right"], 
            50
        ), 
        padding = (10, 5), 
        box_color = (64, 64, 64), 
        text_color = (200, 200, 200),
        text_size = 50
    )

    #gameplay button stuff
    gameover_retry_button = Button.quick_create(
        name = "Gameover_Retry_Button", 
        priority = 1, 
        text = "Try Again", 
        position = (
            screen_positions["center_x"], 
            screen_positions["center_y"] 
        ), 
        padding = (10, 5), 
        button_color = (0, 1, 0), 
        callback = lambda: queue_state(GameState.START)
    )

    #add components to interface
    gameover_interface.add_components([
        gameover_background_box,
        gameover_title_box,
        gameover_retry_button
    ])
    return gameover_interface

#(re)set all interfaces
def init_interfaces():
    global interfaces
    interfaces = {
        GameState.MENU : init_menu_interface(),
        GameState.PLAY : init_gameplay_interface(),
        GameState.PAUSE : init_gamepause_interface(),
        GameState.END : init_gameover_interface()
    }

#helper function to access specific interface
def get_interface(state):
    global interfaces
    return interfaces.get(state, None)

def queue_state(new_state):
    global pending_state
    pending_state = new_state

#direct gameflow
def change_state(new_state):
    global game_is_running, current_state

    #quick check to see if this is even necessary
    if current_state == new_state:
        return
    
    #various game screens
    menu = get_interface(GameState.MENU)
    gameplay = get_interface(GameState.PLAY)
    gamepause = get_interface(GameState.PAUSE)
    gameover = get_interface(GameState.END)

    #switch to new state
    previous_state = current_state
    current_state = new_state
    if current_state == GameState.QUIT:
        game_is_running = False
    elif current_state == GameState.START:
        init_game()
    elif current_state == GameState.MENU:
        menu.show()
        menu.activate()
    elif current_state == GameState.PLAY:
        if previous_state == GameState.MENU:
            menu.hide()
            menu.deactivate()
            init_level()
        elif previous_state == GameState.PAUSE:
            gamepause.deactivate()
            gamepause.hide()
        gameplay.show()
        gameplay.activate()
    elif current_state == GameState.PAUSE:
        gameplay.deactivate()
        gamepause.show()
        gamepause.activate()
    elif current_state == GameState.END:
        gameplay.deactivate()
        gameover.show()
        gameover.activate()

#called during gameloop to handle events
def handle_events():
    global game_is_running, pending_state, interfaces, mouse_button_held, pause_keys, current_state
    for event in pygame.event.get():
        event_consumed = False
        if event.type == pygame.QUIT:
            game_is_running = False
            return
        if event.type == pygame.KEYDOWN:
            if event.key in pause_keys and current_state == GameState.PLAY:
                queue_state(GameState.PAUSE)
                event_consumed = True
        #Ensure only first frame of MOUSEBUTTONDOWN is processed
        toggle_mouse_state = (
            (event.type == pygame.MOUSEBUTTONDOWN and not mouse_button_held) or 
            (event.type == pygame.MOUSEBUTTONUP and mouse_button_held)
        )

        if level and not event_consumed:
            event_consumed = level.handle_event(event, mouse_button_held)
        
        for interface in interfaces.values():
            if interface.is_active() and not event_consumed:
                event_consumed = interface.handle_event(event, mouse_button_held)
        
        #Mouse state is toggled after event is consumed
        if toggle_mouse_state:
            mouse_button_held = not mouse_button_held
        
        #resolve state changes after events are handled
        if pending_state:
            change_state(pending_state)
            pending_state = None

#called during gameloop to render the game
def render_game():
    global screen, interfaces, current_state

    #reset screen
    screen.fill("black")

    #render game grid first
    if current_state == GameState.PLAY or current_state == GameState.PAUSE or current_state == GameState.END:
        level.render(screen)
    
    #render interfaces on top
    for i in interfaces:
        if interfaces[i].is_visible():
            interfaces[i].render(screen)
    
    #finish rendering
    pygame.display.flip()

#called during gameloop to update in-game logic
def update_game(delta_time):
    global current_state, level
    if current_state == GameState.PLAY:
        level.update(delta_time)

#main program, contains the gameloop
def main():
    global game_is_running, game_settings, clock, pending_state
    init_pygame()
    init_game()

    #game loop
    while game_is_running:
        #events
        handle_events()
        #tick update logic
        update_game(clock.get_time())
        #draw update logic
        render_game()
        
        #limit tickrate
        clock.tick(game_settings.get_setting("fps"))
    quit_game()

#called when game ends
def quit_game():
    pygame.quit()

#ensure that main program is called
if __name__ == "__main__":
    main()
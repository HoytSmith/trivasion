#imports
import pygame
from src.gamesettings import GameSettings
from src.gamestates import GameState
from src.gameinterface import GameInterface
from src.gameinterfacecomponent import GameInterfaceComponent
from src.gameinterfacemanager import GameInterfaceManager
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
    "tithe_x" : None,
    "tithe_y" : None,
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

#called when settings are changed
def save_options():
    global game_settings, current_state
    changed_flags = game_settings.apply_selection_options()
    if changed_flags["fullscreen"] or changed_flags["resolution"]:
        init_display()
        init_interfaces()
        change_state(current_state)

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

#(re)set all interfaces
def init_interfaces():
    def implement_options_functionality(options_panel, option):
        def update_options_label(label, selected, new_content):
            label.update_content(new_content)
            selected.position_component_relative(
                component=label, 
                position=(50,50), 
                percent_flag=True, 
                h_align=Alignment.MIDDLE, 
                v_align=Alignment.MIDDLE
            )
            #End of this function
        global game_settings
        #prepare
        prefix = f"Menu_Options_{option.capitalize()}"
        option_row = options_panel.get_child(f"{prefix}_Row")
        option_selected = option_row.get_child(f"{prefix}_Selected")
        #setup label
        option_label = option_selected.get_child(f"{prefix}_Selected_Label")
        update_options_label(option_label, option_selected, game_settings.get_selected_option_text(option))
        #previous button
        option_previous = option_row.get_child(f"{prefix}_Previous_Button")
        option_previous.set_callback(
            lambda: update_options_label(option_label, option_selected, game_settings.select_previous_option(option))
        )
        #next button
        option_next = option_row.get_child(f"{prefix}_Next_Button")
        option_next.set_callback(
            lambda: update_options_label(option_label, option_selected, game_settings.select_next_option(option))
        )
        #End of this function
    global interfaces, game_settings
    interfaces = GameInterfaceManager(game_settings.get_setting("resolution"))
    
    # IMPLEMENT FUNCTIONALITY:
    # MAIN MENU INTERFACE:
    menu_interface = interfaces.get_interface(GameState.MENU)
    # Menu Options Panel                    ("Menu_Options_Panel")
    menu_options_panel = menu_interface.get_component("Menu_Options_Panel")
    
    # WAVES OPTION FUNCTIONALITY:
    implement_options_functionality(menu_options_panel, "waves")
    # DIFFICULTY OPTION FUNCTIONALITY:
    implement_options_functionality(menu_options_panel, "difficulty")
    # VOLUME OPTION FUNCTIONALITY:
    implement_options_functionality(menu_options_panel, "volume")
    # FULLSCREEN OPTION FUNCTIONALITY:
    implement_options_functionality(menu_options_panel, "fullscreen")
    # RESOLUTION OPTION FUNCTIONALITY:
    implement_options_functionality(menu_options_panel, "resolution")
    # FPS OPTION FUNCTIONALITY:
    implement_options_functionality(menu_options_panel, "fps")

    # Options Panel Save Button             ("Menu_Options_Panel_Save")
    options_panel_save = menu_options_panel.get_child("Menu_Options_Panel_Save")
    options_panel_save.set_callback(
        lambda : save_options()
    )
    # Start Game Button                     ("Menu_Start_Button")
    menu_start_game = menu_interface.get_component("Menu_Start_Button")
    menu_start_game.set_callback(
        lambda: queue_state(GameState.PLAY)
    )
    # Quit Game Button                      ("Menu_Quit_Button")
    menu_quit_game = menu_interface.get_component("Menu_Quit_Button")
    menu_quit_game.set_callback(
        lambda: queue_state(GameState.QUIT)
    )

    # GAME PLAY INTERFACE:
    gameplay_interface = interfaces.get_interface(GameState.PLAY)

    # TOWERS PANEL FUNCTIONALITY:
    # Tower Picker Panel                    ("Tower_Panel")
    tower_panel = gameplay_interface.get_component("Tower_Panel")
    # Circle Tower Picker Button            ("Circle_Tower_Picker")     (NOT YET IMPLEMENTED)
    circle_tower_picker = tower_panel.get_child("Circle_Tower_Picker")
    # Square Tower Picker Button            ("Square_Tower_Picker")     (NOT YET IMPLEMENTED)
    square_tower_picker = tower_panel.get_child("Square_Tower_Picker")
    # Hexagon Tower Picker Button           ("Hexagon_Tower_Picker")    (NOT YET IMPLEMENTED)
    hexagon_tower_picker = tower_panel.get_child("Hexagon_Tower_Picker")
    # Octagon Tower Picker Button           ("Octagon_Tower_Picker")    (NOT YET IMPLEMENTED)
    octagon_tower_picker = tower_panel.get_child("Octagon_Tower_Picker")

    # INFORMATION PANEL FUNCTIONALITY:
    # Information Panel                     ("Information_Panel")
    information_panel = gameplay_interface.get_component("Information_Panel")
    # Playpause Button                      ("Playpause_Button")    (TO BE CHANGED?)
    gameplay_pause_button = information_panel.get_child("Playpause_Button")
    gameplay_pause_button.set_callback(
        lambda: queue_state(GameState.PAUSE)
    )
    # Fast Forward Button                   ("Fastforward_Button")    (NOT YET IMPLEMENTED)
    gameplay_fast_forward_button = information_panel.get_child("Fastforward_Button")
    # Main Menu Button                      ("Main_Menu_Button")
    gameplay_main_menu_button = information_panel.get_child("Main_Menu_Button")
    gameplay_main_menu_button.set_callback(
        lambda: queue_state(GameState.START)
    )
    # Quit Game Button                      ("Quit_Game_Button")
    gameplay_quit_game_button = information_panel.get_child("Quit_Game_Button")
    gameplay_quit_game_button.set_callback(
        lambda: queue_state(GameState.QUIT)
    )

    # GAMEPAUSE INTERFACE:
    gamepause_interface = interfaces.get_interface(GameState.PAUSE)
    # Resume Game Button
    gamepause_resume_button = gamepause_interface.get_component("Gamepause_Resume_Button")
    gamepause_resume_button.set_callback(
        lambda: queue_state(GameState.PLAY)
    )

    # GAME OVER INTERFACE:
    gameover_interface = interfaces.get_interface(GameState.END)
    # Retry Game Button
    gameover_retry_button = gameover_interface.get_component("Gameover_Retry_Button")
    gameover_retry_button.set_callback(
        lambda: queue_state(GameState.START)
    )

#helper function to access specific interface
def get_interface(state):
    global interfaces
    return interfaces.get_interface(state)

def queue_state(new_state):
    global pending_state
    pending_state = new_state

#direct gameflow
def change_state(new_state):
    global game_is_running, current_state
    
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
    elif current_state == GameState.PLAY:
        if previous_state == GameState.MENU:
            menu.hide()
            init_level()
        elif previous_state == GameState.PAUSE:
            gamepause.hide()
        gameplay.show()
    elif current_state == GameState.PAUSE:
        gameplay.deactivate()
        gamepause.show()
    elif current_state == GameState.END:
        gameplay.deactivate()
        gameover.show()

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
        
        if not event_consumed:
            event_consumed = interfaces.handle_event(event, mouse_button_held)
        #for interface in interfaces.values():
        #    if interface.is_active() and not event_consumed:
        #        event_consumed = interface.handle_event(event, mouse_button_held)
        
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
    interfaces.render(screen)
    #for i in interfaces:
    #    if interfaces[i].is_visible():
    #       interfaces[i].render(screen)
    
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
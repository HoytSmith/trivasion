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

#globals
game_is_running = True
game_settings = GameSettings("settings", "DEFAULT_SETTINGS.json", "GAME_SETTINGS.json")
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

#initializes the game. resets everything when called again later
def init_game():
    global game_is_running, game_settings, current_state, interfaces
    init_pygame()
    init_interfaces()
    change_state(GameState.MENU)

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
    resolution = game_settings.get_setting("screen_resolution")
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode(resolution, flags)
    screen_positions = {
        "top" : 0,
        "left" : 0,
        "center_x" : resolution[0]//2,
        "center_y" : resolution[1]//2,
        "right" : resolution[0],
        "bottom" : resolution[1],
    }

#(re)set main menu interface
def init_menu_interface():
    global screen_positions
    menu_interface = GameInterface(priority=0)

    #menu title stuff
    menu_title_box = Box(name="Menu_Title_Box", priority=0, position=(0, 50), size=(800, 50), color=(100, 100, 100))
    menu_title_label = Label(name="Menu_Title_Label", priority=1, content="Main Menu", font_size=50)
    menu_title_box.position_component_relative(component=menu_title_label, position=(50,50), percent_flag=True,
                                               h_align=Alignment.MIDDLE, v_align=Alignment.MIDDLE)
    menu_title_box.add_child(menu_title_label)

    #menu buttons
    menu_start_button = Button.quick_create(
        name="Menu_Start_Button", 
        text="Start Game", 
        position=(400, 400), 
        padding=(10,5), 
        callback=lambda: queue_state(GameState.PLAY)
    )
    menu_quit_button = Button.quick_create(
        name="Menu_Quit_Button", 
        text="Quit Game", 
        position=(400, 500), 
        padding=(10,5), 
        callback=lambda: queue_state(GameState.QUIT)
    )

    #add components to interface
    menu_interface.add_component(menu_title_box)
    menu_interface.add_component(menu_start_button)
    menu_interface.add_component(menu_quit_button)
    return menu_interface

#(re)set gameplay interface
def init_gameplay_interface():
    global screen_positions
    gameplay_interface = GameInterface(priority=0)

    #gameplay title stuff
    gameplay_title_box = Box(name="Gameplay_Title_Box", priority=0, position=(250, 50), size=(300, 100), color=(100, 100, 100))
    gameplay_title_label = Label(name="Gameplay_Title_Label", priority=1, content="Gameplay", position=(300, 75), font_size=50)
    gameplay_title_box.add_child(gameplay_title_label)

    #gameplay button stuff
    gameplay_return_button = Button.quick_create(
        name="Gameplay_Return_Button", 
        text="Return to Main Menu", 
        position=(250, 400), 
        padding=(10,5), 
        callback=lambda: queue_state(GameState.START)
    )

    #add components to interface
    gameplay_interface.add_component(gameplay_title_box)
    gameplay_interface.add_component(gameplay_return_button)
    return gameplay_interface

#(re)set paused game interface overlay
def init_gamepause_interface():
    global screen_positions
    gamepause_interface = GameInterface(priority=10)

    #gameplay title stuff
    gamepause_title_box = Box(name="Gamepause_Title_Box", priority=0, position=(250, 150), size=(300, 100), color=(100, 100, 100))
    gamepause_title_label = Label(name="Gamepause_Title_Label", priority=1, content="Game Paused", position=(300, 175), font_size=50)
    gamepause_title_box.add_child(gamepause_title_label)

    #gameplay button stuff
    gamepause_resume_button = Button.quick_create(
        name="Gamepause_Resume_Button", 
        text="Resume Game", 
        position=(400, 300), 
        padding=(10,5), 
        button_color=(0,1,0), 
        callback=lambda: queue_state(GameState.PLAY)
    )
    
    #add components to interface
    gamepause_interface.add_component(gamepause_title_box)
    gamepause_interface.add_component(gamepause_resume_button)
    return gamepause_interface

#(re)set game-over interface overlay
def init_gameover_interface():
    global screen_positions
    gameover_interface = GameInterface(priority=10)
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
    current_state = new_state
    if current_state == GameState.QUIT:
        game_is_running = False
    elif current_state == GameState.START:
        init_game()
    elif current_state == GameState.MENU:
        menu.show()
        menu.activate()
    elif current_state.value >= GameState.PLAY.value:
        menu.hide()
        menu.deactivate()
        gameplay.show()
        if current_state == GameState.PLAY:
            gamepause.deactivate()
            gamepause.hide()
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
    global game_is_running, pending_state, interfaces, mouse_button_held, pause_keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False
            return
        if event.type == pygame.KEYDOWN:
            if event.key in pause_keys and current_state == GameState.PLAY:
                queue_state(GameState.PAUSE)
        #Ensure only first frame of MOUSEBUTTONDOWN is processed
        toggle_mouse_state = (
            (event.type == pygame.MOUSEBUTTONDOWN and not mouse_button_held) or 
            (event.type == pygame.MOUSEBUTTONUP and mouse_button_held)
        )

        for interface in interfaces.values():
            if interface.is_active():
                interface.handle_event(event, mouse_button_held)
        
        #Mouse state is toggled after event is consumed
        if toggle_mouse_state:
            mouse_button_held = not mouse_button_held
        
        #resolve state changes after events are handled
        if pending_state:
            change_state(pending_state)
            pending_state = None

#called during gameloop to render the game
def render_game():
    global screen, interfaces
    screen.fill("black")
    for i in interfaces:
        if interfaces[i].is_visible():
            interfaces[i].render(screen)
    pygame.display.flip()

#main program, contains the gameloop
def main():
    global game_is_running, game_settings, clock, pending_state
    init_game()

    #game loop
    while game_is_running:
        #events
        handle_events()
        #tick update logic
        #draw update logic
        render_game()
        
        #limit tickrate
        clock.tick(game_settings.get_setting("fps_limit"))
    quit_game()

#called when game ends
def quit_game():
    pygame.quit()

#ensure that main program is called
if __name__ == "__main__":
    main()
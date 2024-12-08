#imports
import pygame
from src.gamesettings import GameSettings
from src.gamestates import GameState
from src.gameinterface import GameInterface
from src.gameinterfacecomponent import GameInterfaceComponent
from src.label import Label
from src.box import Box
from src.buttonstate import ButtonState
from src.button import Button

#globals
game_is_running = True
game_settings = GameSettings("settings", "DEFAULT_SETTINGS.json", "GAME_SETTINGS.json")
current_state = GameState.START
interfaces = {}
screen = None
clock = None

#initializes the game. resets everything when called again later
def init_game():
    global game_is_running, game_settings, current_state, interfaces
    init_pygame()
    init_interfaces()
    change_state(GameState.MENU)

#initialize everything related to pygame
def init_pygame():
    global game_settings, screen, clock
    pygame.init()
    fullscreen = game_settings.get_setting("fullscreen")
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode(game_settings.get_setting("screen_resolution"), flags)
    clock = pygame.time.Clock()

#(re)set main menu interface
def init_menu_interface():
    menu_interface = GameInterface(priority=0)

    #menu title stuff
    menu_box = Box(name="Menu_Box", priority=1, position=(250, 50), size=(300, 100), color=(100, 100, 100))
    menu_title = Label(name="Menu_Title", priority=2, content="Main Menu", position=(300, 75), font_size=50)
    menu_box.add_child(menu_title)

    #menu button stuff
    menu_button = Button(name="Menu_Button", priority=0, position=(200, 400), size=(200, 50))
    menu_button_label = Label(name="Menu_Button_Label", priority=2, content="Menu Button", position=(200, 400), color=(255, 255, 255), font_size=36)
    menu_button_idle = Box(name="Menu_Button_Idle", priority=1, position=(200, 400), size=(200, 50), color=(0, 0, 200))
    menu_button_hover = Box(name="Menu_Button_Hover", priority=1, position=(200, 400), size=(200, 50), color=(0, 0, 255))
    menu_button_active = Box(name="Menu_Button_Active", priority=1, position=(200, 400), size=(200, 50), color=(0, 0, 128))
    menu_button.set_label(menu_button_label)
    menu_button.set_style(key=ButtonState.IDLE, style=menu_button_idle)
    menu_button.set_style(key=ButtonState.HOVER, style=menu_button_hover)
    menu_button.set_style(key=ButtonState.ACTIVE, style=menu_button_active)

    #add components to interface
    menu_interface.add_component(menu_box)
    menu_interface.add_component(menu_button)
    return menu_interface

#(re)set gameplay interface
def init_gameplay_interface():
    gameplay_interface = GameInterface(priority=0)
    return gameplay_interface

#(re)set paused game interface overlay
def init_gamepause_interface():
    gamepause_interface = GameInterface(priority=10)
    return gamepause_interface

#(re)set game-over interface overlay
def init_gameover_interface():
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

#direct gameflow
def change_state(new_state):
    global current_state
    menu = get_interface(GameState.MENU)
    gameplay = get_interface(GameState.PLAY)
    gamepause = get_interface(GameState.PAUSE)
    gameover = get_interface(GameState.END)
    current_state = new_state
    if current_state == GameState.START:
        init_game()
    elif current_state == GameState.MENU:
        menu.show()
        menu.activate()
    elif current_state >= GameState.PLAY:
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
    global game_is_running, interfaces
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_is_running = False
        for i in interfaces:
            if interfaces[i].is_active():
                interfaces[i].handle_event(event)

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
    global game_is_running, game_settings, clock
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


#ensure that main program is called
if __name__ == "__main__":
    main()
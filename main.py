#imports
import pygame
from src.gamesettings import GameSettings
from src.gamestates import GameState
from src.gameinterface import GameInterface
from src.gameinterfacecomponent import GameInterfaceComponent

#basic setup
game_settings = GameSettings("settings", "DEFAULT_SETTINGS.json", "GAME_SETTINGS.json")
current_state = GameState.START

#setup game interfaces
gamemenu_interface = GameInterface()
gameplay_interface = GameInterface()
gamepause_interface = GameInterface()
gameover_interface = GameInterface()
interfaces = [gamemenu_interface, gameplay_interface, gamepause_interface, gameover_interface]

#main program
def main():
    global game_settings, current_state
    screen_resolution = game_settings.get_setting("screen_resolution")
    fps_limit = game_settings.get_setting("fps_limit")
    #setup pygame
    pygame.init()
    screen = pygame.display.set_mode(screen_resolution)
    clock = pygame.time.Clock()
    
    #game loop
    game_is_running = True
    while game_is_running:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False
            for interface in interfaces:
                interface.handle_event(event)
        #tick update logic
        #draw update logic
        screen.fill("black")
        for interface in interfaces:
            interface.render(screen)
        pygame.display.flip()

        #limit tickrate
        clock.tick(fps_limit)


#ensure that main program is called
if __name__ == "__main__":
    main()
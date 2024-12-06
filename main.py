#imports
import pygame
from src.gamesettings import GameSettings
from src.gamestates import GameState

#basic setup
game_settings = GameSettings("settings", "DEFAULT_SETTINGS.json", "GAME_SETTINGS.json")
current_state = GameState.START

#main program
def main():
    global game_settings, current_state
    screen_resolution = game_settings.get_setting("screen_resolution")
    #setup pygame
    pygame.init()
    screen = pygame.display.set_mode(screen_resolution)

    #game loop
    game_is_running = True
    while game_is_running:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_running = False
        #tick update logic
        #draw update logic
        pygame.display.flip()

#ensure that main program is called
if __name__ == "__main__":
    main()
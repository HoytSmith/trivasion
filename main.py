#imports
import pygame

#main program
def main():
    #setup pygame
    pygame.init()
    screen = pygame.display.set_mode()

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
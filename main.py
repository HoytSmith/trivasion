#imports
import pygame

#main program
def main():
    #setup pygame
    pygame.init()
    screen = pygame.display.set_mode()

    #game loop
    while True:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

#ensure that main program is called
if __name__ == "__main__":
    main()
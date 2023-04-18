import pygame

from game import Game

if __name__ == '__main__':
    print("Successfully started application.")
    pygame.init()

    game = Game(4, 400, 400)

    game.run()

    pygame.quit()
import sys

import pygame


def check():

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                print('up')
            elif event.key == pygame.K_DOWN:
                print('down')
            elif event.key == pygame.K_RIGHT:
                print('right')
            elif event.key == pygame.K_LEFT:
                print('left')
            elif event.key == pygame.K_ESCAPE:
                print('exit')
                pygame.quit()
                sys.exit(0)


pygame.init()
screen = pygame.display.set_mode((1000, 800))
while True:
    check()

import random
import sys

import pygame
from graphic import Graphic
from snake import Snake

if __name__ == '__main__':

    bg = (170, 202, 154)
    gray = (55, 55, 55)
    black = (0, 0, 0)
    width = 600
    height = 400
    block = 20
    pink = (171, 54, 81)
    blue = (106, 133, 164)
    screen = pygame.display.set_mode((width, height))
    # Create snake
    sn = Snake(width=width, height=height, block=block)
    x_snake, y_snake = sn.get_random_location()
    snake = [(x_snake, y_snake)]
    direction = 'right'
    eaten = True
    while True:
        # Draw scene
        gr = Graphic(scene_width=width, scene_height=height,
                     block=block, bg_color=bg, food_color=pink,
                     wall_color=black, snake_color=blue)

        scene = gr.draw_scene(scene=screen)
        if eaten:
            x_food = random.randint(3 * block, width - 2 * block)
            y_food = random.randint(3 * block, height - 2 * block)
            x_food = block * round(x_food / block)
            y_food = block * round(y_food / block)
            food = (x_food, y_food)
            eaten = False
        gr.draw_food(scene=scene, food=food)
        # time.sleep(3)
        keys_pressed = pygame.event.get()
        for event in keys_pressed:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake, direction, eaten = sn.turn_up(snake, food)
                elif event.key == pygame.K_DOWN:
                    snake, direction, eaten = sn.turn_down(snake, food)
                elif event.key == pygame.K_RIGHT:
                    snake, direction, eaten = sn.turn_right(snake, food)
                elif event.key == pygame.K_LEFT:
                    snake, direction, eaten = sn.turn_left(snake, food)
                elif event.key == pygame.K_ESCAPE:
                    print('exit')
                    pygame.quit()
                    sys.exit(0)

        if sn.is_dead(snake=snake, direction=direction):
            print('died')
            pygame.quit()
            sys.exit(0)

        scene = gr.draw_snake(scene=scene, snake=snake)
        pygame.display.update()
    # time.sleep(10)

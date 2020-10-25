import random
import sys

import pygame
from graphic import Graphic
from snake import Snake

if __name__ == '__main__':

    bg = (170, 202, 154)
    # gray = (55, 55, 55)
    black = (0, 0, 0)
    width = 600
    height = 400
    info_zone = 60
    block = 20
    pink = (171, 54, 81)
    blue = (106, 133, 164)
    screen = pygame.display.set_mode((width, height + info_zone))
    # Create snake
    sn = Snake(width=width, height=height, block=block, info_zone=info_zone)
    x_snake, y_snake = sn.get_random_location()
    snake = [(x_snake, y_snake)]
    direction = ''
    eaten = True
    score = 1
    # Draw scene
    gr = Graphic(scene_width=width, scene_height=height,
                 info_zone=info_zone, block=block, bg_color=bg,
                 food_color=pink, wall_color=black, snake_color=blue)
    while True:

        scene = gr.draw_scene(scene=screen, score=score)
        if eaten:
            food = ()
            while food == ():
                x_food = random.randint(3 * block, width - 2 * block)
                y_food = random.randint(3 * block, height - 2 * block)
                + info_zone
                x_food = block * round(x_food / block)
                y_food = block * round(y_food / block)
                if (x_food, y_food) not in snake:
                    food = (x_food, y_food)
            eaten = False
        gr.draw_food(scene=scene, food=food)
        # time.sleep(3)
        keys_pressed = pygame.event.get()
        for event in keys_pressed:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                elif event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_ESCAPE:
                    print('exit')
                    pygame.quit()
                    sys.exit(0)
        snake, eaten, score = sn.move_snake(
            snake=snake, direction=direction, food=food, score=score)
        if sn.is_dead(snake=snake, direction=direction):
            print('Died\nscore = ', score)
            pygame.quit()
            sys.exit(0)

        scene = gr.draw_snake(scene=scene, snake=snake)
        pygame.display.update()
        pygame.time.Clock().tick(5)
    # time.sleep(10)

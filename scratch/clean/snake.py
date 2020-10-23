import random

import pygame
from graphic import Graphic


class Snake:
    def __init__(self, width, height, block, info_zone):
        self.width = width
        self.height = height
        self.block = block
        self.info_zone = info_zone
        self.bg = (170, 202, 154)
        self.pink = (171, 54, 81)
        self.black = (0, 0, 0)
        self.blue = (106, 133, 164)

    def get_random_coords(self, start, stop):
        value = random.randint(3 * start, stop - 2 * start)
        normalized_value = start * round(value / start)
        return normalized_value

    def init_positions(self):
        # Init snake
        x_head = self.get_random_coords(start=self.block, stop=self.width)
        y_head = self.get_random_coords(start=self.block, stop=self.height)
        init_snake = [(x_head, y_head), (x_head, y_head - self.block),
                      (x_head, y_head - 2 * self.block)]

        # Init food
        init_food = ()
        while init_food == ():
            while init_food == ():
                x_food = self.get_random_coords(
                    start=self.block, stop=self.width)
                y_food = self.get_random_coords(
                    start=self.block, stop=self.height)
                if (x_food, y_food) not in init_snake:
                    init_food = (x_food, y_food)
            return (x_head, y_head), init_snake, init_food

    def play_game(self, snake, food, button_direction, score, screen, clock):
        gr = Graphic(scene_width=self.width, scene_height=self.height,
                     info_zone=self.info_zone, block=self.block,
                     bg_color=self.bg, food_color=self.pink,
                     wall_color=self.black, snake_color=self.blue)
        alive = True
        while alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    alive = False
            scene = gr.draw_scene(scene=screen, score=score)
            gr.draw_food(scene=scene, food=food)
            snake, food, score = self.move(
                snake, food, button_direction, score)
            scene = gr.draw_snake(scene=scene, snake=snake)
            pygame.display.update()
            pygame.time.Clock().tick(clock)
            return snake, food, score

    def move(self, snake, food, button_direction, score):
        head_x = snake[0][0]
        head_y = snake[0][1]
        if button_direction == 'right':
            head_x += self.block
        elif button_direction == 'left':
            head_x -= self.block
        elif button_direction == 'up':
            head_y -= self.block
        elif button_direction == 'down':
            head_y += self.block
        if head_x == food[0] and head_y == food[1]:
            score += 1
        else:
            snake.pop()
        snake.insert(0, (head_x, head_y))
        a, b, food = self.init_positions()
        return snake, food, score

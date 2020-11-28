import random

import pygame
from graphic import Graphic


class Snake:
    """Class to create the snake and move it.

    Parameters
    ----------
    width : int
        The width of the scene.
    height : int
        The height of the scene.
    block : int
        The size of the blocks forming the snake and the borders.
    info_zone : int
        The height of the info zone.

    Attributes
    ----------
    bg : tuple[int]
        The background color.
    pink : tuple
        The food color.
    black : tuple
        The wall color.
    blue : tuple
        The snake color.
    width
    height
    block
    info_zone

    """

    def __init__(self, width, height, block, info_zone):
        self.width = width
        self.height = height
        self.block = block
        self.info_zone = info_zone
        self.bg = (170, 202, 154)
        self.pink = (171, 54, 81)
        self.black = (0, 0, 0)
        self.blue = (106, 133, 164)

    def get_random_coords(self, start, stop, extra=0):
        """Generate random coordinates for food and snake at start.

        Parameters
        ----------
        start : int
            The beginning of the possible coordinates interval.
        stop : int
            The end of the possible coordinates interval.
        extra : int
            If not null, consider the info zone height.

        Returns
        -------
        normalized_value: int
            The generated coordinates.

        """
        value = random.randint(3 * start + extra, stop - 2 * start)
        normalized_value = start * round(value / start)
        return normalized_value

    def init_positions(self):
        """Init the snake and food positions at the start.

        Returns
        -------
        x_head: int
            The snake's head X coordinate.
        y_head: int
            The snake's head Y coordinate.
        init_snake: tuple[int]
            The snake's coordinates.
        init_food: tuple[int]
            The generated food coordinates.

        """
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
                    start=self.block, stop=self.height, extra=60)
                if (x_food, y_food) not in init_snake:
                    init_food = (x_food, y_food)
            return (x_head, y_head), init_snake, init_food

    def play_game(self, snake, food, button_direction, score, screen, clock):
        """Launch the snake game.

        Parameters
        ----------
        snake : tuple[int]
            The snake coordinates.
        food : tuple[int]
            The food coordinates.
        button_direction : int
            The direction the snake will follow.
        score : int
            The score value.
        screen : type
            The scene.
        clock : int
            The speed of the snake.

        Returns
        -------
        snake: tuple[int]
            The snake's coordinates.
        food: tuple[int]
            The food's coordinates.
        score: int
            The updated score value.

        """

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
        """Move the snake to a specified direction.

        Parameters
        ----------
        snake : tuple[int]
            The snake's coordinates.
        food : tuple[int]
            The food's coordinates.
        button_direction : int
            The input direction.
        score : int
            The score value.

        Returns
        -------
        snake: tuple[int]
            The snake's coordinates.
        food: tuple[int]
            The food's coordinates.
        score: int
            The updated score value.

        """
        head_x = snake[0][0]
        head_y = snake[0][1]
        if button_direction == 1:
            head_x += self.block
        elif button_direction == 0:
            head_x -= self.block
        elif button_direction == 2:
            head_y += self.block
        else:
            head_y -= self.block
        if head_x == food[0] and head_y == food[1]:
            score += 1
            a, b, food = self.init_positions()
        else:
            snake.pop()
        snake.insert(0, (head_x, head_y))
        return snake, food, score

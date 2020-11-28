import numpy as np

import pygame
from snake import Snake
from tqdm import tqdm
from utils import Utils


class GenerateData:
    """Class to simulate games and generate the training data.

    Parameters
    ----------
    width : int
        The width of the scene.
    height : int
        The height of the scene.
    block : int
        The size of the blocks forming the snake and the walls.
    info_zone : int
        The info zone height.
    clock_rate : int
        The speed of the snake.

    Attributes
    ----------
    training_data_x : numpy ndarray
        The generated training data.
    training_data_y : numpy ndarray
        The training data labels.
    training_games : int
        The number of the games to be simulated.
    steps_per_game : int
        The number of moves per games.
    sn : class
        The class to create the snake.
    utils : class
        The class with helper methods.
    height
    width
    block
    info_zone
    clock_rate

    """

    def __init__(self, height, width, block, info_zone, clock_rate):
        self.height = height
        self.width = width
        self.block = block
        self.info_zone = info_zone
        self.training_data_x = []
        self.training_data_y = []
        self.training_games = 100
        self.steps_per_game = 5000
        self.clock_rate = clock_rate
        self.sn = Snake(self.width, self.height, self.block, self.info_zone)
        self.utils = Utils(width=self.width, height=self.height,
                           block=self.block, info_zone=self.info_zone)

    def generate_training_data(self):
        """Generate training data.

        Returns
        -------
        training_data_x: numpy ndarray
            The training data.
        training_data_y: numpy ndarray
            The training data labels.

        """
        screen = pygame.display.set_mode((self.width, self.height))

        for game in tqdm(range(self.training_games)):
            snake_head, snake, food = self.sn.init_positions()
            score = 1
            for step in range(self.steps_per_game):
                (angle, snake_direction, normalized_angle,
                 normalized_direction) = self.utils.calculate_angle(
                     snake, food)

                direction, button_direction = self.generate_random_direction(
                    snake, angle)

                (current_direction, is_front_blocked, is_left_blocked,
                 is_right_blocked) = self.utils.blocked_directions(snake)
                direction, button_direction, self.training_data_y = \
                    self.generate_training_data_y(
                        snake, angle, button_direction,
                        direction, self.training_data_y,
                        is_front_blocked, is_left_blocked,
                        is_right_blocked)
                if (is_front_blocked == 1 and
                    is_left_blocked == 1 and
                        is_right_blocked == 1):
                    break
                self.training_data_x.append(
                    [is_left_blocked, is_front_blocked,
                     is_right_blocked, normalized_angle[0],
                     normalized_direction[0], normalized_angle[1],
                     normalized_direction[1]])

                snake, food, score = self.sn.play_game(
                    snake=snake, food=food, button_direction=button_direction,
                    score=score, screen=screen, clock=self.clock_rate)
        return self.training_data_x, self.training_data_y

    def generate_random_direction(self, snake, food_angle):
        """Generate random direction.

        Parameters
        ----------
        snake : tuple[int]
            The snake coordinates.
        food_angle : float
            The angle between the food and the snake's head.

        Returns
        -------
        direction: int
            The the next snake direction.
        button_direction: int
            The direction that corresponds to the next direction.

        """
        direction = 0
        if food_angle > 0:
            direction = 1
        elif food_angle < 0:
            direction = -1
        else:
            direction = 0

        return self.direction_vector(snake, food_angle, direction)

    def direction_vector(self, snake, food_angle, direction):
        """Generate a coordinates vector based on the gived direction.

        Parameters
        ----------
        snake : tuple[int]
            The snake coordinates.
        food_angle : float
            The angle between the food and the snake's head.
        direction : int
            The generated direction.

        Returns
        -------
        direction: int
            The the next snake direction.
        button_direction: int
            The direction that corresponds to the next direction.

        """
        current_direction = np.array(snake[0]) - np.array(snake[1])
        left_direction = np.array([current_direction[1],
                                   -current_direction[0]])
        right_direction = np.array([-current_direction[1],
                                    current_direction[0]])

        new_direction = current_direction

        if direction == -1:
            new_direction = left_direction
        if direction == 1:
            new_direction = right_direction

        button_direction = self.utils.generate_button_direction(new_direction)

        return direction, button_direction

    def generate_training_data_y(self, snake, food_angle, button_direction,
                                 direction, training_data_y, is_front_blocked,
                                 is_left_blocked, is_right_blocked):
        """Generate the training data labels.

        Parameters
        ----------
        snake : tuple[int]
            The snake coordinates.
        food_angle : float
            The angle between the food and the snake's head.

        button_direction : int
            The direction that corresponds to the next direction.
        direction : int
            The generated direction.
        training_data_y : numpy ndarray
            The training data labels.
        is_front_blocked : bool
            True if the front is blocked, False if not.
        is_left_blocked : bool
            True if the left is blocked, False if not.
        is_right_blocked : bool
            True if the right is blocked, False if not.

        Returns
        -------
        direction : int
            The generated direction.
        button_direction : int
            The direction that corresponds to the next direction.
        training_data_y : numpy ndarray
            The training data labels.

        """
        if direction == -1:
            if is_left_blocked == 1:
                if is_front_blocked == 1 and is_right_blocked == 0:
                    direction, button_direction = self.direction_vector(
                        snake, food_angle, 1)
                    training_data_y.append([0, 0, 1])
                elif is_front_blocked == 0 and is_right_blocked == 1:
                    direction, button_direction = self.direction_vector(
                        snake, food_angle, 0)
                    training_data_y.append([0, 1, 0])
                elif is_front_blocked == 0 and is_right_blocked == 0:
                    direction, button_direction = self.direction_vector(
                        snake, food_angle, 1)
                    training_data_y.append([0, 0, 1])

            else:
                training_data_y.append([1, 0, 0])

        elif direction == 0:
            if is_front_blocked == 1:
                if is_left_blocked == 1 and is_right_blocked == 0:
                    direction, button_direction = self.direction_vector(
                        snake, food_angle, 1)
                    training_data_y.append([0, 0, 1])
                elif is_left_blocked == 0 and is_right_blocked == 1:
                    direction, button_direction = self.direction_vector(
                        snake, food_angle, -1)
                    training_data_y.append([1, 0, 0])
                elif is_left_blocked == 0 and is_right_blocked == 0:
                    training_data_y.append([0, 0, 1])
                    direction, button_direction = self.direction_vector(
                        snake, food_angle, 1)
            else:
                training_data_y.append([0, 1, 0])
        else:
            if is_right_blocked == 1:
                if is_left_blocked == 1 and is_front_blocked == 0:
                    direction, button_direction = self.direction_vector(
                        snake, food_angle, 0)
                    training_data_y.append([0, 1, 0])
                elif is_left_blocked == 0 and is_front_blocked == 1:
                    direction, button_direction = self.direction_vector(
                        snake, food_angle, -1)
                    training_data_y.append([1, 0, 0])
                elif is_left_blocked == 0 and is_front_blocked == 0:
                    direction, button_direction = self.direction_vector(
                        snake, food_angle, -1)
                    training_data_y.append([1, 0, 0])
            else:
                training_data_y.append([0, 0, 1])

        return direction, button_direction, training_data_y

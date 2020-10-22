import math

import numpy as np

import pygame
from snake import Snake
from tqdm import tqdm


class GenerateData:
    def __init__(self, height, width, block, info_zone):
        self.height = height
        self.width = width
        self.block = block
        self.info_zone = info_zone
        self.training_data_x = []
        self.training_data_y = []
        self.training_games = 10
        self.steps_per_game = 20
        self.sn = Snake(self.width, self.height, self.block, self.info_zone)

    def generate_training_data(self):
        screen = pygame.display.set_mode((self.width, self.height))
        for game in tqdm(range(self.training_games)):
            snake_head, snake, food = self.sn.init_positions()
            score = 1
            for step in range(self.steps_per_game):
                (angle, snake_direction, normalized_angle,
                 normalized_direction) = self.calculate_angle(snake, food)

                direction, button_direction = self.generate_random_direction(
                    snake, angle)

                (current_direction, is_front_blocked, is_left_blocked,
                 is_right_blocked) = self.blocked_directions(snake)
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
                    score=score, screen=screen, clock=100)
        return self.training_data_x, self.training_data_y

    def calculate_angle(self, snake, food):
        direction = np.array(snake[0]) - np.array(snake[1])
        normalized_direction = np.linalg.norm(direction)
        angle = np.array(food) - np.array(snake[0])
        normalized_angle = np.linalg.norm(angle)
        food_angle = angle / normalized_angle
        snake_direction = direction / normalized_direction
        final_angle = math.atan2(
            food_angle[1] * snake_direction[0]
            - food_angle[0] * snake_direction[1],
            food_angle[1] * snake_direction[1]
            + food_angle[0] * snake_direction[0]) / math.pi
        return (final_angle, direction, food_angle, snake_direction)

    def generate_random_direction(self, snake, food_angle):
        direction = 0
        if food_angle > 0:
            direction = 1
        elif food_angle < 0:
            direction = -1
        else:
            direction = 0

        return self.direction_vector(snake, food_angle, direction)

    def direction_vector(self, snake, food_angle, direction):
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

        button_direction = self.generate_button_direction(new_direction)

        return direction, button_direction

    def generate_button_direction(self, new_direction):
        # Check if it is 10 or 5 based on the block size
        button_direction = 0
        if new_direction.tolist() == [10, 0]:
            button_direction = 1  # Change it to right
        elif new_direction.tolist() == [-10, 0]:
            button_direction = 0  # Change it to left
        elif new_direction.tolist() == [0, 10]:
            button_direction = 2  # Change it to down
        else:
            button_direction = 3  # Change it to up

        return button_direction

    def blocked_directions(self, snake):
        current_direction = np.array(snake[0]) - np.array(snake[1])

        left_direction = np.array([current_direction[1],
                                   -current_direction[0]])
        right_direction = np.array([-current_direction[1],
                                    current_direction[0]])

        is_front_blocked = self.is_direction_blocked(snake, current_direction)
        is_left_blocked = self.is_direction_blocked(snake, left_direction)
        is_right_blocked = self.is_direction_blocked(snake, right_direction)

        return (current_direction, is_front_blocked,
                is_left_blocked, is_right_blocked)

    def is_direction_blocked(self, snake, current_direction):
        next_step = snake[0] + current_direction
        # snake_start = snake[0]
        if (self.collision_with_boundaries(next_step) == 1 or
                self.collision_with_self(next_step.tolist(), snake) == 1):
            return 1
        else:
            return 0

    def collision_with_boundaries(self, snake_start):
        if (snake_start[0] >= 600 or snake_start[0] < 0 or
                snake_start[1] >= 400 or snake_start[1] < 0):
            return 1
        else:
            return 0

    def collision_with_self(self, snake_start, snake):
        # snake_start = snake_position[0]
        if snake_start in snake[1:]:
            return 1
        else:
            return 0

    def generate_training_data_y(self, snake, food_angle, button_direction,
                                 direction, training_data_y, is_front_blocked,
                                 is_left_blocked, is_right_blocked):
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

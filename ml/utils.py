import math

import numpy as np


class Utils:
    def __init__(self, width, height, block, info_zone):
        self.width = width
        self.height = height
        self.block = block
        self.info_zone = info_zone

    def calculate_angle(self, snake, food):
        direction = np.array(snake[0]) - np.array(snake[1])
        normalized_direction = np.linalg.norm(direction)
        angle = np.array(food) - np.array(snake[0])
        normalized_angle = np.linalg.norm(angle)
        if normalized_angle == 0:
            normalized_angle = 10
        if normalized_direction == 0:
            normalized_direction = 10
        food_angle = angle / normalized_angle
        snake_direction = direction / normalized_direction
        final_angle = math.atan2(
            food_angle[1] * snake_direction[0]
            - food_angle[0] * snake_direction[1],
            food_angle[1] * snake_direction[1]
            + food_angle[0] * snake_direction[0]) / math.pi
        return (final_angle, direction, food_angle, snake_direction)

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
        if (self.collision_with_boundaries(next_step) == 1
                or self.collision_with_self(tuple(next_step), snake) == 1):
            return 1
        else:
            return 0

    def collision_with_boundaries(self, snake_start,):
        if (snake_start[0] >= self.width - self.block or
            snake_start[0] <= self.block or
                snake_start[1] >= self.height - self.block
                or snake_start[1] <= self.block + self.info_zone):
            return 1
        else:
            return 0

    def collision_with_self(self, snake_start, snake):
        if snake_start in snake[1:]:
            return 1
        else:
            return 0

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

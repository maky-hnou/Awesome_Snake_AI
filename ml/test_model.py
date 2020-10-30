import numpy as np

import pygame
import tensorflow as tf
from generate_data import GenerateData
from snake import Snake


class TestSnakeModel:
    def __init__(self, model_path, json_path, width, height, block, info_zone):
        self.model_path = model_path
        self.width = width
        self.height = height
        self.block = block
        self.json_path = json_path
        self.info_zone = info_zone
        self.sn = Snake(width=self.width, height=self.height,
                        block=self.block, info_zone=self.info_zone)
        self.gd = GenerateData(height=self.height, width=self.width,
                               block=self.block, info_zone=self.info_zone,
                               clock_rate=100)

    def load_model(self):
        json_file = open(self.json_path, 'r')
        loaded_json_model = json_file.read()
        model = tf.keras.models.model_from_json(loaded_json_model)
        model.load_weights(self.model_path)
        return model

    def run_test(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        score = 3
        model = self.load_model()
        snake_head, snake, food = self.sn.init_positions()
        while True:
            (current_direction, is_front_blocked, is_left_blocked,
             is_right_blocked) = self.gd.blocked_directions(snake)

            (angle, snake_direction, normalized_angle,
             normalized_direction) = self.gd.calculate_angle(snake, food)
            input_data = np.array(
                [is_left_blocked, is_front_blocked,
                 is_right_blocked,
                 normalized_angle[0],
                 normalized_direction[0], normalized_angle[1],
                 normalized_direction[1]]).reshape(-1, 7)

            predicted_directions = model.predict(input_data)
            predicted_direction = np.argmax(np.array(predicted_directions)) - 1

            new_direction = np.array(snake[0]) - np.array(snake[1])
            if predicted_direction == -1:
                new_direction = np.array([new_direction[1], -new_direction[0]])
            elif predicted_direction == 1:
                new_direction = np.array([-new_direction[1], new_direction[0]])

            button_direction = self.gd.generate_button_direction(new_direction)

            next_step = snake[0] + current_direction
            if (self.gd.collision_with_boundaries(snake[0]) == 1
                or self.gd.collision_with_self(tuple(next_step),
                                               snake) == 1):
                break

            snake, food, score = self.sn.play_game(
                snake=snake, food=food, button_direction=button_direction,
                score=score, screen=screen, clock=50)


test = TestSnakeModel(model_path='models/model.h5',
                      json_path='models/model.json',
                      width=600, height=400, block=10,
                      info_zone=60)
test.run_test()

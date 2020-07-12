import pygame


class Graphic:
    def __init__(self, scene_width, scene_height, block, bg_color,
                 food_color, wall_color, snake_color):

        self.scene_width = scene_width
        self.scene_height = scene_height
        self.block = block
        self.bg_color = bg_color
        self.food_color = food_color
        self.wall_color = wall_color

        self.snake_color = snake_color

    def draw_scene(self, scene):
        # Fill the background
        scene.fill(self.bg_color)
        # building the horizontal walls
        for x in range(0, self.scene_width, self.block):
            y = 0
            pygame.draw.rect(scene, self.wall_color,
                             (x, y, self.block, self.block), 1)
            pygame.draw.rect(scene, self.wall_color,
                             (x+3, y+3, self.block-6, self.block-6))
            y = self.scene_height - self.block
            pygame.draw.rect(scene, self.wall_color,
                             (x, y, self.block, self.block), 1)
            pygame.draw.rect(scene, self.wall_color,
                             (x+3, y+3, self.block-6, self.block-6))
        # building the vertical walls
        for y in range(self.block, self.scene_height-self.block, self.block):
            x = 0
            pygame.draw.rect(scene, self.wall_color,
                             (x, y, self.block, self.block), 1)
            pygame.draw.rect(scene, self.wall_color,
                             (x+3, y+3, self.block-6, self.block-6))
            x = self.scene_width - self.block
            pygame.draw.rect(scene, self.wall_color,
                             (x, y, self.block, self.block), 1)
            pygame.draw.rect(scene, self.wall_color,
                             (x+3, y+3, self.block-6, self.block-6))
        return scene

    def draw_food(self, scene, food):
        # Get the x and y coordinates that are multiples of the block size
        # x = self.block * round(food[0] / self.block)
        # y = self.block * round(food[1] / self.block)
        pygame.draw.rect(
            scene, self.food_color,
            (food[0] + 3, food[1] + 3, self.block - 6, self.block - 6))
        return scene

    def draw_snake(self, scene, snake):
        for (x, y) in snake:
            pygame.draw.rect(scene, self.snake_color,
                             (x, y, self.block, self.block), 1)
            pygame.draw.rect(scene, self.snake_color,
                             (x+3, y+3, self.block-6, self.block-6))
        return scene

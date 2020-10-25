import pygame


class Graphic:
    def __init__(self, scene_width, scene_height, block, bg_color,
                 food_color, wall_color, snake_color, info_zone):

        self.scene_width = scene_width
        self.scene_height = scene_height
        self.block = block
        self.bg_color = bg_color
        self.food_color = food_color
        self.wall_color = wall_color
        self.info_zone = info_zone

        self.snake_color = snake_color
        # Init the font
        pygame.font.init()
        self.myfont = pygame.font.Font('freesansbold.ttf', 25)

    def draw_scene(self, scene, score):
        # Fill the background
        scene.fill(self.bg_color)
        # set the text to be written
        textsurface = self.myfont.render('Score: {}'.format(score),
                                         False, (55, 55, 55))
        scene.blit(textsurface, (20, 20))
        # building the horizontal walls
        for x in range(0, self.scene_width, self.block):
            y = self.info_zone
            pygame.draw.rect(scene, self.wall_color,
                             (x, y, self.block, self.block), 1)
            pygame.draw.rect(scene, self.wall_color,
                             (x+3, y+3, self.block-6, self.block-6))
            y = self.scene_height - self.block + self.info_zone
            pygame.draw.rect(scene, self.wall_color,
                             (x, y, self.block, self.block), 1)
            pygame.draw.rect(scene, self.wall_color,
                             (x+3, y+3, self.block-6, self.block-6))
        # building the vertical walls
        for y in range(self.block, self.scene_height-self.block, self.block):
            x = 0
            pygame.draw.rect(scene, self.wall_color,
                             (x, y + self.info_zone,
                              self.block, self.block),
                             1)
            pygame.draw.rect(scene, self.wall_color,
                             (x+3, y+3 + self.info_zone,
                              self.block-6, self.block-6))
            x = self.scene_width - self.block
            pygame.draw.rect(scene, self.wall_color,
                             (x, y + self.info_zone,
                              self.block, self.block),
                             1)
            pygame.draw.rect(scene, self.wall_color,
                             (x+3, y+3 + self.info_zone,
                              self.block-6, self.block-6))
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

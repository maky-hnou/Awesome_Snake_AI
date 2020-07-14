import random


class Snake:
    def __init__(self, width, height, block):
        self.width = width
        self.height = height
        self.block = block

    def get_random_location(self):
        x = random.randint(3 * self.block, self.width - 2 * self.block)
        x = self.block * round(x / self.block)
        y = random.randint(3 * self.block, self.height - 2 * self.block)
        y = self.block * round(y / self.block)
        return x, y

    def move_snake(self, snake, direction, food):
        head_x = snake[0][0]
        head_y = snake[0][1]
        eaten = False
        if direction == 'right':
            head_x += self.block
        elif direction == 'left':
            head_x -= self.block
        elif direction == 'up':
            head_y -= self.block
        elif direction == 'down':
            head_y += self.block
        if head_x == food[0] and head_y == food[1]:
            eaten = True
        else:
            snake.pop()
        snake.insert(0, (head_x, head_y))
        return snake, eaten

    def hit_walls(self, snake, direction):
        head_x = snake[0][0]
        head_y = snake[0][1]
        if (direction == 'right' and head_x == self.width - self.block):
            return True
        elif (direction == 'left' and head_x == 0):
            return True
        elif (direction == 'up' and head_y == 0):
            return True
        elif (direction == 'down' and head_y == self.height - self.block):
            return True
        return False

    def hit_itself(self, snake, direction):
        head_x = snake[0][0]
        head_y = snake[0][1]
        snake_body = snake[1:]
        if (direction == 'right'
                and (head_x, head_y) in snake_body):
            return True
        elif (direction == 'left'
              and (head_x, head_y) in snake_body):
            return True
        elif (direction == 'up'
              and (head_x, head_y) in snake_body):
            return True
        elif (direction == 'down'
              and (head_x, head_y) in snake_body):
            return True
        return False

    def is_dead(self, snake, direction):
        if (self.hit_walls(snake, direction)
                or self.hit_itself(snake, direction)):
            return True
        return False

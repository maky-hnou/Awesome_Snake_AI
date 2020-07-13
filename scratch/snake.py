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

    def turn_right(self, snake, food):
        head_x = snake[0][0]
        head_y = snake[0][1]
        direction = 'right'
        head_x += self.block
        eaten = False
        if head_x == food[0] and head_y == food[1]:
            snake.insert(0, food)
            eaten = True
            return snake, direction, eaten
        snake.insert(0, (head_x, head_y))
        snake.pop()
        return snake, direction, eaten

    def turn_left(self, snake, food):
        head_x = snake[0][0]
        head_y = snake[0][1]
        direction = 'left'
        head_x -= self.block
        eaten = False
        if head_x == food[0] and head_y == food[1]:
            snake.insert(0, food)
            eaten = True
            return snake, direction, eaten
        snake.insert(0, (head_x, head_y))
        snake.pop()
        return snake, direction, eaten

    def turn_up(self, snake, food):
        head_x = snake[0][0]
        head_y = snake[0][1]
        eaten = False
        direction = 'up'
        head_y -= self.block
        if head_y == food[1] and head_x == food[0]:
            snake.insert(0, food)
            eaten = True
            return snake, direction, eaten
        snake.insert(0, (head_x, head_y))
        snake.pop()
        return snake, direction, eaten

    def turn_down(self, snake, food):
        head_x = snake[0][0]
        head_y = snake[0][1]
        eaten = False
        direction = 'down'
        head_y += self.block
        if head_y == food[1] and head_x == food[0]:
            snake.insert(0, food)
            eaten = True
            return snake, direction, eaten
        snake.insert(0, (head_x, head_y))
        snake.pop()
        return snake, direction, eaten

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

        if (direction == 'right'
                and (head_x + self.block, head_y) in snake):
            return True
        elif (direction == 'left'
              and (head_x - self.block, head_y) in snake):
            return True
        elif (direction == 'up'
              and (head_x, head_y - self.block) in snake):
            return True
        elif (direction == 'down'
              and (head_x, head_y + self.block) in snake):
            return True
        return False

    def is_dead(self, snake, direction):
        if (self.hit_walls(snake, direction)
                or self.hit_itself(snake, direction)):
            return True
        return False

        # if the food is near the head of the snake and the snake is going
        # in the same direction of the food, then increase the size of
        # the snake

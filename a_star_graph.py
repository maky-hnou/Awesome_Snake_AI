import random
import sys

import pygame


class Snake:
    def __init__(self, fps, window_width, window_height, cell_size):
        self.fps = fps
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        self.cell_width = int(self.window_width / self.cell_size)
        self.cell_height = int(self.window_height / self.cell_size)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255,   0)
        self.dark_green = (0, 155,   0)
        self.dark_gray = (40,  40,  40)
        self.orange = (255, 155, 111)
        self.bg_color = (17,  18,  13)
        self.up = 'up'
        self.down = 'down'
        self.right = 'right'
        self.left = 'left'
        self.head = 0
        self.fps_clock = pygame.time.Clock()
        self.display_surf = pygame.display.set_mode(
            (self.window_width, self.window_height))
        self.basic_font = pygame.font.Font('freesansbold.ttf', 18)
        self.wall_coords = self.find_wall()
        self.soft_wall_coords = self.find_soft_wall()
        self.stalling = False

    def run_game(self):
        stalling_count = -1
        start_x = 5
        start_y = 0
        snake = [{'x': start_x + 6, 'y': start_y},
                 {'x': start_x + 5, 'y': start_y},
                 {'x': start_x + 4, 'y': start_y},
                 ]
        direction = self.right
        directions_list = [self.right]
        path = []

        # Start the food in a random place.
        # food = get_random_location(snake)
        food = {'x': start_x+8,     'y': start_y}
        last_food = {'x': start_x-1,   'y': start_y - 1}
        path = self.calculate_path(snake, food, True)
        directions_list = self.calculate_direction(path)
        last_wall = 0

        while True:
            for event in pygame.event.get():  # event handling loop
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.terminate()
            # check if the snake has hit itself or the edge
            if (snake[self.head]['x'] == -1 or
                snake[self.head]['x'] == self.cell_width or
                snake[self.head]['y'] == -1 or
                    snake[self.head]['y'] == self.cell_height):
                self.terminate()
                return  # game over
            for snake_cell in snake[1:]:
                # sys.exit()
                if (snake_cell['x'] == snake[self.head]['x'] and
                        snake_cell['y'] == snake[self.head]['y']):
                    self.terminate()
                    return  # game over

            # check if snake has eaten an apply
            if (snake[self.head]['x'] == food['x'] and
                    snake[self.head]['y'] == food['y']):
                # don't remove snake's tail segment
                last_food = food
                # set a new food somewhere
                food = self.get_random_location(snake)
                # for testing purposes
                self.draw_food(food, last_food)
                # draw_food(last_food)
                # section_break() #just print some crap
                # calculate path to go
                path = self.calculate_path(snake, food, True)
                if not path:
                    self.stalling = True
                    stalling_count = 10000
                elif path == 'stall':
                    self.stalling = True
                    stalling_count = int(len(snake)/2)
                else:
                    directions_list = self.calculate_direction(path)
            else:
                del snake[-1]  # remove snake's tail segment

            last_direction = direction
            if self.stalling and not directions_list:
                only_direction = self.calculate_only_direction(snake)
                if only_direction and only_direction == last_direction:
                    directions_list.append(only_direction)
                    print('only direction:', direction)
                else:
                    if self.safe_to_go(snake, direction, last_wall):
                        # print('safe')
                        # continue the previous direction
                        directions_list.append(direction)
                    elif ((not self.find_new_head(direction, snake)
                           in snake) or
                          (self.find_new_head(direction, snake) in
                           self.wall_coords)):
                        directions_list.append(direction)
                    else:
                        last_direction = direction
                        # check if path can be found, if yes override
                        # previous calcualtion
                        path = self.calculate_path(snake, food, False)
                        if path != [] and path != 'stall':
                            self.stalling = False
                            stalling_count = -1
                            directions_list = self.calculate_direction(path)
                        else:
                            if self.check_last_wall(snake):
                                last_wall = self.check_last_wall(snake)
                            directions_list.extend(
                                self.find_better_direction(
                                    snake, direction, last_wall))
                            if self.calculate_area(
                                    self.find_new_head(
                                        directions_list[0], snake),
                                    snake, last_wall) < 3:
                                directions_list = [last_direction]
                            # print(directions_list)
                    stalling_count = stalling_count - 1
                    # print ('stalling Count:', stalling_count)
                    if stalling_count < 1:
                        # print('stalling Count',stalling_count)
                        self.stalling = False
                        prev_last_wall = last_wall
                        last_wall = 0
                        directions_list.append(last_direction)
                        # calculate path to go
                        path = self.calculate_path(snake, food, True)
                        if not path:
                            self.stalling = True
                            stalling_count = 10000
                            last_wall = prev_last_wall
                        elif path == 'stall':
                            self.stalling = True
                            stalling_count = int(len(snake)/2)
                            last_wall = prev_last_wall
                        else:
                            directions_list = self.calculate_direction(path)
            next_head = self.find_new_head(directions_list[0], snake)
            '''
            if (next_head in snake or next_head in wall_coords or next_head in
                get_next_wall_coords(last_wall)):  #if gonig to die go
                into tunnel
              last_wall = 0
              directions_list = find_next_direction(snake,
              directions_list[0],0)
              print('going into tunnel')
            '''
            if self.stalling:
                # return true if the area going in is too small
                if self.area_is_too_small(self.cell_width, next_head,
                                          snake, last_wall):
                    last_wall = 0
                    directions_list = self.find_next_direction(
                        snake, directions_list[0], 0)
                    print('almost died, recalcualting...',
                          snake[0], directions_list)

            direction = directions_list.pop(0)
            new_head = self.find_new_head(direction, snake)
            snake.insert(0, new_head)
            self.display_surf.fill(self.bg_color)
            self.draw_grid()
            self.draw_snake(snake)
            self.draw_food(food, last_food)
            self.draw_score(len(snake) - 3)
            pygame.display.update()
            self.fps_clock.tick(self.fps)

    def calculate_only_direction(self, snake):
        count = 4
        ways = self.get_neighborhood(snake[0])
        the_way = 0
        for each in ways:
            if each in snake:
                count = count - 1
            else:
                the_way = each
        if count == 1:
            return self.calculate_direction([snake[0], the_way])
        else:
            return 0

    def get_next_wall_coords(self, last_wall):
        walls = []
        # append self.left self.right walls
        loop_count = 0
        for _ in range(self.cell_height):
            if last_wall == self.right:
                walls.append({'x': 0, 'y': loop_count})
            if last_wall == self.left:
                walls.append({'x': self.cell_width-1, 'y': loop_count})
            loop_count = loop_count + 1
        # append TOP BOTTOM walls
        loop_count = 0
        for _ in range(self.cell_width):
            if last_wall == self.down:
                walls.append({'x': loop_count, 'y': 0})
            if last_wall == self.up:
                walls.append({'x': loop_count, 'y': self.cell_height-1})
            loop_count = loop_count + 1
        return walls

    def safe_to_go(self, snake, direction, last_wall):
        list_of_no = self.wall_coords + snake
        list_of_no.extend(self.get_next_wall_coords(last_wall))
        # head = snake[0]
        forward = snake[0]
        forward_left = snake[0]
        forward_right = snake[0]
        left = snake[0]
        right = snake[0]
        if direction == self.up:
            new_head = {'x': snake[self.head]['x'],
                        'y': snake[self.head]['y'] - 1}
            forward = {'x': snake[self.head]['x'],
                       'y': snake[self.head]['y'] - 2}
            forward_left = {'x': snake[self.head]['x']-1,
                            'y': snake[self.head]['y'] - 1}
            forward_right = {'x': snake[self.head]['x']+1,
                             'y': snake[self.head]['y'] - 1}
            left = {'x': snake[self.head]['x']-1,
                    'y': snake[self.head]['y']}
            right = {'x': snake[self.head]['x']+1,
                     'y': snake[self.head]['y']}
            # print('new head:', new_head)
            # print('forward:', forward)
            # print('forward left:', forward_left)
            # print('forward right:', forward_right)
            # print('left:', left)
            # print('right:', right)
            # sys.ewit(0)
        elif direction == self.down:
            new_head = {'x': snake[self.head]['x'],
                        'y': snake[self.head]['y'] + 1}
            forward = {'x': snake[self.head]['x'],
                       'y': snake[self.head]['y'] + 2}
            forward_left = {'x': snake[self.head]['x']-1,
                            'y': snake[self.head]['y'] + 1}
            forward_right = {'x': snake[self.head]['x']+1,
                             'y': snake[self.head]['y'] + 1}
            left = {'x': snake[self.head]['x']-1,
                    'y': snake[self.head]['y']}
            right = {'x': snake[self.head]['x']+1,
                     'y': snake[self.head]['y']}
        elif direction == self.left:
            new_head = {'x': snake[self.head]['x'] - 1,
                        'y': snake[self.head]['y']}
            forward = {'x': snake[self.head]['x'] - 2,
                       'y': snake[self.head]['y']}
            forward_left = {'x': snake[self.head]['x']-1,
                            'y': snake[self.head]['y'] + 1}
            forward_right = {'x': snake[self.head]['x']-1,
                             'y': snake[self.head]['y'] - 1}
            left = {'x': snake[self.head]['x'],
                    'y': snake[self.head]['y']+1}
            right = {'x': snake[self.head]['x'],
                     'y': snake[self.head]['y']-1}
        elif direction == self.right:
            new_head = {'x': snake[self.head]['x'] + 1,
                        'y': snake[self.head]['y']}
            forward = {'x': snake[self.head]['x'] + 2,
                       'y': snake[self.head]['y']}
            forward_left = {'x': snake[self.head]['x']+1,
                            'y': snake[self.head]['y'] - 1}
            forward_right = {'x': snake[self.head]['x']+1,
                             'y': snake[self.head]['y'] + 1}
            left = {'x': snake[self.head]['x'],
                    'y': snake[self.head]['y']-1}
            right = {'x': snake[self.head]['x'],
                     'y': snake[self.head]['y']+1}

        # print ('newhead',new_head,'no go:',list_of_no)
        if ((forward_left in list_of_no and left not in list_of_no) or
                (forward_right in list_of_no and right not in list_of_no)):
            # print ('forwardleft left detected', forward_left, left,
            #        'right:', forward_right, right)
            return False
        if new_head in list_of_no:
            return False
        ways_to_go = []
        ways_to_go = self.get_neighborhood(new_head)
        count = len(ways_to_go)
        for each in ways_to_go:
            if each in list_of_no:
                count = count - 1
        # print (ways_to_go,count)
        if (count < 1):
            return False
        elif (count < 2 and not (forward in list_of_no)):
            return False
        else:
            return True

    def check_last_wall(self, snake):
        x = snake[0]['x']
        y = snake[0]['y']
        if (x == 0):
            return self.left
        elif (x == self.cell_width - 1):
            return self.right
        elif (y == 0):
            return self.up
        elif (y == self.cell_height - 1):
            return self.down
        else:
            return 0

    def check_smart_turn(self, snake, list_of_no, direction1, direction2):
        if direction1 == self.up or direction1 == self.down:
            if direction2 == self.right:
                if ({'x': snake[self.head]['x']+3,
                     'y': snake[self.head]['y']} in
                    list_of_no and
                    ({'x': snake[self.head]['x']+2, 'y': snake[self.head]['y']}
                     not in list_of_no)):
                    return True
                else:
                    return False
            if direction2 == self.left:
                if ({'x': snake[self.head]['x']-3, 'y': snake[self.head]['y']}
                    in list_of_no and
                    ({'x': snake[self.head]['x']-2, 'y': snake[self.head]['y']}
                     not in list_of_no)):
                    return True
                else:
                    return False
        if (direction1 == self.left or direction1 == self.right):
            if (direction2 == self.up):
                if ({'x': snake[self.head]['x'], 'y': snake[self.head]['y']-3}
                    in list_of_no and
                    ({'x': snake[self.head]['x'], 'y': snake[self.head]['y']-2}
                     not in list_of_no)):
                    return True
                else:
                    return False
            if (direction2 == self.down):
                if ({'x': snake[self.head]['x'],
                     'y': snake[self.head]['y']+3} in list_of_no and
                    ({'x': snake[self.head]['x'],
                      'y': snake[self.head]['y']+2} not in list_of_no)):
                    return True
                else:
                    return False

    def find_better_direction(self, snake, direction, last_wall):
        list_of_no = list(snake)
        # smart_turn = False  # dont kill yourself in the corner
        if (direction == self.up):
            area_left = self.calculate_area(
                {'x': snake[self.head]['x']-1,
                 'y': snake[self.head]['y']}, snake, last_wall)
            area_right = self.calculate_area(
                {'x': snake[self.head]['x']+1,
                 'y': snake[self.head]['y']}, snake, last_wall)
            if (area_left == 0 and area_right == 0):
                return [direction]
            area_straight = self.calculate_area(
                {'x': snake[self.head]['x'],
                 'y': snake[self.head]['y']-1}, snake, last_wall)
            max_area = max(area_left, area_right, area_straight)
            print('Options:', 'left:', area_left, 'right:',
                  area_right, 'straight:', area_straight)
            if (max_area == area_straight):
                return [direction]
            elif (max_area == area_left):
                if (self.check_smart_turn(snake, list_of_no,
                                          direction, self.left)):
                    print('Smart Turn Enabled')
                    return [self.left, self.left]
                else:
                    return [self.left, self.down]
            else:
                if (self.check_smart_turn(snake, list_of_no,
                                          direction, self.right)):
                    print('Smart Turn Enabled')
                    return [self.right, self.right]
                else:
                    return [self.right, self.down]

        if (direction == self.down):
            area_left = self.calculate_area(
                {'x': snake[self.head]['x']-1,
                 'y': snake[self.head]['y']}, snake, last_wall)
            area_right = self.calculate_area(
                {'x': snake[self.head]['x']+1,
                 'y': snake[self.head]['y']}, snake, last_wall)
            if (area_left == 0 and area_right == 0):
                return [direction]
            area_straight = self.calculate_area(
                {'x': snake[self.head]['x'],
                 'y': snake[self.head]['y']+1}, snake, last_wall)
            max_area = max(area_left, area_right, area_straight)
            print('Options:', 'left:', area_left, 'right:',
                  area_right, 'straight:', area_straight)
            if (max_area == area_straight):
                return [direction]
            elif (area_left == max_area):
                if (self.check_smart_turn(snake, list_of_no,
                                          direction, self.left)):
                    print('Smart Turn Enabled')
                    return [self.left, self.left]
                else:
                    return [self.left, self.up]
            else:
                if (self.check_smart_turn(snake, list_of_no,
                                          direction, self.right)):
                    print('Smart Turn Enabled')
                    return [self.right, self.right]
                else:
                    return [self.right, self.up]

        elif (direction == self.left):
            area_up = self.calculate_area(
                {'x': snake[self.head]['x'],
                 'y': snake[self.head]['y'] - 1}, snake, last_wall)
            area_down = self.calculate_area(
                {'x': snake[self.head]['x'],
                 'y': snake[self.head]['y'] + 1}, snake, last_wall)
            if (area_up == 0 and area_down == 0):
                return [direction]
            area_straight = self.calculate_area(
                {'x': snake[self.head]['x']-1,
                 'y': snake[self.head]['y']}, snake, last_wall)
            max_area = max(area_straight, area_up, area_down)
            print('Options:', 'up:', area_up, 'down:',
                  area_down, 'straight:', area_straight)
            if (max_area == area_straight):
                return [direction]
            elif (max_area == area_up):
                if (self.check_smart_turn(snake, list_of_no,
                                          direction, self.up)):
                    print('Smart Turn Enabled')
                    return [self.up, self.up]
                else:
                    return [self.up, self.right]
            else:
                if (self.check_smart_turn(snake, list_of_no,
                                          direction, self.down)):
                    print('Smart Turn Enabled')
                    return [self.down, self.down]
                else:
                    return [self.down, self.right]

        elif (direction == self.right):
            area_up = self.calculate_area(
                {'x': snake[self.head]['x'],
                 'y': snake[self.head]['y'] - 1}, snake, last_wall)
            area_down = self.calculate_area(
                {'x': snake[self.head]['x'],
                 'y': snake[self.head]['y'] + 1}, snake, last_wall)
            if (area_up == 0 and area_down == 0):
                return [direction]
            area_straight = self.calculate_area(
                {'x': snake[self.head]['x']+1,
                 'y': snake[self.head]['y']}, snake, last_wall)
            max_area = max(area_straight, area_up, area_down)
            print('Options:', 'up:', area_up, 'down:',
                  area_down, 'straight:', area_straight)
            if (max_area == area_straight):
                return [direction]
            elif (area_up == max_area):
                if (self.check_smart_turn(snake, list_of_no,
                                          direction, self.up)):
                    print('Smart Turn Enabled')
                    return [self.up, self.up]
                else:
                    return [self.up, self.left]
            else:
                if (self.check_smart_turn(snake, list_of_no,
                                          direction, self.down)):
                    print('Smart Turn Enabled')
                    return [self.down, self.down]
                else:
                    return [self.down, self.left]

    def find_next_direction(self, snake, direction, last_wall):
        # list_of_no = list(snake)
        area_left = self.calculate_area(
            {'x': snake[self.head]['x']-1,
             'y': snake[self.head]['y']}, snake, last_wall)
        area_right = self.calculate_area(
            {'x': snake[self.head]['x']+1,
             'y': snake[self.head]['y']}, snake, last_wall)
        area_up = self.calculate_area(
            {'x': snake[self.head]['x'],
             'y': snake[self.head]['y'] - 1}, snake, last_wall)
        area_down = self.calculate_area(
            {'x': snake[self.head]['x'],
             'y': snake[self.head]['y'] + 1}, snake, last_wall)
        max_area = max(area_left, area_right, area_up, area_down)
        if (max_area == area_up):
            return [self.up]
        elif (max_area == area_down):
            return [self.down]
        elif (max_area == area_left):
            return [self.left]
        else:
            return [self.right]

    def calculate_area(self, point, snake, last_wall):
        next_wall = self.get_next_wall_coords(last_wall)
        if (point in snake or point in self.wall_coords or point in next_wall):
            return 0
        tail_bonus = 0
        q = []
        search_points = []
        search_points.append(point)
        while (search_points):
            i = search_points.pop()
            for each in self.get_neighborhood(i):
                if (each not in q):
                    if (not (each in snake or
                             each in self.wall_coords or
                             point in next_wall)):
                        search_points.append(each)
                if each == snake[-1]:
                    tail_bonus = 200
            q.append(i)
        return len(q)+tail_bonus

    def area_is_too_small(self, bound, point, snake, last_wall):
        next_wall = self.get_next_wall_coords(last_wall)
        if (point in snake or point in self.wall_coords or point in next_wall):
            return True
        tail_bonus = 0
        q = []
        search_points = []
        search_points.append(point)
        while (search_points):
            i = search_points.pop()
            for each in self.get_neighborhood(i):
                if (each not in q):
                    if (not (each in snake or
                             each in self.wall_coords or
                             point in next_wall)):
                        search_points.append(each)
                if (each == snake[-1]):
                    tail_bonus = 200
            q.append(i)
            if ((len(q) + tail_bonus) > bound):
                return False
        return True

    def calculate_direction(self, path_):
        '''Converting point-path_ to step by step direction'''
        last_point = path_[0]
        directions = []
        next_direction = ''
        for current_point in path_:
            if (current_point['x'] > last_point['x']):
                next_direction = self.right
            elif (current_point['x'] < last_point['x']):
                next_direction = self.left
            else:
                if (current_point['y'] > last_point['y']):
                    next_direction = self.down
                elif (current_point['y'] < last_point['y']):
                    next_direction = self.up
                else:
                    # print ('Apple Found...')
                    continue
            # print ('Last Point:', last_point, 'current_point:',
            #        current_point, ' --> ', next_direction)
            last_point = current_point
            directions.append(next_direction)
        # print (directions)
        return directions

    def calculate_path(self, snake, food, soft_calculation):
        old_snake = list(snake)
        # print(new_snake)
        path_ = self.main_calculation(snake, food, soft_calculation)
        if not path_:
            return []
        else:
            path_copy = list(path_)
            path_copy.reverse()
            new_snake = path_copy + old_snake
            path_out = self.main_calculation(new_snake, new_snake[-1], False)
            if not path_out:
                print('No path out, dont go for food')
                return 'stall'
            else:
                return path_

    def main_calculation(self, snake, food, soft_calculation):
        points_to_path = []
        discover_edge = []
        new_points = []
        exhausted_points = []
        nbr_of_points = 1  # if all point tested go back one point
        finding_path = True  # false
        list_of_no = self.get_list_of_no(snake)
        soft_list_of_no = self.get_soft_list_of_no(snake)
        soft_list_of_no.extend(self.soft_wall_coords)
        discover_edge.append(snake[0])
        exhausted_points.append(snake[0])
        last_point = discover_edge[-1]
        points_to_path.append(last_point)

        if ((food in self.soft_wall_coords) or (food in soft_list_of_no)):
            soft_calculation = False

        # calculate avialable path
        while (finding_path and soft_calculation):
            last_point = discover_edge[-1]
            new_points = self.get_neighborhood(last_point)
            new_points = sorted(new_points,
                                key=lambda k: self.calculate_distance(
                                    k, food), reverse=True)  # sort new_points
            nbr_of_points = len(new_points)
            for point in new_points:
                if (point in soft_list_of_no):
                    # print ('No Go Point:', point)
                    nbr_of_points = nbr_of_points - 1
                elif point in exhausted_points:
                    # print ('considered already:', point)
                    nbr_of_points = nbr_of_points - 1
                else:
                    # new points --> discover_edge, closest one last in
                    discover_edge.append(point)
                    points_to_path.append(last_point)
                    exhausted_points.append(last_point)
                    # print (point)
                # exhausted_points.append(point)
            if nbr_of_points == 0:
                # backtrack
                exhausted_points.append(discover_edge.pop())
                exhausted_points.append(points_to_path.pop())
            if food in discover_edge:
                finding_path = 0
            if not discover_edge:
                soft_calculation = False
                break

        # print ('soft_calculation: ', soft_calculation)
        if not soft_calculation:
            points_to_path = []
            discover_edge = []
            new_points = []
            exhausted_points = []
            nbr_of_points = 1  # if all point tested go back one point
            finding_path = True  # false
            list_of_no = self.get_list_of_no(snake)
            discover_edge.append(snake[0])
            exhausted_points.append(snake[0])
            last_point = discover_edge[-1]
            points_to_path.append(last_point)

            # calculate avialable path
            while(finding_path):
                last_point = discover_edge[-1]
                new_points = self.get_neighborhood(last_point)
                # sort new_points
                new_points = sorted(new_points,
                                    key=lambda k: self.calculate_distance(
                                        k, food), reverse=True)
                nbr_of_points = len(new_points)
                for point in new_points:
                    if point in list_of_no:
                        # print ('No Go Point:', point)
                        nbr_of_points = nbr_of_points - 1
                    elif point in exhausted_points:
                        # print ('considered already:', point)
                        nbr_of_points = nbr_of_points - 1
                    else:
                        # new points --> discover_edge, closest one last in
                        discover_edge.append(point)
                        points_to_path.append(last_point)
                        exhausted_points.append(last_point)
                        # print (point)
                    # exhausted_points.append(point)
                if nbr_of_points == 0:
                    # backtrack
                    exhausted_points.append(discover_edge.pop())
                    exhausted_points.append(points_to_path.pop())
                if food in discover_edge:
                    finding_path = 0
                if not discover_edge:
                    # should start stalling since no path found
                    # print ('stalling...')
                    return []
                '''
          # Debugging................
          # Draw path found
          display_surf.fill(bg_color)
          draw_grid()
          draw_snake(snake)
          # draw_edge_of_discovery(discover_edge)
          draw_edge_of_discovery(points_to_path)
          draw_edge_of_discovery(list_of_no)
          draw_food(food)
          pygame.display.update()
          pause_game()
          print ('points to path')
          print (points_to_path)
          '''

        # WHEN DISCOVER EDGE IS EMPTY, TRY FIND TAIL
        points_to_path.append(food)  # adding in the last point
        return points_to_path

    def get_neighborhood(self, point):  # NOT NEGATIVE
        neighborhood = []
        if point['x'] < self.cell_width:
            neighborhood.append({'x': point['x']+1, 'y': point['y']})
        if point['x'] > 0:
            neighborhood.append({'x': point['x']-1, 'y': point['y']})
        if point['y'] < self.cell_height:
            neighborhood.append({'x': point['x'], 'y': point['y']+1})
        if point['y'] > 0:
            neighborhood.append({'x': point['x'], 'y': point['y']-1})
        return neighborhood

    def calculate_distance(self, point, food):
        distance = abs(point['x'] - food['x']) + abs(point['y'] - food['y'])
        return distance

    def get_soft_list_of_no(self, snake):
        list_of_no = []
        list_of_no.extend(self.get_snake_surroundings(snake))
        # list_of_no.extend(soft_wall_coords)
        # remove duplicates
        return list_of_no

    def get_snake_surroundings(self, snake):
        list_of_no = []
        head_x = snake[0]['x']
        head_y = snake[0]['y']
        count = 0
        for each in snake:
            if count == 0:
                list_of_no.append(each)
            else:
                dist = abs(each['x'] - head_x) + abs(each['y']-head_y)
                count_from_behind = len(snake) - count
                if dist < (count_from_behind+1):
                    list_of_no.append(each)
                    list_of_no.append({'x': each['x']+1, 'y': each['y']})
                    list_of_no.append({'x': each['x']-1, 'y': each['y']})
                    list_of_no.append({'x': each['x'], 'y': each['y']+1})
                    list_of_no.append({'x': each['x'], 'y': each['y']-1})
                    list_of_no.append({'x': each['x']+1, 'y': each['y']+1})
                    list_of_no.append({'x': each['x']-1, 'y': each['y']-1})
                    list_of_no.append({'x': each['x']-1, 'y': each['y']+1})
                    list_of_no.append({'x': each['x']+1, 'y': each['y']-1})
            count = count + 1
        seen = set()
        new_list = []
        for d in list_of_no:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_list.append(d)
        return new_list

    def get_list_of_no(self, snake):
        list_of_no = []
        head_x = snake[0]['x']
        head_y = snake[0]['y']
        for idx, node in enumerate(snake):
            dist = abs(node['x'] - head_x) + abs(node['y'] - head_y)
            count_from_behind = len(snake) - idx
            if dist < (count_from_behind+1):
                list_of_no.append(node)
        list_of_no.extend(self.wall_coords)
        return list_of_no

    def find_wall(self):
        walls = []
        # append self.left self.right walls
        loop_count = 0
        for _ in range(self.cell_height):
            walls.append({'x': -1, 'y': loop_count})
            walls.append({'x': self.cell_width, 'y': loop_count})
            loop_count = loop_count + 1
        # append TOP BOTTOM walls
        loop_count = 0
        for _ in range(self.cell_width):
            walls.append({'x': loop_count, 'y': -1})
            walls.append({'x': loop_count, 'y': self.cell_height})
            loop_count = loop_count + 1
        # print (walls)
        return walls

    def find_soft_wall(self):
        walls = []
        # append self.left self.right walls
        loop_count = 0
        for _ in range(self.cell_height):
            walls.append({'x': 0, 'y': loop_count})
            walls.append({'x': self.cell_width-1, 'y': loop_count})
            loop_count = loop_count + 1
        # append TOP BOTTOM walls
        loop_count = 0
        for _ in range(self.cell_width):
            walls.append({'x': loop_count, 'y': 0})
            walls.append({'x': loop_count, 'y': self.cell_height-1})
            loop_count = loop_count + 1
        # print (walls)
        return walls

    def draw_edge_of_discovery(self, points):
        for point in points:
            x = point['x'] * self.cell_size
            y = point['y'] * self.cell_size
            snake_segment_rect = pygame.Rect(
                x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(
                self.display_surf, self.orange, snake_segment_rect)
        # last_point_rect = pygame.Rect(points[-1]['x']*cell_size, points[-1]
        #                               ['y']*cell_size, cell_size, cell_size)
        pygame.draw.rect(
            self.display_surf, (255, 255, 255), snake_segment_rect)
        # print('Drawing Edge of Discovery...')
        # time.sleep(0.05)

    def pause_game(self):
        pause = True
        while (pause):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = False

    def find_new_head(self, direction, snake):
        if direction == self.up:
            new_head = {'x': snake[self.head]['x'],
                        'y': snake[self.head]['y'] - 1}
        elif direction == self.down:
            new_head = {'x': snake[self.head]['x'],
                        'y': snake[self.head]['y'] + 1}
        elif direction == self.left:
            new_head = {'x': snake[self.head]['x'] - 1,
                        'y': snake[self.head]['y']}
        elif direction == self.right:
            new_head = {'x': snake[self.head]['x'] + 1,
                        'y': snake[self.head]['y']}
        return new_head

    """
    ////////////////////////////////////////////////////////////////////////////
    """

    def draw_press_key_msg(self):
        press_key_surf = self.basic_font.render(
            'Press a key to play.', True, self.dark_gray)
        press_key_rect = press_key_surf.get_rect()
        press_key_rect.topleft = (self.window_width - 200,
                                  self.window_height - 30)
        self.display_surf.blit(press_key_surf, press_key_rect)

    def check_for_key_press(self):
        if len(pygame.event.get(pygame.QUIT)) > 0:
            self.terminate()

        key_up_events = pygame.event.get(pygame.KEYUP)
        if len(key_up_events) == 0:
            return None
        if key_up_events[0].key == pygame.K_ESCAPE:
            self.terminate()
        return key_up_events[0].key

    def show_start_screen(self):
        title_font = pygame.font.Font('freesansbold.ttf', 100)
        title_surf1 = title_font.render(
            'Awesome_Snake_AI!', True, self.white, self.dark_green)
        title_surf2 = title_font.render('Awesome_Snake_AI!', True, self.green)

        degrees1 = 0
        degrees2 = 0
        while True:
            self.display_surf.fill(self.bg_color)
            rotated_surf1 = pygame.transform.rotate(title_surf1, degrees1)
            rotated_rect1 = rotated_surf1.get_rect()
            rotated_rect1.center = (int(self.window_width / 2),
                                    int(self.window_height / 2))
            self.display_surf.blit(rotated_surf1, rotated_rect1)

            rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
            rotated_rect2 = rotated_surf2.get_rect()
            rotated_rect2.center = (int(self.window_width / 2),
                                    int(self.window_height / 2))
            self.display_surf.blit(rotated_surf2, rotated_rect2)

            self.draw_press_key_msg()

            if self.check_for_key_press():
                pygame.event.get()  # clear event queue
                return
            pygame.display.update()
            self.fps_clock.tick(self.fps)
            degrees1 += 3  # rotate by 3 degrees each frame
            degrees2 += 7  # rotate by 7 degrees each frame

    def terminate(self):
        print('YOU DIED!')
        self.pause_game()
        pygame.quit()
        sys.exit()

    def get_random_location(self, snake):
        location = {'x': random.randint(0, self.cell_width - 1),
                    'y': random.randint(0, self.cell_height - 1)}
        while(location in snake):
            location = {'x': random.randint(0, self.cell_width - 1),
                        'y': random.randint(0, self.cell_height - 1)}
        return location

    def show_game_over_screen(self):
        game_over_font = pygame.font.Font('freesansbold.ttf', 150)
        game_surf = game_over_font.render('Game', True, self.white)
        overSurf = game_over_font.render('Over', True, self.white)
        game_rect = game_surf.get_rect()
        over_rect = overSurf.get_rect()
        game_rect.midtop = (self.window_width / 2, 10)
        over_rect.midtop = (self.window_width / 2, game_rect.height + 10 + 25)

        self.display_surf.blit(game_surf, game_rect)
        self.display_surf.blit(overSurf, over_rect)
        self.draw_press_key_msg()
        pygame.display.update()
        pygame.time.wait(500)
        # clear out any key presses in the event queue
        self.check_for_key_press()

        while True:
            if self.check_for_key_press():
                pygame.event.get()  # clear event queue
                return

    def draw_score(self, score):
        score_surf = self.basic_font.render(
            'Score: %s' % (score), True, self.white)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (self.window_width - 120, 10)
        self.display_surf.blit(score_surf, score_rect)

    def draw_snake(self, snake):
        for coord in snake:
            x = coord['x'] * self.cell_size
            y = coord['y'] * self.cell_size
            # snake_segment_rect = pygame.Rect(x, y, cell_size, cell_size)
            # pygame.draw.rect(display_surf, white, snake_segment_rect)
            snake_inner_segment_rect = pygame.Rect(
                x + 1, y + 1, self.cell_size - 2, self.cell_size - 2)
            pygame.draw.rect(
                self.display_surf, self.white, snake_inner_segment_rect)
        '''
        x = snake[0]['x'] * cell_size
        y = snake[0]['y'] * cell_size
        snake_segment_rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(display_surf, white, snake_segment_rect)
        x = snake[-1]['x'] * cell_size
        y = snake[-1]['y'] * cell_size
        snake_segment_rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(display_surf, white, snake_segment_rect)
        '''

    def draw_food(self, coord, last_food):
        x = coord['x'] * self.cell_size
        y = coord['y'] * self.cell_size
        food_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.display_surf, self.red, food_rect)
        # x1 = last_food['x'] * cell_size
        # y1 = last_food['y'] * cell_size
        # food_rect = pygame.Rect(x1, y1, cell_size, cell_size)
        # pygame.draw.rect(display_surf, red, food_rect)

    def draw_grid(self):
        return  # do nothing
        # draw vertical lines
        for x in range(0, self.window_width, self.cell_size):
            pygame.draw.line(self.display_surf, self.dark_gray,
                             (x, 0), (x, self.window_height))
        # draw horizontal lines
        for y in range(0, self.window_height, self.cell_size):
            pygame.draw.line(self.display_surf, self.dark_gray,
                             (0, y), (self.window_width, y))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Wormy')
    snake_ai = Snake(fps=60, window_width=1200,
                     window_height=800, cell_size=50)
    snake_ai.show_start_screen()
    while True:
        snake_ai.run_game()
        snake_ai.show_game_over_screen()

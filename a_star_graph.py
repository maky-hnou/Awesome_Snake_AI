import random
import sys

import pygame

fps = 60
window_width = 1200
window_height = 800
cell_size = 50
assert window_width % cell_size == 0, \
    "Window width must be a multiple of cell size."
assert window_height % cell_size == 0, \
    "Window height must be a multiple of cell size."
cell_width = int(window_width / cell_size)
cell_height = int(window_height / cell_size)

#         R    G    B
white = (255, 255, 255)
grey = (200, 200, 200)
pink = (198, 134, 156)
black = (17,  18,  13)
red = (255,   0,   0)
green = (0, 255,   0)
dark_green = (0, 155,   0)
dark_gray = (40,  40,  40)
orange = (255, 155, 111)
bg_color = black

up_dir = 'up'
down_dir = 'down'
left_dir = 'left'
right_dir = 'right'


snake_head = 0  # syntactic sugar: index of the snake's head


def main():
    global fps_clock, display_surf, basic_font
    global wall_coords, soft_wall_coords
    wall_coords = []
    soft_wall_coords = []
    soft_wall_coords = find_soft_wall()
    wall_coords = findWall()
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((window_width, window_height))
    basic_font = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    # OUTPUT PRINT TO FILE
    # os.remove("test.txt")
    # sys.stdout=open("test.txt","w")

    while True:
        run_game()
        show_game_over_screen()


def run_game():
    global stalling
    stalling = False
    stalling_count = -1
    # Set a random start point.
    # start_x = random.randint(5, cell_width - 6)
    # start_y = random.randint(5, cell_height - 6)
    start_x = 5
    start_y = 0
    snake = [{'x': start_x + 6, 'y': start_y},
             {'x': start_x + 5, 'y': start_y},
             {'x': start_x + 4, 'y': start_y},
             ]

    direction = right_dir
    directions_list = [right_dir]
    path = []

    # Start the food in a random place.
    # food = get_random_location(snake)
    food = {'x': start_x+8,     'y': start_y}
    # food = {'x': start_x-1,     'y': start_y-1}
    last_food = {'x': start_x-1,   'y': start_y - 1}
    path = calculate_path(snake, food, True)
    directions_list = calculate_direction(path)
    last_wall = 0

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
        # check if the snake has hit itself or the edge
        if (snake[snake_head]['x'] == -1 or
            snake[snake_head]['x'] == cell_width or
            snake[snake_head]['y'] == -1 or
                snake[snake_head]['y'] == cell_height):
            terminate()
            return  # game over

        for snake_cell in snake[1:]:
            # sys.exit()
            if (snake_cell['x'] == snake[snake_head]['x'] and
                    snake_cell['y'] == snake[snake_head]['y']):
                terminate()
                return  # game over
        # check if snake has eaten an apply
        if (snake[snake_head]['x'] == food['x'] and
                snake[snake_head]['y'] == food['y']):
            # don't remove snake's tail segment
            last_food = food
            food = get_random_location(snake)  # set a new food somewhere
            draw_food(food, last_food)  # for testing purposes
            # draw_food(last_food)
            # section_break() #just print some crap
            path = calculate_path(snake, food, True)  # calculate path to go
            if not path:
                stalling = True
                stalling_count = 10000
            elif path == 'stall':
                stalling = True
                stalling_count = int(len(snake)/2)
            else:
                directions_list = calculate_direction(path)
        else:
            del snake[-1]  # remove snake's tail segment

        last_direction = direction

        '''finding next direction'''
        # if (stalling and len(directions_list) == 1 and
        #         snake[0] in soft_wall_coords):
        # print('special case')
        # directions_list.extend(find_better_direction(snake,direction,0))
        if stalling and not directions_list:
            only_direction = calculate_only_direction(snake)
            if only_direction and only_direction == last_direction:
                directions_list.append(only_direction)
                print('only direction:', direction)
            else:
                if safe_to_go(snake, direction, last_wall):
                    # print('safe')
                    # continue the previous direction
                    directions_list.append(direction)
                elif ((not find_new_head(direction, snake) in snake) or
                      (find_new_head(direction, snake) in wall_coords)):
                    directions_list.append(direction)
                else:
                    last_direction = direction
                    # check if path can be found, if yes override
                    # previous calcualtion
                    path = calculate_path(snake, food, False)
                    if path != [] and path != 'stall':
                        stalling = False
                        stalling_count = -1
                        directions_list = calculate_direction(path)
                    else:
                        if check_last_wall(snake):
                            last_wall = check_last_wall(snake)
                        directions_list.extend(
                            find_better_direction(snake, direction, last_wall))
                        if calculate_area(
                                find_new_head(directions_list[0], snake),
                                snake, last_wall) < 3:
                            directions_list = [last_direction]
                        # print(directions_list)
                stalling_count = stalling_count - 1
                # print ('stalling Count:', stalling_count)
                if stalling_count < 1:
                    # print('stalling Count',stalling_count)
                    stalling = False
                    prev_last_wall = last_wall
                    last_wall = 0
                    directions_list.append(last_direction)
                    # calculate path to go
                    path = calculate_path(snake, food, True)
                    if not path:
                        stalling = True
                        stalling_count = 10000
                        last_wall = prev_last_wall
                    elif path == 'stall':
                        stalling = True
                        stalling_count = int(len(snake)/2)
                        last_wall = prev_last_wall
                    else:
                        directions_list = calculate_direction(path)
        next_head = find_new_head(directions_list[0], snake)
        '''
        if (next_head in snake or next_head in wall_coords or next_head in
            get_next_wall_coords(last_wall)):  #if gonig to die go into tunnel
          last_wall = 0
          directions_list = find_next_direction(snake, directions_list[0],0)
          print('going into tunnel')
        '''
        if stalling:
            # return true if the area going in is too small
            if area_is_too_small(cell_width, next_head, snake, last_wall):
                last_wall = 0
                directions_list = find_next_direction(
                    snake, directions_list[0], 0)
                print('almost died, recalcualting...',
                      snake[0], directions_list)

        direction = directions_list.pop(0)
        new_head = find_new_head(direction, snake)
        snake.insert(0, new_head)
        display_surf.fill(bg_color)
        draw_grid()
        draw_snake(snake)
        draw_food(food, last_food)
        draw_score(len(snake) - 3)
        pygame.display.update()
        fps_clock.tick(fps)


def calculate_only_direction(snake):
    count = 4
    ways = get_neighborhood(snake[0])
    the_way = 0
    for each in ways:
        if each in snake:
            count = count - 1
        else:
            the_way = each
    if count == 1:
        return calculate_direction([snake[0], the_way])
    else:
        return 0


def get_next_wall_coords(last_wall):
    walls = []
    # append left_dir right_dir walls
    loop_count = 0
    for _ in range(cell_height):
        if last_wall == right_dir:
            walls.append({'x': 0, 'y': loop_count})
        if last_wall == left_dir:
            walls.append({'x': cell_width-1, 'y': loop_count})
        loop_count = loop_count + 1
    # append TOP BOTTOM walls
    loop_count = 0
    for _ in range(cell_width):
        if last_wall == down_dir:
            walls.append({'x': loop_count, 'y': 0})
        if last_wall == up_dir:
            walls.append({'x': loop_count, 'y': cell_height-1})
        loop_count = loop_count + 1
    return walls


def safe_to_go(snake, direction, last_wall):
    list_of_no = wall_coords + snake
    list_of_no.extend(get_next_wall_coords(last_wall))
    # head = snake[0]
    forward = snake[0]
    forward_left = snake[0]
    forward_right = snake[0]
    left = snake[0]
    right = snake[0]
    if direction == up_dir:
        new_head = {'x': snake[snake_head]['x'],
                    'y': snake[snake_head]['y'] - 1}
        forward = {'x': snake[snake_head]['x'],
                   'y': snake[snake_head]['y'] - 2}
        forward_left = {'x': snake[snake_head]['x']-1,
                        'y': snake[snake_head]['y'] - 1}
        forward_right = {'x': snake[snake_head]['x']+1,
                         'y': snake[snake_head]['y'] - 1}
        left = {'x': snake[snake_head]['x']-1,
                'y': snake[snake_head]['y']}
        right = {'x': snake[snake_head]['x']+1,
                 'y': snake[snake_head]['y']}
        # print('new head:', new_head)
        # print('forward:', forward)
        # print('forward left:', forward_left)
        # print('forward right:', forward_right)
        # print('left:', left)
        # print('right:', right)
        # sys.ewit(0)
    elif direction == down_dir:
        new_head = {'x': snake[snake_head]['x'],
                    'y': snake[snake_head]['y'] + 1}
        forward = {'x': snake[snake_head]['x'],
                   'y': snake[snake_head]['y'] + 2}
        forward_left = {'x': snake[snake_head]['x']-1,
                        'y': snake[snake_head]['y'] + 1}
        forward_right = {'x': snake[snake_head]['x']+1,
                         'y': snake[snake_head]['y'] + 1}
        left = {'x': snake[snake_head]['x']-1,
                'y': snake[snake_head]['y']}
        right = {'x': snake[snake_head]['x']+1,
                 'y': snake[snake_head]['y']}
    elif direction == left_dir:
        new_head = {'x': snake[snake_head]['x'] - 1,
                    'y': snake[snake_head]['y']}
        forward = {'x': snake[snake_head]['x'] - 2,
                   'y': snake[snake_head]['y']}
        forward_left = {'x': snake[snake_head]['x']-1,
                        'y': snake[snake_head]['y'] + 1}
        forward_right = {'x': snake[snake_head]['x']-1,
                         'y': snake[snake_head]['y'] - 1}
        left = {'x': snake[snake_head]['x'],
                'y': snake[snake_head]['y']+1}
        right = {'x': snake[snake_head]['x'],
                 'y': snake[snake_head]['y']-1}
    elif direction == right_dir:
        new_head = {'x': snake[snake_head]['x'] + 1,
                    'y': snake[snake_head]['y']}
        forward = {'x': snake[snake_head]['x'] + 2,
                   'y': snake[snake_head]['y']}
        forward_left = {'x': snake[snake_head]['x']+1,
                        'y': snake[snake_head]['y'] - 1}
        forward_right = {'x': snake[snake_head]['x']+1,
                         'y': snake[snake_head]['y'] + 1}
        left = {'x': snake[snake_head]['x'],
                'y': snake[snake_head]['y']-1}
        right = {'x': snake[snake_head]['x'],
                 'y': snake[snake_head]['y']+1}

    # print ('newhead',new_head,'no go:',list_of_no)
    if ((forward_left in list_of_no and left not in list_of_no) or
            (forward_right in list_of_no and right not in list_of_no)):
        # print ('forwardleft left detected', forward_left, left,
        #        'right:', forward_right, right)
        return False
    if new_head in list_of_no:
        return False
    ways_to_go = []
    ways_to_go = get_neighborhood(new_head)
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


def check_last_wall(snake):
    x = snake[0]['x']
    y = snake[0]['y']
    if (x == 0):
        return left_dir
    elif (x == cell_width - 1):
        return right_dir
    elif (y == 0):
        return up_dir
    elif (y == cell_height - 1):
        return down_dir
    else:
        return 0


def check_smart_turn(snake, list_of_no, direction1, direction2):
    if direction1 == up_dir or direction1 == down_dir:
        if direction2 == right_dir:
            if ({'x': snake[snake_head]['x']+3, 'y': snake[snake_head]['y']} in
                list_of_no and
                ({'x': snake[snake_head]['x']+2, 'y': snake[snake_head]['y']}
                 not in list_of_no)):
                return True
            else:
                return False
        if direction2 == left_dir:
            if ({'x': snake[snake_head]['x']-3, 'y': snake[snake_head]['y']}
                in list_of_no and
                ({'x': snake[snake_head]['x']-2, 'y': snake[snake_head]['y']}
                 not in list_of_no)):
                return True
            else:
                return False
    if (direction1 == left_dir or direction1 == right_dir):
        if (direction2 == up_dir):
            if ({'x': snake[snake_head]['x'], 'y': snake[snake_head]['y']-3}
                in list_of_no and
                ({'x': snake[snake_head]['x'], 'y': snake[snake_head]['y']-2}
                 not in list_of_no)):
                return True
            else:
                return False
        if (direction2 == down_dir):
            if ({'x': snake[snake_head]['x'], 'y': snake[snake_head]['y']+3} in
                list_of_no and
                ({'x': snake[snake_head]['x'], 'y': snake[snake_head]['y']+2}
                 not in list_of_no)):
                return True
            else:
                return False


def find_better_direction(snake, direction, last_wall):
    list_of_no = list(snake)
    # smart_turn = False  # dont kill yourself in the corner
    if (direction == up_dir):
        area_left = calculate_area(
            {'x': snake[snake_head]['x']-1,
             'y': snake[snake_head]['y']}, snake, last_wall)
        area_right = calculate_area(
            {'x': snake[snake_head]['x']+1,
             'y': snake[snake_head]['y']}, snake, last_wall)
        if (area_left == 0 and area_right == 0):
            return [direction]
        area_straight = calculate_area(
            {'x': snake[snake_head]['x'],
             'y': snake[snake_head]['y']-1}, snake, last_wall)
        max_area = max(area_left, area_right, area_straight)
        print('Options:', 'left:', area_left, 'right:',
              area_right, 'straight:', area_straight)
        if (max_area == area_straight):
            return [direction]
        elif (max_area == area_left):
            if (check_smart_turn(snake, list_of_no, direction, left_dir)):
                print('Smart Turn Enabled')
                return [left_dir, left_dir]
            else:
                return [left_dir, down_dir]
        else:
            if (check_smart_turn(snake, list_of_no, direction, right_dir)):
                print('Smart Turn Enabled')
                return [right_dir, right_dir]
            else:
                return [right_dir, down_dir]

    if (direction == down_dir):
        area_left = calculate_area(
            {'x': snake[snake_head]['x']-1,
             'y': snake[snake_head]['y']}, snake, last_wall)
        area_right = calculate_area(
            {'x': snake[snake_head]['x']+1,
             'y': snake[snake_head]['y']}, snake, last_wall)
        if (area_left == 0 and area_right == 0):
            return [direction]
        area_straight = calculate_area(
            {'x': snake[snake_head]['x'],
             'y': snake[snake_head]['y']+1}, snake, last_wall)
        max_area = max(area_left, area_right, area_straight)
        print('Options:', 'left:', area_left, 'right:',
              area_right, 'straight:', area_straight)
        if (max_area == area_straight):
            return [direction]
        elif (area_left == max_area):
            if (check_smart_turn(snake, list_of_no, direction, left_dir)):
                print('Smart Turn Enabled')
                return [left_dir, left_dir]
            else:
                return [left_dir, up_dir]
        else:
            if (check_smart_turn(snake, list_of_no, direction, right_dir)):
                print('Smart Turn Enabled')
                return [right_dir, right_dir]
            else:
                return [right_dir, up_dir]

    elif (direction == left_dir):
        area_up = calculate_area(
            {'x': snake[snake_head]['x'],
             'y': snake[snake_head]['y'] - 1}, snake, last_wall)
        area_down = calculate_area(
            {'x': snake[snake_head]['x'],
             'y': snake[snake_head]['y'] + 1}, snake, last_wall)
        if (area_up == 0 and area_down == 0):
            return [direction]
        area_straight = calculate_area(
            {'x': snake[snake_head]['x']-1,
             'y': snake[snake_head]['y']}, snake, last_wall)
        max_area = max(area_straight, area_up, area_down)
        print('Options:', 'up:', area_up, 'down:',
              area_down, 'straight:', area_straight)
        if (max_area == area_straight):
            return [direction]
        elif (max_area == area_up):
            if (check_smart_turn(snake, list_of_no, direction, up_dir)):
                print('Smart Turn Enabled')
                return [up_dir, up_dir]
            else:
                return [up_dir, right_dir]
        else:
            if (check_smart_turn(snake, list_of_no, direction, down_dir)):
                print('Smart Turn Enabled')
                return [down_dir, down_dir]
            else:
                return [down_dir, right_dir]

    elif (direction == right_dir):
        area_up = calculate_area(
            {'x': snake[snake_head]['x'],
             'y': snake[snake_head]['y'] - 1}, snake, last_wall)
        area_down = calculate_area(
            {'x': snake[snake_head]['x'],
             'y': snake[snake_head]['y'] + 1}, snake, last_wall)
        if (area_up == 0 and area_down == 0):
            return [direction]
        area_straight = calculate_area(
            {'x': snake[snake_head]['x']+1,
             'y': snake[snake_head]['y']}, snake, last_wall)
        max_area = max(area_straight, area_up, area_down)
        print('Options:', 'up:', area_up, 'down:',
              area_down, 'straight:', area_straight)
        if (max_area == area_straight):
            return [direction]
        elif (area_up == max_area):
            if (check_smart_turn(snake, list_of_no, direction, up_dir)):
                print('Smart Turn Enabled')
                return [up_dir, up_dir]
            else:
                return [up_dir, left_dir]
        else:
            if (check_smart_turn(snake, list_of_no, direction, down_dir)):
                print('Smart Turn Enabled')
                return [down_dir, down_dir]
            else:
                return [down_dir, left_dir]


def find_next_direction(snake, direction, last_wall):
    # list_of_no = list(snake)
    area_left = calculate_area(
        {'x': snake[snake_head]['x']-1,
         'y': snake[snake_head]['y']}, snake, last_wall)
    area_right = calculate_area(
        {'x': snake[snake_head]['x']+1,
         'y': snake[snake_head]['y']}, snake, last_wall)
    area_up = calculate_area(
        {'x': snake[snake_head]['x'],
         'y': snake[snake_head]['y'] - 1}, snake, last_wall)
    area_down = calculate_area(
        {'x': snake[snake_head]['x'],
         'y': snake[snake_head]['y'] + 1}, snake, last_wall)
    max_area = max(area_left, area_right, area_up, area_down)
    if (max_area == area_up):
        return [up_dir]
    elif (max_area == area_down):
        return [down_dir]
    elif (max_area == area_left):
        return [left_dir]
    else:
        return [right_dir]


def calculate_area(point, snake, last_wall):
    next_wall = get_next_wall_coords(last_wall)
    if (point in snake or point in wall_coords or point in next_wall):
        return 0
    tail_bonus = 0
    q = []
    search_points = []
    search_points.append(point)
    while (search_points):
        i = search_points.pop()
        for each in get_neighborhood(i):
            if (each not in q):
                if (not (each in snake or
                         each in wall_coords or
                         point in next_wall)):
                    search_points.append(each)
            if each == snake[-1]:
                tail_bonus = 200
        q.append(i)
    return len(q)+tail_bonus


def area_is_too_small(bound, point, snake, last_wall):
    next_wall = get_next_wall_coords(last_wall)
    if (point in snake or point in wall_coords or point in next_wall):
        return True
    tail_bonus = 0
    q = []
    search_points = []
    search_points.append(point)
    while (search_points):
        i = search_points.pop()
        for each in get_neighborhood(i):
            if (each not in q):
                if (not (each in snake or
                         each in wall_coords or
                         point in next_wall)):
                    search_points.append(each)
            if (each == snake[-1]):
                tail_bonus = 200
        q.append(i)
        if ((len(q) + tail_bonus) > bound):
            return False
    return True


def calcCost(point, snake):
    print('calculating cost of point', point)
    neibors = get_neighborhood(point)
    for each in neibors:
        if (each in snake[1:]):
            return snake.index(each)
    return 999


def calculate_direction(path_):
    '''Converting point-path_ to step by step direction'''
    last_point = path_[0]
    directions = []
    next_direction = ''
    for current_point in path_:
        if (current_point['x'] > last_point['x']):
            next_direction = right_dir
        elif (current_point['x'] < last_point['x']):
            next_direction = left_dir
        else:
            if (current_point['y'] > last_point['y']):
                next_direction = down_dir
            elif (current_point['y'] < last_point['y']):
                next_direction = up_dir
            else:
                # print ('Apple Found...')
                continue
        # print ('Last Point:', last_point, 'current_point:',
        #        current_point, ' --> ', next_direction)
        last_point = current_point
        directions.append(next_direction)
    # print (directions)
    return directions


def calculate_path(snake, food, soft_calculation):
    old_snake = list(snake)
    # print(new_snake)
    path_ = main_calculation(snake, food, soft_calculation)
    if (not path_):
        return []
    else:
        path_copy = list(path_)
        path_copy.reverse()
        new_snake = path_copy + old_snake
        path_out = main_calculation(new_snake, new_snake[-1], False)
        if (not path_out):
            print('No path out, dont go for food')
            return 'stall'
        else:
            return path_


def main_calculation(snake, food, soft_calculation):
    points_to_path = []
    discover_edge = []
    new_points = []
    exhausted_points = []
    nbr_of_points = 1  # if all point tested go back one point
    finding_path = True  # false
    list_of_no = get_list_of_no(snake)
    soft_list_of_no = get_soft_list_of_no(snake)
    soft_list_of_no.extend(soft_wall_coords)
    discover_edge.append(snake[0])
    exhausted_points.append(snake[0])
    last_point = discover_edge[-1]
    points_to_path.append(last_point)

    if ((food in soft_wall_coords) or (food in soft_list_of_no)):
        soft_calculation = False

    # calculate avialable path
    while (finding_path and soft_calculation):
        last_point = discover_edge[-1]
        new_points = get_neighborhood(last_point)
        new_points = sorted(new_points, key=lambda k: calculate_distance(
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
        list_of_no = get_list_of_no(snake)
        discover_edge.append(snake[0])
        exhausted_points.append(snake[0])
        last_point = discover_edge[-1]
        points_to_path.append(last_point)

        # calculate avialable path
        while(finding_path):
            last_point = discover_edge[-1]
            new_points = get_neighborhood(last_point)
            new_points = sorted(new_points, key=lambda k: calculate_distance(
                k, food), reverse=True)  # sort new_points
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
      #Debugging................
      #Draw path found
      display_surf.fill(bg_color)
      draw_grid()
      draw_snake(snake)
      #draw_edge_of_discovery(discover_edge)
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


def get_neighborhood(point):  # NOT NEGATIVE
    neighborhood = []
    if point['x'] < cell_width:
        neighborhood.append({'x': point['x']+1, 'y': point['y']})
    if point['x'] > 0:
        neighborhood.append({'x': point['x']-1, 'y': point['y']})
    if point['y'] < cell_height:
        neighborhood.append({'x': point['x'], 'y': point['y']+1})
    if point['y'] > 0:
        neighborhood.append({'x': point['x'], 'y': point['y']-1})
    return neighborhood


def calculate_distance(point, food):
    distance = abs(point['x'] - food['x']) + abs(point['y'] - food['y'])
    return distance


def get_soft_list_of_no(snake):
    list_of_no = []
    list_of_no.extend(get_snake_surroundings(snake))
    # list_of_no.extend(soft_wall_coords)
    # remove duplicates
    return list_of_no


def get_snake_surroundings(snake):
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
    newList = []
    for d in list_of_no:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            newList.append(d)
    return newList


def get_list_of_no(snake):
    list_of_no = []
    head_x = snake[0]['x']
    head_y = snake[0]['y']
    count = 0
    for each in snake:
        dist = abs(each['x'] - head_x) + abs(each['y']-head_y)
        count_from_behind = len(snake) - count
        count = count + 1
        if dist < (count_from_behind+1):
            list_of_no.append(each)
    list_of_no.extend(wall_coords)
    # print ('List of No Go:')
    # print (list_of_no)
    return list_of_no


def findWall():
    walls = []
    # append left_dir right_dir walls
    loop_count = 0
    for _ in range(cell_height):
        walls.append({'x': -1, 'y': loop_count})
        walls.append({'x': cell_width, 'y': loop_count})
        loop_count = loop_count + 1
    # append TOP BOTTOM walls
    loop_count = 0
    for _ in range(cell_width):
        walls.append({'x': loop_count, 'y': -1})
        walls.append({'x': loop_count, 'y': cell_height})
        loop_count = loop_count + 1
    # print (walls)
    return walls


def find_soft_wall():
    walls = []
    # append left_dir right_dir walls
    loop_count = 0
    for _ in range(cell_height):
        walls.append({'x': 0, 'y': loop_count})
        walls.append({'x': cell_width-1, 'y': loop_count})
        loop_count = loop_count + 1
    # append TOP BOTTOM walls
    loop_count = 0
    for _ in range(cell_width):
        walls.append({'x': loop_count, 'y': 0})
        walls.append({'x': loop_count, 'y': cell_height-1})
        loop_count = loop_count + 1
    # print (walls)
    return walls


def draw_edge_of_discovery(points):
    for point in points:
        x = point['x'] * cell_size
        y = point['y'] * cell_size
        snake_segment_rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(display_surf, orange, snake_segment_rect)
    # last_point_rect = pygame.Rect(points[-1]['x']*cell_size, points[-1]
    #                               ['y']*cell_size, cell_size, cell_size)
    pygame.draw.rect(display_surf, (255, 255, 255), snake_segment_rect)
    # print('Drawing Edge of Discovery...')
    # time.sleep(0.05)


def section_break():
    print('AAAAAAAAAAAAAAAAAAAA')
    print('AAAAAAAAAAAAAAAAAAAA')
    print('AAAAAAAAAAAAAAAAAAAA')
    print('AAAAAAAAAAAAAAAAAAAA')
    print('AAAAAAAAAAAAAAAAAAAA')
    print('AAAAAAAAAAAAAAAAAAAA')
    print('AAAAAAAAAAAAAAAAAAAA')


def pause_game():
    pause = True
    while (pause):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = False


def opposite_direction(direction):
    if direction == up_dir:
        return down_dir
    elif direction == down_dir:
        return up_dir
    elif direction == left_dir:
        return right_dir
    elif direction == right_dir:
        return left_dir


def find_new_head(direction, snake):
    if direction == up_dir:
        new_head = {'x': snake[snake_head]['x'],
                    'y': snake[snake_head]['y'] - 1}
    elif direction == down_dir:
        new_head = {'x': snake[snake_head]['x'],
                    'y': snake[snake_head]['y'] + 1}
    elif direction == left_dir:
        new_head = {'x': snake[snake_head]['x'] - 1,
                    'y': snake[snake_head]['y']}
    elif direction == right_dir:
        new_head = {'x': snake[snake_head]['x'] + 1,
                    'y': snake[snake_head]['y']}
    return new_head


"""
////////////////////////////////////////////////////////////////////////////
"""


def draw_press_key_msg():
    press_key_surf = basic_font.render('Press a key to play.', True, dark_gray)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (window_width - 200, window_height - 30)
    display_surf.blit(press_key_surf, press_key_rect)


def check_for_key_press():
    if len(pygame.event.get(pygame.QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(pygame.KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == pygame.K_ESCAPE:
        terminate()
    return key_up_events[0].key


def show_start_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surf1 = title_font.render('Wormy!', True, white, dark_green)
    title_surf2 = title_font.render('Wormy!', True, green)

    degrees1 = 0
    degrees2 = 0
    while True:
        display_surf.fill(bg_color)
        rotated_surf1 = pygame.transform.rotate(title_surf1, degrees1)
        rotated_rect1 = rotated_surf1.get_rect()
        rotated_rect1.center = (window_width / 2, window_height / 2)
        display_surf.blit(rotated_surf1, rotated_rect1)

        rotated_surf2 = pygame.transform.rotate(title_surf2, degrees2)
        rotated_rect2 = rotated_surf2.get_rect()
        rotated_rect2.center = (window_width / 2, window_height / 2)
        display_surf.blit(rotated_surf2, rotated_rect2)

        draw_press_key_msg()

        if check_for_key_press():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        fps_clock.tick(fps)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    print('YOU DIED!')
    pause_game()
    pygame.quit()
    sys.exit()


def get_random_location(snake):
    location = {'x': random.randint(0, cell_width - 1),
                'y': random.randint(0, cell_height - 1)}
    while(location in snake):
        location = {'x': random.randint(0, cell_width - 1),
                    'y': random.randint(0, cell_height - 1)}
    return location


def show_game_over_screen():
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surf = game_over_font.render('Game', True, white)
    overSurf = game_over_font.render('Over', True, white)
    game_rect = game_surf.get_rect()
    over_rect = overSurf.get_rect()
    game_rect.midtop = (window_width / 2, 10)
    over_rect.midtop = (window_width / 2, game_rect.height + 10 + 25)

    display_surf.blit(game_surf, game_rect)
    display_surf.blit(overSurf, over_rect)
    draw_press_key_msg()
    pygame.display.update()
    pygame.time.wait(500)
    # clear out any key presses in the event queue
    check_for_key_press()

    while True:
        if check_for_key_press():
            pygame.event.get()  # clear event queue
            return


def draw_score(score):
    score_surf = basic_font.render('Score: %s' % (score), True, white)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (window_width - 120, 10)
    display_surf.blit(score_surf, score_rect)


def draw_snake(snake):
    for coord in snake:
        x = coord['x'] * cell_size
        y = coord['y'] * cell_size
        # snake_segment_rect = pygame.Rect(x, y, cell_size, cell_size)
        # pygame.draw.rect(display_surf, white, snake_segment_rect)
        snake_inner_segment_rect = pygame.Rect(
            x + 1, y + 1, cell_size - 2, cell_size - 2)
        pygame.draw.rect(display_surf, white, snake_inner_segment_rect)
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


def draw_food(coord, last_food):
    x = coord['x'] * cell_size
    y = coord['y'] * cell_size
    food_rect = pygame.Rect(x, y, cell_size, cell_size)
    pygame.draw.rect(display_surf, red, food_rect)
    # x1 = last_food['x'] * cell_size
    # y1 = last_food['y'] * cell_size
    # food_rect = pygame.Rect(x1, y1, cell_size, cell_size)
    # pygame.draw.rect(display_surf, red, food_rect)


def draw_grid():
    return  # do nothing
    for x in range(0, window_width, cell_size):  # draw vertical lines
        pygame.draw.line(display_surf, dark_gray, (x, 0), (x, window_height))
    for y in range(0, window_height, cell_size):  # draw horizontal lines
        pygame.draw.line(display_surf, dark_gray, (0, y), (window_width, y))


if __name__ == '__main__':
    main()

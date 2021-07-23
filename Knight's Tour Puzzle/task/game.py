KNIGHT_MOVES = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
POSSIBLE_STATUS = tuple(str(x) for x in range(8))
PRINTABLE_STATUS = ('X', '*') + POSSIBLE_STATUS


def check_in_table(position):
    pos_x, pos_y = position
    if 1 <= pos_x <= table_x and 1 <= pos_y <= table_y:
        return True
    else:
        return None


def previous_movements(table, position):
    row, column_in_row = convert_position(position)
    if table[row][column_in_row] == '*':
        return True
    else:
        return False


def ask_position(first_move):
    while True:
        print("Enter the knight's starting position: " if first_move else "Enter your next move: ", end='')
        position = ask_and_check_input()
        if position is not None and check_in_table(position):
            return position
        else:
            print('Invalid position!')


def ask_dimensions():
    while True:
        print("Enter your board dimensions: ", end='')
        dimension = ask_and_check_input()
        if dimension is not None and 1 <= dimension[0] and 1 <= dimension[1]:
            return dimension
        else:
            print('Invalid dimensions!')


def ask_and_check_input():
    try:
        coordinates = [int(coordinate) for coordinate in input().split()]
    except (ValueError, TypeError):
        return None
    else:
        if len(coordinates) == 2:
            return coordinates


def draw_table(table, solve_trigger):
    print(' ' * max_placeholder_column, '-' * ((cell_size + 1) * table_x + 3), sep='')
    for i in reversed(range(table_y)):
        print(f'{" " if max_placeholder_column > 1 and i + 1 < 10 else ""}{i + 1}| ', end='')
        for j in range(table_x):
            if solve_trigger:
                print(' ' * (cell_size - 2) + (str(table[i][j]) if len(str(table[i][j])) > 1
                                               else ' ' + str(table[i][j])), end=' ')
            else:
                print(' ' * (cell_size - 1) + table[i][j] if table[i][j] in PRINTABLE_STATUS
                      else '_' * cell_size, end=' ')
        print('|')
    print(' ' * max_placeholder_column, '-' * ((cell_size + 1) * table_x + 3), sep='')
    print(' ' * (max_placeholder_column + 2), end='')
    for i in range(table_x):
        print(' ' if cell_size > 1 and table_x < 10 else '', ' ' if cell_size == 3 else '',
              f' {i + 1}' if max_placeholder_row > 1 and i + 1 < 10 else f'{i + 1}', sep='', end=' ')
    print('\n') if not solve_trigger else print()


def add_position_to_table(table, position, sign):
    row, column_in_row = convert_position(position)
    table[row][column_in_row] = sign


def create_table(sign):
    new_table = [[sign for _ in range(table_x)] for _ in range(table_y)]
    return new_table


def update_table(table):
    for row in range(table_y):
        for column_in_row in range(table_x):
            if table[row][column_in_row] == 'X':
                table[row][column_in_row] = '*'
            elif table[row][column_in_row] in POSSIBLE_STATUS:
                table[row][column_in_row] = '_'


def number_of_possible_movements(table, position):
    pos_x, pos_y = position
    count = 0
    for move in KNIGHT_MOVES:
        move_x, move_y = move
        possible_movement = [pos_x + move_x, pos_y + move_y]
        if check_in_table(possible_movement) and not previous_movements(table, possible_movement):
            count += 1
    return str(count - 1)


def add_count_possible_moves(table, position):
    pos_x, pos_y = position
    count = 0
    for move in KNIGHT_MOVES:
        move_x, move_y = move
        possible_movement = [pos_x + move_x, pos_y + move_y]
        if check_in_table(possible_movement) and not previous_movements(table, possible_movement):
            count += 1
            number_of_movements = number_of_possible_movements(table, possible_movement)
            add_position_to_table(table, possible_movement, number_of_movements)
    return count


def solve_table(table, position, count):
    pos_x, pos_y = position
    for move in KNIGHT_MOVES:
        move_x, move_y = move
        if count >= max_squares + 1:
            return True
        new_pos_x = pos_x + move_x
        new_pos_y = pos_y + move_y
        if validate_move_for_solving(table, [new_pos_x, new_pos_y]):
            add_position_to_table(table, [new_pos_x, new_pos_y], count)
            if solve_table(table, [new_pos_x, new_pos_y], count + 1):
                return True
            add_position_to_table(table, [new_pos_x, new_pos_y], 0)
    return False


def validate_move_for_solving(table, position):
    x_pos, y_pos = position
    row, column_in_row = convert_position(position)
    if 1 <= x_pos <= table_x and 1 <= y_pos <= table_y and table[row][column_in_row] == 0:
        return True


def convert_position(position):
    return [position[1] - 1, position[0] - 1]


def ask_to_puzzle():
    while True:
        print('Do you want to try the puzzle? (y/n): ', end='')
        answer = input()
        if answer in ('y', 'n'):
            break
        print('Invalid option')
    return True if answer == 'y' else False


def table_sum_up(n):
    if n == 0:
        return 0
    return table_sum_up(n - 1) + n


def exist_solution(table):
    return table_sum_up(max_squares) == sum([sum(row) for row in table])


def check_possible_status(table, position):
    row, column_in_row = convert_position(position)
    return table[row][column_in_row] in POSSIBLE_STATUS


table_x, table_y = ask_dimensions()
max_squares = table_x * table_y
max_placeholder_row = 1 if table_x < 10 else 2
max_placeholder_column = 1 if table_y < 10 else 2
cell_size = len(str(table_x * table_y))

count_visited_squares = 1

knight_position = ask_position(True)
try_to_puzzle = ask_to_puzzle()

table_for_solving = create_table(0)
add_position_to_table(table_for_solving, knight_position, 1)
solve_table(table_for_solving, knight_position, 2)

if not exist_solution(table_for_solving):
    print('No solution exists!')
else:
    if not try_to_puzzle:
        print("\nHere's the solution!")
        draw_table(table_for_solving, True)
    else:
        table_for_playing = create_table('_')
        add_position_to_table(table_for_playing, knight_position, 'X')
        add_count_possible_moves(table_for_playing, knight_position)
        draw_table(table_for_playing, False)
        while True:
            knight_position = ask_position(False)
            if check_possible_status(table_for_playing, knight_position):
                count_visited_squares += 1
                update_table(table_for_playing)
            else:
                print('Invalid move!', end=' ')
                continue
            add_position_to_table(table_for_playing, knight_position, 'X')
            count_next_possible_moves = add_count_possible_moves(table_for_playing, knight_position)
            draw_table(table_for_playing, False)
            if count_visited_squares == max_squares:
                print('What a great tour! Congratulations!')
                break
            if count_next_possible_moves == 0:
                print('No more possible moves!')
                print(f'Your knight visited {count_visited_squares} squares!')
                break

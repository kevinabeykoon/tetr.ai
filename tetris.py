"""
tetris_final.py
This Python file implements a Tetris game using Pygame, enhanced with a basic
AI recommendation system. The game features essential mechanics such as block
generation, movement, rotation, and row clearing. An AI module suggests the
best row and rotation for the current block based on a scoring function that
evaluates the number of cleared lines, the presence of holes, and the stack
height. The recommended is highlighted on the bottom-right  corner of the game
board, while the suggested rotation is also displayed in the bottom-right
corner.

Authors: Yifan Qin, Kevin Abeykoon, Joanna Joy, Vivian Ma

The foundation of this project is based on an article from Zhihu, and we
have built upon it with several enhancements. We fixed bugs in the original
implementation and introduced new features such as multi-colored blocks,
background music, AI recommendations, and gesture recognition.
Link: https://zhuanlan.zhihu.com/p/353922161


Notes:
In order to run the program, please ensure that your terminal is navigated
to the correct directory. Additionally, make sure that all necessary files
are present in the folder:

1. tetris_final.py
2. hand_gesture_recognition.py
3. blocks.py
4. command.txt (Blank file)
5. tetris_music.mp3
6. PokemonGb-RAeo.ttf
7. Tetr.ai_Logo.png

Then open terminal:
>>> python3 tetris_final.py (If you want to play game by using keyboard)

Open another terminal and run:
>>> python3 hand_gesture_recognition.py (If you want to play game by using gesture)
"""

import random
import sys
import time

import pygame
from blocks import block_000, block_001, block_002, block_003, block_004, block_005, block_006

SCREEN_WIDTH, SCREEN_HEIGHT = 450, 750
BG_COLOR = (40, 40, 60)
BLOCK_COL_NUM = 10
SIZE = 30
BLOCK_ROW_NUM = 25
BORDER_WIDTH = 4
RED = (200, 30, 30)
COLOR_DICT = {'A': (20, 128, 200), 'B': (134, 20, 200), 'C': (20, 200, 185), 'D': (200, 197, 20), 'E': (200, 20, 23), 'F': (200, 20, 188), 'G': (255, 126, 2)}


def read_command_from_file(file_path='command.txt'):
    """
    read comments from the file
    """
    try:
        with open(file_path, 'r') as file:
            command = file.readline().strip()
        # clean the file
        open(file_path, 'w').close()
        return command
    except FileNotFoundError:
        return None


def judge_game_over(stop_all_block_list):
    """
    check whether the game is over
    """
    if "A" in stop_all_block_list[0] or "B" in stop_all_block_list[0] or "C" in stop_all_block_list[0] or "D" in stop_all_block_list[0] or "E" in stop_all_block_list[0] or "F" in stop_all_block_list[0] or "G" in stop_all_block_list[0]:
        return True


def change_speed(score):
    speed_level = [("1", 0.5, 0, 20), ("2", 0.4, 21, 50), ("3", 0.3, 51, 100), ("4", 0.2, 101, 200),
                   ("5", 0.1, 201, None)]
    for speed_info, speed, score_start, score_stop in speed_level:
        if score_stop and score_start <= score <= score_stop:
            return speed_info, speed
        elif score_stop is None and score >= score_start:
            return speed_info, speed


def judge_lines(stop_all_block_list):
    """
    update the score and clean up the lines
    """
    # record the row number that will be cleaned
    move_row_list = list()

    # clean lines in the game board
    for row, line in enumerate(stop_all_block_list):
        if "." not in line:
            stop_all_block_list[row] = ['.' for _ in range(len(line))]
            move_row_list.append(row)

    if not move_row_list:
        return 0

    for row in move_row_list:
        stop_all_block_list.pop(row)
        stop_all_block_list.insert(0, ['.' for _ in range(len(line))])

    return len(move_row_list) * 10


def add_to_stop_all_block_list(stop_all_block_list, current_block, current_block_start_row, current_block_start_col):
    """
    update the game board
    """
    for row, line in enumerate(current_block):
        for col, block in enumerate(line):
            if block != '.':
                stop_all_block_list[min(current_block_start_row + row, BLOCK_ROW_NUM-1)][min(current_block_start_col + col, BLOCK_COL_NUM-1)] = block


def change_current_block_style(current_block):
    """
    rotate the block
    """
    # find the block list the current block belong to
    current_block_style_list = None
    for block_style_list in [block_000, block_001, block_002, block_003, block_004, block_005, block_006]:
        if current_block in block_style_list:
            current_block_style_list = block_style_list

    # get the index of current block in block list
    index = current_block_style_list.index(current_block)
    # get the next index (after the rotation)
    index += 1
    # avoid out of scope
    index = index % len(current_block_style_list)

    return current_block_style_list[index]


def judge_move_right(current_block, current_block_start_row, current_block_start_col, stop_all_block_list):
    """
    whether the block can move left
    """
    # from right to left
    for col in range(len(current_block[0]) - 1, -1, -1):
        # get the (right, mid, left)  column of current block
        col_list = [line[col] for line in current_block]
        # whether allow to move left
        if ((('A' in col_list) or ('B' in col_list) or ('C' in col_list) or ('D' in col_list) or ('E' in col_list) or ('F' in col_list) or ('G' in col_list)) and (current_block_start_col + col >= BLOCK_COL_NUM)):
            return False
        if (('A' in col_list) or ('B' in col_list) or ('C' in col_list) or ('D' in col_list) or ('E' in col_list) or ('F' in col_list) or ('G' in col_list)):
            indices = [i for i, value in enumerate(col_list) if ((value == 'A') or (value == 'B') or (value == 'C') or (value == 'D') or (value == 'E') or (value == 'F') or (value == 'G'))]
            for j in indices:
                if ((stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'A') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'B') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'C') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'D') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'E') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'F') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'G')):
                    return False

    return True


def judge_move_left(current_block, current_block_start_row, current_block_start_col, stop_all_block_list):
    """
    whether the block can move left
    """
    # from left to right
    for col in range(len(current_block[0])):
        # get the (left, mid, right)  column of current block
        col_list = [line[col] for line in current_block]
        # whether allow to move right
        if ((('A' in col_list) or ('B' in col_list) or ('C' in col_list) or ('D' in col_list) or ('E' in col_list) or ('F' in col_list) or ('G' in col_list)) and (current_block_start_col + col < 0)):
            return False
        if (('A' in col_list) or ('B' in col_list) or ('C' in col_list) or ('D' in col_list) or ('E' in col_list) or ('F' in col_list) or ('G' in col_list)):
            indices = [i for i, value in enumerate(col_list) if  ((value == 'A') or (value == 'B') or (value == 'C') or (value == 'D') or (value == 'E') or (value == 'F') or (value == 'G'))]
            for j in indices:
                if ((stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'A') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'B') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'C') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'D') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'E') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'F') or (stop_all_block_list[min(current_block_start_row+j, BLOCK_ROW_NUM-1)][min(current_block_start_col+col, BLOCK_COL_NUM-1)] == 'G')):
                    return False

    return True


def ai_suggest_best_position(current_block_1, stop_all_block_list, current_block_start_row_1, current_block_start_col_1):
    best_score = float('-inf')
    best_col = 0
    best_rotation = 0
    current_block = current_block_1

    for rotation in range(4):
        current_block_next_style = change_current_block_style(current_block)
        if judge_move_left(current_block_next_style, current_block_start_row_1, current_block_start_col_1, stop_all_block_list) and \
                judge_move_right(current_block_next_style, current_block_start_row_1, current_block_start_col_1, stop_all_block_list) and \
                judge_move_down(current_block, current_block_start_row_1, current_block_start_col_1,
                                stop_all_block_list):
            current_block = current_block_next_style

        move_left_check = False
        move_right_check = False

        for col in range(BLOCK_COL_NUM - len(current_block[0]) + 1):
            current_block_start_row_11 = current_block_start_row_1
            temp_board = [row[:] for row in stop_all_block_list]

            if col == 0 and judge_move_left(current_block, current_block_start_row_1, current_block_start_col_1 - 1,
                               temp_board):
                move_left_check = True

            if col == BLOCK_COL_NUM - len(current_block[0]) and judge_move_right(current_block, current_block_start_row_1, current_block_start_col_1 + 1,
                                stop_all_block_list):
                move_right_check = True

            while judge_move_down(current_block, current_block_start_row_11 + 1, col,
                                  temp_board):
                current_block_start_row_11 += 1

            add_to_stop_all_block_list(temp_board, current_block, current_block_start_row_11, col)

            cleared_lines = judge_lines(temp_board)
            holes = count_holes(temp_board)
            height = get_stack_height(temp_board)

            score = cleared_lines * 20 - holes * 10 - height * 2


            if score > best_score:
                best_score = score
                best_col = col
                best_rotation = rotation


    for i in range(best_rotation+1):
        current_block_1 = change_current_block_style(current_block_1)

    best_col_list = []
    for col in range(len(current_block_1[0])):
        # get the (left, mid, right)  column of current block
        col_list = [line[col] for line in current_block]
        # whether allow to move right
        if 'X' in col_list:
            best_col_list.append(best_col+col)

    return best_col_list, best_rotation+1, current_block_1


def judge_move_down(current_block, current_block_start_row, current_block_start_col, stop_all_block_list):
    """
    whether the block can move down
    """
    # get all the blocks coordinate on game board
    stop_all_block_position = list()
    for row, line in enumerate(stop_all_block_list):
        for col, block in enumerate(line):
            if block != ".":
                stop_all_block_position.append((row, col))

    for row, line in enumerate(current_block):
        if ((('A' in line) or ('B' in line) or ('C' in line) or ('D' in line) or ('E' in line) or ('F' in line) or ('G' in line)) and (current_block_start_row + row >= BLOCK_ROW_NUM)):
            return False

        for col, block in enumerate(line):
            if block != "." and (
                    current_block_start_row + row, current_block_start_col + col) in stop_all_block_position:
                return False
    return True


def get_block():
    """
    generate a new block
    """
    block_style_list = random.choice([block_000, block_001, block_002, block_003, block_004, block_005, block_006])
    return random.choice(block_style_list)


def ai_suggest_best_position(current_block_1, stop_all_block_list, current_block_start_row_1, current_block_start_col_1):
    best_score = float('-inf')
    best_col = 0
    best_rotation = 0
    current_block = current_block_1

    for rotation in range(4):
        current_block_next_style = change_current_block_style(current_block)
        if judge_move_left(current_block_next_style, current_block_start_row_1, current_block_start_col_1, stop_all_block_list) and \
                judge_move_right(current_block_next_style, current_block_start_row_1, current_block_start_col_1, stop_all_block_list) and \
                judge_move_down(current_block, current_block_start_row_1, current_block_start_col_1,
                                stop_all_block_list):
            current_block = current_block_next_style

        move_left_check = False
        move_right_check = False

        for col in range(BLOCK_COL_NUM - len(current_block[0]) + 1):
            current_block_start_row_11 = current_block_start_row_1
            temp_board = [row[:] for row in stop_all_block_list]

            if col == 0 and judge_move_left(current_block, current_block_start_row_1, current_block_start_col_1 - 1,
                               temp_board):
                move_left_check = True

            if col == BLOCK_COL_NUM - len(current_block[0]) and judge_move_right(current_block, current_block_start_row_1, current_block_start_col_1 + 1,
                                stop_all_block_list):
                move_right_check = True

            while judge_move_down(current_block, current_block_start_row_11 + 1, col,
                                  temp_board):
                current_block_start_row_11 += 1

            add_to_stop_all_block_list(temp_board, current_block, current_block_start_row_11, col)

            cleared_lines = judge_lines(temp_board)
            holes = count_holes(temp_board)
            height = get_stack_height(temp_board)

            score = cleared_lines * 20 - holes * 10 - height * 2

            if score > best_score:
                best_score = score
                best_col = col
                best_rotation = rotation

    for i in range(best_rotation+1):
        current_block_1 = change_current_block_style(current_block_1)

    best_col_list = []
    for col in range(len(current_block_1[0])):
        # get the (left, mid, right)  column of current block
        col_list = [line[col] for line in current_block_1]
        # whether allow to move right
        if ('A' in col_list) or ('B' in col_list) or ('C' in col_list) or ('D' in col_list) or ('E' in col_list) or ('F' in col_list) or ('G' in col_list):
            best_col_list.append(best_col+col)

    return best_col_list, best_rotation+1, current_block_1


def count_holes(board):
    holes = 0
    for col in range(len(board[0])):
        block_found = False
        for row in range(len(board)):
            if board[row][col] != '.' and not block_found:
                block_found = True

            elif board[row][col] == '.' and block_found:
                holes += 1

    return holes


def get_stack_height(board):
    terminal_value = False
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != '.':
                terminal_value = True
                current_row = row
                break

        if terminal_value:
            break

    height = BLOCK_ROW_NUM - current_row

    return height


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tretr.ai')

    pygame.mixer.init()
    pygame.mixer.music.load("/Users/yiifann2021/Desktop/python/tetris_music.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0)

    # get the current block
    current_block = get_block()

    # the location of the new block generation
    current_block_start_row = -2  # on the top (unseen)
    current_block_start_col = 0  # mid column

    # next block
    next_block = get_block()
    last_time = time.time()

    # block move speed
    speed = 0.5
    speed_info = '1'

    # define the game board -- BLOCK_COL_NUM * BLOCK_ROW_NUM
    stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]

    # font
    font = pygame.font.Font("/Users/yiifann2021/Desktop/python/PokemonGb-RAeo.ttf", 20)
    font_2 = pygame.font.Font("/Users/yiifann2021/Desktop/python/PokemonGb-RAeo.ttf", 13)
    game_over_font = pygame.font.Font("/Users/yiifann2021/Desktop/python/PokemonGb-RAeo.ttf", 20)
    game_over_font_width, game_over_font_height = game_over_font.size('GAME OVER')
    game_again_font_width, game_again_font_height = font.size('NEW GAME')

    # score
    score = 0

    # check game status
    game_over = False
    paused = False
    ai_check = False

    # build the clock
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    paused = not paused
                    pygame.mixer.music.play(loops=  -1, start= 0.0)

                elif event.key == pygame.K_LEFT:
                    if judge_move_left(current_block, current_block_start_row, current_block_start_col - 1, stop_all_block_list):
                        current_block_start_col -= 1

                elif event.key == pygame.K_RIGHT:
                    if judge_move_right(current_block, current_block_start_row, current_block_start_col + 1, stop_all_block_list):
                        current_block_start_col += 1

                elif event.key == pygame.K_UP:
                    current_block_next_style = change_current_block_style(current_block)
                    if judge_move_left(current_block_next_style, current_block_start_row, current_block_start_col, stop_all_block_list) and \
                            judge_move_right(current_block_next_style, current_block_start_row, current_block_start_col, stop_all_block_list) and \
                            judge_move_down(current_block, current_block_start_row, current_block_start_col,
                                            stop_all_block_list):
                        current_block = current_block_next_style

                elif event.key == pygame.K_DOWN:
                    if judge_move_down(current_block, current_block_start_row + 2, current_block_start_col,
                                       stop_all_block_list):
                        current_block_start_row += 2
                elif event.key == pygame.K_i:
                    best_col_list, best_rotation, best_block = ai_suggest_best_position(current_block,
                                                                                            stop_all_block_list,
                                                                                            4, 4)

                    ai_check = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                if game_over:
                    current_block = get_block()
                    current_block_start_row = -2
                    current_block_start_col = 0
                    next_block = get_block()
                    stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]
                    score = 0
                    game_over = False

        command = read_command_from_file()
        if command == 'left':
            if judge_move_left(current_block, current_block_start_row, current_block_start_col - 1, stop_all_block_list):
                current_block_start_col -= 1
        elif command == 'right':
            if judge_move_right(current_block, current_block_start_row, current_block_start_col + 1, stop_all_block_list):
                current_block_start_col += 1
        elif command == 'down':
            if judge_move_down(current_block, current_block_start_row + 2, current_block_start_col,
                               stop_all_block_list):
                current_block_start_row += 2
        elif command == 'up':
            current_block_next_style = change_current_block_style(current_block)
            if judge_move_left(current_block_next_style, current_block_start_row, current_block_start_col,
                               stop_all_block_list) and \
                    judge_move_right(current_block_next_style, current_block_start_row, current_block_start_col,
                                     stop_all_block_list) and \
                    judge_move_down(current_block, current_block_start_row, current_block_start_col,
                                    stop_all_block_list):
                current_block = current_block_next_style

        elif command == 'openpalm':
            best_col_list, best_rotation, best_block = ai_suggest_best_position(current_block,
                                                                                stop_all_block_list,
                                                                                4, 4)
            ai_check = True

        # whether the block should move down (depends on speed)
        if not paused and not game_over:
            if time.time() - last_time > speed:
                last_time = time.time()
                if judge_move_down(current_block, current_block_start_row + 1, current_block_start_col,
                                   stop_all_block_list):
                    current_block_start_row += 1
                else:
                    # update the game board
                    add_to_stop_all_block_list(stop_all_block_list, current_block, current_block_start_row,
                                               current_block_start_col)
                    # update the score
                    score += judge_lines(stop_all_block_list)
                    # check whether the game is over
                    game_over = judge_game_over(stop_all_block_list)
                    # change the speed
                    speed_info, speed = change_speed(score)
                    # create new block and new next block
                    current_block = next_block
                    next_block = get_block()
                    # reset current block coordinate
                    current_block_start_col = 0
                    current_block_start_row = -2

        # background
        screen.fill(BG_COLOR)

        # separate the game board and the information board
        pygame.draw.line(screen, (100, 40, 200), (SIZE * BLOCK_COL_NUM, 0), (SIZE * BLOCK_COL_NUM, SCREEN_HEIGHT),
                         BORDER_WIDTH)

        # display the current block
        for row, line in enumerate(current_block):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(screen, COLOR_DICT[block], (
                        (current_block_start_col + col) * SIZE, (current_block_start_row + row) * SIZE, SIZE, SIZE), 0)

        # display the previous block
        for row, line in enumerate(stop_all_block_list):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(screen, COLOR_DICT[block], (col * SIZE, row * SIZE, SIZE, SIZE), 0)

        # Display Vertical Grid Lines
        for x in range(BLOCK_COL_NUM):
            pygame.draw.line(screen, (0, 0, 0), (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1)
        # Display horizontal Grid Lines
        for y in range(BLOCK_ROW_NUM):
            pygame.draw.line(screen, (0, 0, 0), (0, y * SIZE), (BLOCK_COL_NUM * SIZE, y * SIZE), 1)

        # Game information
        #logo
        image = pygame.image.load("/Users/yiifann2021/Desktop/python/Tetr.ai_Logo.png").convert()
        scaledImage = pygame.transform.smoothscale(image, (143,80))
        screen.blit(scaledImage, (306, 3))

        # Score
        score_show_msg = font.render('Score: ', True, (150, 130, 200))
        screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 160))
        score_show_msg = font.render(str(score), True, (150, 130, 200))
        screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 200))
        # Speed
        speed_show_msg = font.render('Speed: ', True, (150, 130, 200))
        screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 250))
        speed_show_msg = font.render(speed_info, True, (150, 130, 200))
        screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 290))
        # Next Block
        next_style_msg = font.render('Next', True, (150, 130, 200))
        screen.blit(next_style_msg, (BLOCK_COL_NUM * SIZE + 10, 350))
        next_style_msg = font.render('Block: ', True, (150, 130, 200))
        screen.blit(next_style_msg, (BLOCK_COL_NUM * SIZE + 10, 390))
        # Next Block
        for row, line in enumerate(next_block):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(screen, COLOR_DICT[block],
                                     (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE + 140, SIZE, SIZE), 0)

                    # left
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE + 140),
                                     (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE + 140), 1)

                    # up
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE + 140),
                                     (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE + 140), 1)

                    # down
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE + 140),
                                     (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE + 140), 1)

                    # right
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE + 140),
                                     (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE + 140), 1)

        # AI Hint
        if ai_check:
            hint_show_msg = font_2.render('AI HINT:', True, (150, 130, 200))
            screen.blit(hint_show_msg, (BLOCK_COL_NUM * SIZE + 10, 600))
            hint_show_msg = font_2.render('Turn:', True, (150, 130, 200))
            screen.blit(hint_show_msg, (BLOCK_COL_NUM * SIZE + 10, 630))
            hint_show_msg = font_2.render(str(best_rotation), True, (150, 130, 200))
            screen.blit(hint_show_msg, (BLOCK_COL_NUM * SIZE + 10, 660))

            hint_show_msg = font_2.render('Column:', True, (150, 130, 200))
            screen.blit(hint_show_msg, (BLOCK_COL_NUM * SIZE + 10, 690))
            hint_show_msg = font_2.render(str(best_col_list), True, (150, 130, 200))
            screen.blit(hint_show_msg, (BLOCK_COL_NUM * SIZE + 10, 720))

        # game pause situation
        if paused:
            pygame.mixer.music.pause()
            pause_msg = font.render('PAUSED', True, (255, 255, 0))
            screen.blit(pause_msg, ((SCREEN_WIDTH - pause_msg.get_width()) // 2, SCREEN_HEIGHT // 2))
            resume_msg = font.render('Press P to Resume', True, (255, 255, 0))
            screen.blit(resume_msg, ((SCREEN_WIDTH - resume_msg.get_width()) // 2, SCREEN_HEIGHT // 2 + 40))

        # game over situation
        if game_over:
            pygame.mixer.music.stop()
            game_over_tips = game_over_font.render('GAME OVER', True, RED)
            screen.blit(game_over_tips,
                        ((SCREEN_WIDTH - game_over_font_width) // 2, (SCREEN_HEIGHT - game_over_font_height) // 2))
            # restart the new game
            game_again = font.render('NEW GAME', True, RED)
            screen.blit(game_again, (
                (SCREEN_WIDTH - game_again_font_width) // 2, (SCREEN_HEIGHT - game_again_font_height) // 2 + 80))

        # update the game
        pygame.display.update()
        # FPS
        clock.tick(60)  # 60 times per minute


if __name__ == '__main__':
    main()

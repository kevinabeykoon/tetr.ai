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
    if "X" in stop_all_block_list[0]:
        return True


def change_speed(score):
    speed_level = [("1", 0.5, 0, 20), ("2", 0.4, 21, 50), ("3", 0.3, 51, 100), ("4", 0.2, 101, 200), ("5", 0.1, 201, None)]
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
                stop_all_block_list[current_block_start_row + row][current_block_start_col + col] = "X"


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


def judge_move_right(current_block, current_block_start_col):
    """
    whether the block can move left
    """
    # from right to left
    for col in range(len(current_block[0]) - 1, -1, -1):
        # get the (right, mid, left)  column of current block
        col_list = [line[col] for line in current_block]
        # whether allow to move left
        if 'X' in col_list and current_block_start_col + col >= BLOCK_COL_NUM:
            return False
    return True


def judge_move_left(current_block, current_block_start_col):
    """
    whether the block can move left
    """
    # from left to right
    for col in range(len(current_block[0])):
        # get the (left, mid, right)  column of current block
        col_list = [line[col] for line in current_block]
        # whether allow to move right
        if 'X' in col_list and current_block_start_col + col < 0:
            return False
    return True


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
        if 'X' in line and current_block_start_row + row >= BLOCK_ROW_NUM:
            return False

        for col, block in enumerate(line):
            if block != "." and (current_block_start_row + row, current_block_start_col + col) in stop_all_block_position:
                return False
    return True


def get_block():
    """
    generate a new block
    """
    block_style_list = random.choice([block_000, block_001, block_002, block_003, block_004, block_005, block_006])
    return random.choice(block_style_list)


def ai_suggest_best_position(current_block, stop_all_block_list, current_block_start_row, current_block_start_col):

    best_score = float('-inf')
    best_col = 0
    best_rotation = 0

    for rotation in range(4):
        current_block_next_style = change_current_block_style(current_block)
        if judge_move_left(current_block_next_style, current_block_start_col) and \
                judge_move_right(current_block_next_style, current_block_start_col) and \
                judge_move_down(current_block, current_block_start_row, current_block_start_col, stop_all_block_list):
        current_block = current_block_next_style

        for col in range(BLOCK_COL_NUM - len(current_block[0]) + 1):
            temp_board = simulate_drop(current_block, col, stop_all_block_list)
            score = evaluate_board(temp_board)
            if score > best_score:
                best_score = score
                best_col = col
                best_rotation = rotation

    return best_col, best_rotation

"""
def simulate_drop(block, start_col, stop_all_block_list):

    temp_board = [row[:] for row in stop_all_block_list]

    # 从上往下尝试放置方块
    max_row = BLOCK_ROW_NUM - len(block)  # 方块能放置的最底行
    row_pos = 0  # 初始行位置

    for row in range(max_row + 1):
        # 检查是否碰撞
        if check_collision(block, row, start_col, temp_board):
            row_pos = row - 1  # 上一行是安全的
            break
        else:
            row_pos = row  # 更新当前安全行

    # 将方块“放下去”
    for r_idx, line in enumerate(block):
        for c_idx, cell in enumerate(line):
            if cell != '.':
                temp_board[row_pos + r_idx][start_col + c_idx] = 'O'  # 假设 'O' 表示方块

    return temp_board
    
def check_collision(block, start_row, start_col, board):

    for r_idx, line in enumerate(block):
        for c_idx, cell in enumerate(line):
            if cell != '.':
                row = start_row + r_idx
                col = start_col + c_idx

                # 检查是否越界或撞到方块
                if row >= BLOCK_ROW_NUM or col < 0 or col >= BLOCK_COL_NUM:
                    return True  # 碰到边界
                if board[row][col] != '.':
                    return True  # 碰到静止方块

    return False  # 没有碰撞


def evaluate_board(board):
 
    cleared_lines = count_cleared_lines(board)
    holes = count_holes(board)
    height = get_stack_height(board)

    score = cleared_lines * 100 - holes * 50 - height * 2
    return score


def show_ai_recommendation(screen, block, col, rotation):

    recommended_block = rotate_block_n_times(block, rotation)
    row = simulate_drop_row(recommended_block, col, stop_all_block_list)

    for r_idx, line in enumerate(recommended_block):
        for c_idx, cell in enumerate(line):
            if cell != '.':
                pygame.draw.rect(
                    screen,
                    (0, 255, 0),  # 绿色边框
                    ((col + c_idx) * SIZE, (row + r_idx) * SIZE, SIZE, SIZE),
                    2  # 边框宽度
                )
"""


def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tretr.ai')

    # get the current block
    current_block = get_block()

    # the location of the new block generation
    current_block_start_row = -2  # on the top (unseen)
    current_block_start_col = 4  # mid column

    # next block
    next_block = get_block()
    last_time = time.time()

    # block move speed
    speed = 0.5
    speed_info = '1'

    # define the game board -- BLOCK_COL_NUM * BLOCK_ROW_NUM
    stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]

    # font
    font = pygame.font.SysFont(None, 36)
    game_over_font = pygame.font.SysFont(None, 36)
    game_over_font_width, game_over_font_height = game_over_font.size('GAME OVER')
    game_again_font_width, game_again_font_height = font.size('NEW GAME')

    # score
    score = 0

    # check game status
    game_over = False
    paused = False

    # build the clock
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    paused = not paused

                elif event.key == pygame.K_LEFT:
                    if judge_move_left(current_block, current_block_start_col - 1):
                        current_block_start_col -= 1

                elif event.key == pygame.K_RIGHT:
                    if judge_move_right(current_block, current_block_start_col + 1):
                        current_block_start_col += 1

                elif event.key == pygame.K_UP:
                    current_block_next_style = change_current_block_style(current_block)
                    if judge_move_left(current_block_next_style, current_block_start_col) and \
                            judge_move_right(current_block_next_style, current_block_start_col) and \
                            judge_move_down(current_block, current_block_start_row, current_block_start_col, stop_all_block_list):
                        current_block = current_block_next_style

                elif event.key == pygame.K_DOWN:
                    if judge_move_down(current_block, current_block_start_row + 2, current_block_start_col, stop_all_block_list):
                        current_block_start_row += 2
                """
                elif event.key == pygame.K_i:
                        best_col, best_rotation = ai_suggest_best_position(current_block, stop_all_block_list)
                        show_ai_recommendation(screen, current_block, best_col, best_rotation)
                """

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                if game_over:
                    current_block = get_block()
                    current_block_start_row = -2
                    current_block_start_col = 4
                    next_block = get_block()
                    stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]
                    score = 0
                    game_over = False

        command = read_command_from_file()
        if command == 'left':
            if judge_move_left(current_block, current_block_start_col - 1):
                current_block_start_col -= 1
        elif command == 'right':
            if judge_move_right(current_block, current_block_start_col + 1):
                current_block_start_col += 1
        elif command == 'down':
            if judge_move_down(current_block, current_block_start_row + 2, current_block_start_col,
                               stop_all_block_list):
                current_block_start_row += 2
        elif command == 'up':
            current_block_next_style = change_current_block_style(current_block)
            if judge_move_left(current_block_next_style, current_block_start_col) and \
                    judge_move_right(current_block_next_style, current_block_start_col) and \
                    judge_move_down(current_block, current_block_start_row, current_block_start_col,
                                    stop_all_block_list):
                current_block = current_block_next_style

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
                    current_block_start_col = 4
                    current_block_start_row = -2

        # background
        screen.fill(BG_COLOR)

        # separate the game board and the information board
        pygame.draw.line(screen, (100, 40, 200), (SIZE * BLOCK_COL_NUM, 0), (SIZE * BLOCK_COL_NUM, SCREEN_HEIGHT), BORDER_WIDTH)

        # display the current block
        for row, line in enumerate(current_block):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(screen, (20, 128, 200), ((current_block_start_col + col) * SIZE, (current_block_start_row + row) * SIZE, SIZE, SIZE), 0)

        # display the previous block
        for row, line in enumerate(stop_all_block_list):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(screen, (20, 128, 200), (col * SIZE, row * SIZE, SIZE, SIZE), 0)

        # Display Vertical Grid Lines
        for x in range(BLOCK_COL_NUM):
            pygame.draw.line(screen, (0, 0, 0), (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1)
        # Display horizontal Grid Lines
        for y in range(BLOCK_ROW_NUM):
            pygame.draw.line(screen, (0, 0, 0), (0, y * SIZE), (BLOCK_COL_NUM * SIZE, y * SIZE), 1)

        # Game information
        # Score
        score_show_msg = font.render('Score: ', True, (255, 255, 255))
        screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 10))
        score_show_msg = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 50))
        # Speed
        speed_show_msg = font.render('Speed: ', True, (255, 255, 255))
        screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 100))
        speed_show_msg = font.render(speed_info, True, (255, 255, 255))
        screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 150))
        # Next Block
        next_style_msg = font.render('Next Block: ', True, (255, 255, 255))
        screen.blit(next_style_msg, (BLOCK_COL_NUM * SIZE + 10, 200))
        # Next Block
        for row, line in enumerate(next_block):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(screen, (20, 128, 200), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE, SIZE, SIZE), 0)
                    # left
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE), 1)
                    # up
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE), 1)
                    # down
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1)
                    # right
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1)

        # game pause situation
        if paused:
            pause_msg = font.render('PAUSED', True, (255, 255, 0))
            screen.blit(pause_msg, ((SCREEN_WIDTH - pause_msg.get_width()) // 2, SCREEN_HEIGHT // 2))
            resume_msg = font.render('Press P to Resume', True, (255, 255, 0))
            screen.blit(resume_msg, ((SCREEN_WIDTH - resume_msg.get_width()) // 2, SCREEN_HEIGHT // 2 + 40))

        # game over situation
        if game_over:
            game_over_tips = game_over_font.render('GAME OVER', True, RED)
            screen.blit(game_over_tips, ((SCREEN_WIDTH - game_over_font_width) // 2, (SCREEN_HEIGHT - game_over_font_height) // 2))
            # restart the new game
            game_again = font.render('NEW GAME', True, RED)
            screen.blit(game_again, ((SCREEN_WIDTH - game_again_font_width) // 2, (SCREEN_HEIGHT - game_again_font_height) // 2 + 80))

        # update the game
        pygame.display.update()
        # FPS
        clock.tick(60)  # 60 times per minute


if __name__ == '__main__':
    main()

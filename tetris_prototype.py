
import random
import sys
import time

import pygame

from blocks import block_s, block_i, block_j, block_l, block_o, block_t, block_z

SCREEN_WIDTH, SCREEN_HEIGHT = 450, 750
BG_COLOR = (40, 40, 60)  
BLOCK_COL_NUM = 10  
SIZE = 30  
BLOCK_ROW_NUM = 25   
BORDER_WIDTH = 4   
RED = (200, 30, 30)   


def judge_game_over(stop_all_block_list):
    """
    判断游戏是否结束
    """
    if "O" in stop_all_block_list[0]:
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
    判断是否有同一行的方格，如果有则消除
    """
    # 记录刚刚消除的行数
    move_row_list = list()
    # 消除满格的行
    for row, line in enumerate(stop_all_block_list):
        if "." not in line:
            # 如果这一行没有. 那么就意味着全部是O，则消除这一行
            stop_all_block_list[row] = ['.' for _ in range(len(line))]
            move_row_list.append(row)

    # 如果没有满格的行，则结束此函数
    if not move_row_list:
        return 0

    # 移动剩余的行到下一行
    for row in move_row_list:
        stop_all_block_list.pop(row)
        stop_all_block_list.insert(0, ['.' for _ in range(len(line))])

    return len(move_row_list) * 10


def add_to_stop_all_block_list(stop_all_block_list, current_block, current_block_start_row, current_block_start_col, color):
    """
    将当前已经停止移动的block添加到列表中
    """
    for row, line in enumerate(current_block):
        for col, block in enumerate(line):
            if block != '.':
                stop_all_block_list[current_block_start_row + row][current_block_start_col + col] = color


def change_current_block_style(current_block):
    """
    改变图形的样式
    """
    # 计算出，当前图形样式属于哪个图形
    current_block_style_list = None
    for block_style_list in [block_s, block_i, block_j, block_l, block_o, block_t, block_z]:
        if current_block in block_style_list:
            current_block_style_list = block_style_list

    # 得到当前正在用的图形的索引（下标）
    index = current_block_style_list.index(current_block)
    # 它的下一个图形的索引
    index += 1
    # 防止越界
    index = index % len(current_block_style_list)
    # 返回下一个图形
    return current_block_style_list[index]


def judge_move_right(current_block, current_block_start_col):
    """
    判断是否可以向右移动
    """
    # 先判断列的方式是从右到左
    for col in range(len(current_block[0]) - 1, -1, -1):
        # 得到1列的所有元素
        col_list = [line[col] for line in current_block]
        # 判断是否碰到右边界
        if 'O' in col_list and current_block_start_col + col >= BLOCK_COL_NUM:
            return False
    return True


def judge_move_left(current_block, current_block_start_col):
    """
    判断是否可以向左移动
    """
    # 先判断列的方式是从左到右
    for col in range(len(current_block[0])):
        # 得到1列的所有元素
        col_list = [line[col] for line in current_block]
        # 判断是否碰到右边界
        if 'O' in col_list and current_block_start_col + col < 0:
            return False
    return True


def judge_move_down(current_block, current_block_start_row, current_block_start_col, stop_all_block_list):
    """
    判断是否碰撞到其它图形或者底边界
    """
    # 得到其它图形所有的坐标
    stop_all_block_position = list()
    for row, line in enumerate(stop_all_block_list):
        for col, block in enumerate(line):
            if block != ".":
                stop_all_block_position.append((row, col))
    # print(stop_all_block_position)

    # 判断碰撞
    for row, line in enumerate(current_block):
        if 'O' in line and current_block_start_row + row >= BLOCK_ROW_NUM:
            # 如果当前行有0，且从起始行开始算+当前显示的行，超过了总行数，那么就认为碰到了底部
            return False
        for col, block in enumerate(line):
            if block != "." and (current_block_start_row + row, current_block_start_col + col) in stop_all_block_position:
                return False

    return True


def get_block():
    """
    创建一个图形
    """
    colorList = [(20, 128, 200), (134, 20, 200), (20, 200, 185), (200, 197, 20), (200, 20, 23), (200, 20, 188)]
    color = random.choice(colorList);

    block_style_list = random.choice([block_s, block_i, block_j, block_l, block_o, block_t, block_z])
    return random.choice(block_style_list),color


def main():
    # Initiate pygame
    pygame.init()

    # Create the game screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    current_block,color = get_block()  # 当前图形
    current_block_start_row = -2  # 当前图片从哪一行开始显示图形
    current_block_start_col = 4  # 当前图形从哪一列开始显示
    next_block,color = get_block()  # 下一个图形
    last_time = time.time()
    speed = 0.5  # 降落的速度
    speed_info = '1'  # 显示的速度等级

    # 定义一个列表，用来存储所有的已经停止移动的形状
    stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]

    # 字体
    font = pygame.font.SysFont(None, 36)  # 黑体24
    game_over_font = pygame.font.SysFont(None, 36)
    game_over_font_width, game_over_font_height = game_over_font.size('GAME OVER')
    game_again_font_width, game_again_font_height = font.size('鼠标点击任意位置，再来一局')

    # 得分
    score = 0

    # 标记游戏是否结束
    game_over = False

    # 创建计时器（防止while循环过快，占用太多CPU的问题）
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
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
                        # 判断新的样式没有越界
                        current_block = current_block_next_style
                elif event.key == pygame.K_DOWN:
                    # 判断是否可以向下移动，如果碰到底部或者其它的图形就不能移动了
                    if judge_move_down(current_block, current_block_start_row + 1, current_block_start_col, stop_all_block_list):
                        current_block_start_row += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                if game_over:
                    # 重置游戏用到的变量
                    current_block,color = get_block()  # 当前图形
                    current_block_start_row = -2  # 当前图片从哪一行开始显示图形
                    current_block_start_col = 4  # 当前图形从哪一列开始显示
                    next_block,color = get_block()  # 下一个图形
                    stop_all_block_list = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]
                    score = 0
                    game_over = False

        # 判断是否修改当前图形显示的起始行
        if not game_over and time.time() - last_time > speed:
            last_time = time.time()
            # 判断是否可以向下移动，如果碰到底部或者其它的图形就不能移动了
            if judge_move_down(current_block, current_block_start_row + 1, current_block_start_col, stop_all_block_list):
                current_block_start_row += 1
            else:
                # 将这个图形存储到统一的列表中，这样便于判断是否成为一行
                add_to_stop_all_block_list(stop_all_block_list, current_block, current_block_start_row, current_block_start_col,color)
                # 判断是否有同一行的，如果有就消除，且加上分数
                score += judge_lines(stop_all_block_list)
                # 判断游戏是否结束（如果第一行中间有O那么就表示游戏结束）
                game_over = judge_game_over(stop_all_block_list)
                # 调整速度
                speed_info, speed = change_speed(score)
                # 创建新的图形
                current_block = next_block
                next_block,color = get_block()
                # 重置数据
                current_block_start_col = 4
                current_block_start_row = -2

        # 画背景（填充背景色）
        screen.fill(BG_COLOR)

        # 画游戏区域分隔线
        pygame.draw.line(screen, (100, 40, 200), (SIZE * BLOCK_COL_NUM, 0), (SIZE * BLOCK_COL_NUM, SCREEN_HEIGHT), BORDER_WIDTH)

        # 显示当前图形
        for row, line in enumerate(current_block):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(screen, color, ((current_block_start_col + col) * SIZE, (current_block_start_row + row) * SIZE, SIZE, SIZE), 0)

        # 显示所有停止移动的图形
        for row, line in enumerate(stop_all_block_list):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(screen, color, (col * SIZE, row * SIZE, SIZE, SIZE), 0)

        # 画网格线 竖线
        for x in range(BLOCK_COL_NUM):
            pygame.draw.line(screen, (0, 0, 0), (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1)
        # 画网格线 横线
        for y in range(BLOCK_ROW_NUM):
            pygame.draw.line(screen, (0, 0, 0), (0, y * SIZE), (BLOCK_COL_NUM * SIZE, y * SIZE), 1)

        # 显示右侧（得分、速度、下一行图形）
        # 得分
        score_show_msg = font.render('得分: ', True, (255, 255, 255))
        screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 10))
        score_show_msg = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 50))
        # 速度
        speed_show_msg = font.render('速度: ', True, (255, 255, 255))
        screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 100))
        speed_show_msg = font.render(speed_info, True, (255, 255, 255))
        screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 150))
        # 下一个图形（文字提示）
        next_style_msg = font.render('下一个: ', True, (255, 255, 255))
        screen.blit(next_style_msg, (BLOCK_COL_NUM * SIZE + 10, 200))
        # 下一个图形（图形）
        for row, line in enumerate(next_block):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(screen, color, (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE, SIZE, SIZE), 0)
                    # 显示这个方格的4个边的颜色
                    # 左
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE), 1)
                    # 上
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE), 1)
                    # 下
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1)
                    # 右
                    pygame.draw.line(screen, (0, 0, 0), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1)

        
        # 显示游戏结束画面
        if game_over:
            game_over_tips = game_over_font.render('GAME OVER', True, RED)
            screen.blit(game_over_tips, ((SCREEN_WIDTH - game_over_font_width) // 2, (SCREEN_HEIGHT - game_over_font_height) // 2))
            # 显示"鼠标点击任意位置，再来一局"
            game_again = font.render('鼠标点击任意位置，再来一局', True, RED)
            screen.blit(game_again, ((SCREEN_WIDTH - game_again_font_width) // 2, (SCREEN_HEIGHT - game_again_font_height) // 2 + 80))

        # 刷新显示（此时窗口才会真正的显示）
        pygame.display.update()
        # FPS（每秒钟显示画面的次数）
        clock.tick(60)  # 通过一定的延时，实现1秒钟能够循环60次


if __name__ == '__main__':
    main()

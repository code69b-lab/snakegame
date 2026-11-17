import pygame
import time
import random
import sys

# 게임 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (15, 23, 42)     # 다크 테마 배경 (#0f172a)
BG_PANEL = (30, 41, 59)   # 보더 및 패널
RED = (244, 63, 94)       # 먹이
GREEN = (56, 189, 248)    # 뱀 머리 (스카이블루)
BODY_COLOR = (14, 165, 233)
GRAY = (148, 163, 184)

# 화면 크기
WIDTH = 600
HEIGHT = 600
BLOCK_SIZE = 20

# 디스플레이 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("지렁이 게임 (Snake Game) - Python")

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("malgungothic", 24)
title_font = pygame.font.SysFont("malgungothic", 36)

def display_score(score):
    score_surf = font_style.render(f"점수: {score}", True, WHITE)
    screen.blit(score_surf, [20, 15])

def draw_snake(block_size, snake_list):
    for i, block in enumerate(snake_list):
        if i == len(snake_list) - 1:
            pygame.draw.rect(screen, GREEN, [block[0], block[1], block_size - 2, block_size - 2], border_radius=6)
        else:
            pygame.draw.rect(screen, BODY_COLOR, [block[0], block[1], block_size - 2, block_size - 2], border_radius=4)

def game_loop():
    game_over = False
    game_close = False

    x = WIDTH / 2
    y = HEIGHT / 2

    dx = 0
    dy = 0

    snake_list = []
    length_of_snake = 3

    food_x = round(random.randrange(BLOCK_SIZE, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
    food_y = round(random.randrange(BLOCK_SIZE + 40, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0

    speed = 10

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            over_msg = title_font.render("게임 오버!", True, RED)
            score_msg = font_style.render(f"최종 점수: {(length_of_snake - 3) * 10}", True, WHITE)
            restart_msg = font_style.render("다시 시작: C / 종료: Q", True, GRAY)

            screen.blit(over_msg, [WIDTH / 2 - 80, HEIGHT / 2 - 60])
            screen.blit(score_msg, [WIDTH / 2 - 70, HEIGHT / 2 - 10])
            screen.blit(restart_msg, [WIDTH / 2 - 120, HEIGHT / 2 + 40])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                        return
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and dx == 0:
                    dx = -BLOCK_SIZE
                    dy = 0
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dx == 0:
                    dx = BLOCK_SIZE
                    dy = 0
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and dy == 0:
                    dy = -BLOCK_SIZE
                    dx = 0
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and dy == 0:
                    dy = BLOCK_SIZE
                    dx = 0

        # 벽 충돌 체크
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += dx
        y += dy
        screen.fill(BLACK)

        # 먹이 그리기
        pygame.draw.circle(screen, RED, (int(food_x + BLOCK_SIZE / 2), int(food_y + BLOCK_SIZE / 2)), BLOCK_SIZE // 2 - 1)

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # 자기 몸통 충돌 체크
        for block in snake_list[:-1]:
            if block == snake_head and (dx != 0 or dy != 0):
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        display_score((length_of_snake - 3) * 10)

        pygame.display.update()

        # 먹이 먹었을 때
        if x == food_x and y == food_y:
            food_x = round(random.randrange(BLOCK_SIZE, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
            food_y = round(random.randrange(BLOCK_SIZE + 40, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
            length_of_snake += 1
            if speed < 22:
                speed += 0.5

        clock.tick(speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()

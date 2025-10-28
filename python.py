import sys
import random
import pygame

#!/usr/bin/env python3
# Simple Snake game using pygame
# Save as /home/developerrayhan/Documents/vs_code/code/python.py
# Requires: pygame (pip install pygame)


# Configuration
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (200, 30, 30)
GRAY = (40, 40, 40)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def random_food_position(snake):
    while True:
        pos = (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
        if pos not in snake:
            return pos


def draw_rect(surface, color, pos):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)

    # Initial snake: center, length 3, moving right
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    snake = [(start_x - i, start_y) for i in range(3)]
    direction = RIGHT
    next_direction = RIGHT

    food = random_food_position(snake)
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    if direction != DOWN:
                        next_direction = UP
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    if direction != UP:
                        next_direction = DOWN
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    if direction != RIGHT:
                        next_direction = LEFT
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    if direction != LEFT:
                        next_direction = RIGHT
                elif event.key == pygame.K_r and game_over:
                    # Restart
                    snake = [(start_x - i, start_y) for i in range(3)]
                    direction = RIGHT
                    next_direction = RIGHT
                    food = random_food_position(snake)
                    score = 0
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            direction = next_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

            # Check collision with self
            if new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                    # Speed up slightly every 5 points
                    if score % 5 == 0:
                        # cap FPS to keep playable
                        new_fps = min(30, FPS + score // 5)
                        clock.tick(new_fps)
                else:
                    snake.pop()

        # Draw
        screen.fill(BLACK)

        # Grid lines (optional subtle)
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))

        # Draw food
        draw_rect(screen, RED, food)

        # Draw snake
        if snake:
            draw_rect(screen, DARK_GREEN, snake[0])  # head
            for seg in snake[1:]:
                draw_rect(screen, GREEN, seg)

        # UI
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        if game_over:
            over_surf = font.render("Game Over", True, RED)
            rect = over_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            screen.blit(over_surf, rect)
            info_surf = small_font.render("Press R to restart or ESC to quit", True, WHITE)
            rect2 = info_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 16))
            screen.blit(info_surf, rect2)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
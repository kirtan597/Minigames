import pygame
import random
import time
import sys

if __name__ == "__main__":
    pygame.init()

color = (16, 176, 59)
is_run = True
resolution = (1280, 720)  # WIDESCREEN
icon = pygame.image.load("logo.png")
apple = pygame.image.load("apple.png")
apple = pygame.transform.scale(apple, (40, 40))  # Scale for widescreen
backgruond = pygame.image.load("background.jpg")
backgruond = pygame.transform.scale(backgruond, resolution)  # Scale background

applex = random.randint(0, 1240)
appley = random.randint(0, 680)

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Snake Game - Widescreen")
pygame.display.set_icon(icon)

# Snake variables
snake_pos = [[640, 360]]
snake_direction = [1, 0]  # Moving right
snake_body_color = (255, 255, 255)
apple_color = (255, 0, 0)
grid_size = 20
score = 0
font = pygame.font.Font(None, 40)
game_over = False

def draw_snake():
    for segment in snake_pos:
        pygame.draw.rect(screen, snake_body_color, (segment[0], segment[1], grid_size, grid_size))

def draw_apple():
    screen.blit(apple, (applex, appley))

def draw_score():
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def check_collision():
    head = snake_pos[0]
    if head[0] < 0 or head[0] >= 1280 or head[1] < 0 or head[1] >= 720:
        return True
    for segment in snake_pos[1:]:
        if head == segment:
            return True
    return False

def check_apple_collision():
    head = snake_pos[0]
    if abs(head[0] - applex) < grid_size and abs(head[1] - appley) < grid_size:
        return True
    return False

clock = pygame.time.Clock()

while is_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                is_run = False
            if event.key == pygame.K_UP and snake_direction != [0, 1]:
                snake_direction = [0, -1]
            if event.key == pygame.K_DOWN and snake_direction != [0, -1]:
                snake_direction = [0, 1]
            if event.key == pygame.K_LEFT and snake_direction != [1, 0]:
                snake_direction = [-1, 0]
            if event.key == pygame.K_RIGHT and snake_direction != [-1, 0]:
                snake_direction = [1, 0]

    if not game_over:
        # Move snake
        new_head = [snake_pos[0][0] + snake_direction[0] * grid_size, 
                   snake_pos[0][1] + snake_direction[1] * grid_size]
        snake_pos.insert(0, new_head)

        # Check apple collision
        if check_apple_collision():
            score += 10
            applex = random.randint(0, 1240)
            appley = random.randint(0, 680)
        else:
            snake_pos.pop()

        # Check collision
        if check_collision():
            game_over = True

    screen.fill(color)
    screen.blit(backgruond, (0, 0))
    
    if not game_over:
        draw_snake()
        draw_apple()
        draw_score()
    else:
        game_over_text = font.render(f'GAME OVER! Final Score: {score}', True, (255, 0, 0))
        screen.blit(game_over_text, (400, 360))
        restart_text = font.render('Press ESC to quit', True, (255, 255, 255))
        screen.blit(restart_text, (450, 400))

    pygame.display.update()
    clock.tick(10)  # Smooth gameplay speed

pygame.quit()
sys.exit()

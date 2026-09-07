#importing pygame module
import pygame
import sys
import time
#initialising pygame module
pygame.init()

clock = pygame.time.Clock()
#loading  game sounds
bg_sound = pygame.mixer.Sound("assets/music.mp3")
pygame.mixer.Sound.play(bg_sound)

#initialising game scores
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 48)

def ball_animation():
    global ball_speed_x
    global ball_speed_y
    global opponent_score
    global player_score
    #making ball move [speed controls]
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #making the ball to bounce back
    if (ball.top <= 0 or ball.bottom >= screen_height):
        ball_speed_y *= -1
    if (ball.right >= screen_width or ball.left <= 0):
        
        if ball.left <= 0:
            player_score += 1
        elif ball.right >= screen_width:
            opponent_score += 1
        ball_restart()
    if (ball.colliderect(player) or ball.colliderect(opponent) or player.colliderect(ball) or opponent.colliderect(ball)):
        ball_speed_x *= -1

def player_animation():
    #constrainting player location
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    #constrainting player location
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    ball.center = (screen_width/2, screen_height/2)

#setting up the main window
screen_width = 1280
screen_height = 720  # WIDESCREEN

screen = pygame.display.set_mode((screen_width, screen_height))
##setting caption for pygame window
pygame.display.set_caption("Pong - Widescreen")


#Defining Game elements
ball = pygame.Rect(screen_width/2-15, screen_height/2-15, 30, 30)
player = pygame.Rect(screen_width-30, screen_height/2-70, 15, 140)
opponent = pygame.Rect(15, screen_height/2-70, 15, 140)


#defining ball speed
ball_speed_x = 5  # Reduced for smooth gameplay
ball_speed_y = 5
#DEFINING PLAYER SPEED
player_speed = 0
opponent_speed = 0
#creating game colours
bg_color = pygame.Color("grey12")
light_grey = (200, 200, 200)

#starting game loop
while True:
    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 5  # Reduced speed
            if event.key == pygame.K_UP:
                player_speed -= 5
            if event.key == pygame.K_w:
                opponent_speed += 5
            if event.key == pygame.K_s:
                opponent_speed -= 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 5
            if event.key == pygame.K_UP:
                player_speed += 5
            if event.key == pygame.K_w:
                opponent_speed -= 5
            if event.key == pygame.K_s:
                opponent_speed += 5

    ball_animation()
    #moving player up or down
    player.y += player_speed
    opponent.y += opponent_speed
    
    opponent_animation()
    player_animation()

    #setting up background color
    screen.fill(bg_color)
    #drawing game elements
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))


    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (screen_width - 150, 20))
    
    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (150, 20))

    # Instructions
    instruction_font = pygame.font.Font("freesansbold.ttf", 24)
    instruction_text = instruction_font.render("P1: UP/DOWN | P2: W/S", False, light_grey)
    screen.blit(instruction_text, (screen_width/2 - 150, screen_height - 40))

    #updating the window
    pygame.display.flip()
    clock.tick(60)  # 60 FPS for smooth gameplay
     

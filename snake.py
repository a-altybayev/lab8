import pygame
import time
import random

snake_speed = 15

HEIGHT = 720
WIDTH = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()

pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((HEIGHT, WIDTH))

fps = pygame.time.Clock()

snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

#generate food at a random position
def generate_food_position():
    while True:
        pos = [random.randrange(1, (HEIGHT // 10)) * 10, 
               random.randrange(1, (WIDTH // 10)) * 10]
        if pos not in snake_body:
            return pos

#set initial food position
fruit_position = generate_food_position()
fruit_spawn = True

#set initial direction
direction = 'RIGHT'
change_to = direction

#initialize score and level
score = 0
level = 1

def show_score_level():
    font = pygame.font.SysFont('times new roman', 20)
    score_surface = font.render('Score: ' + str(score) + '  Level: ' + str(level), True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (HEIGHT / 10, 15)
    game_window.blit(score_surface, score_rect)

def game_over():
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render('your Score: ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (HEIGHT / 2, WIDTH / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    #restricting the snake from moving in the opposite direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    #move the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    #body growing
    snake_body.insert(0, list(snake_position))
    if snake_position == fruit_position:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    #generate new food
    if not fruit_spawn:
        fruit_position = generate_food_position()
    fruit_spawn = True

    #level up after every 30 points
    if score // 30 + 1 > level:
        level += 1
        snake_speed += 5
    
    game_window.fill(black)

    #snake body
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    #food
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    #wall collision
    if snake_position[0] < 0 or snake_position[0] > HEIGHT - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > WIDTH - 10:
        game_over()

    #self-collision
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()
    show_score_level()
    pygame.display.update()
    fps.tick(snake_speed)
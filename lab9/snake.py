import pygame
import time
import random

pygame.init()

# Constants
snake_speed = 10
HEIGHT = 800
WIDTH = 600
segment_size = 20  # Размер сегмента змейки
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
colors = {1: pygame.Color(255, 215, 0),  # Gold for weight 1
          2: pygame.Color(255, 140, 0),  # Dark orange for weight 2
          3: red,    # Red for weight 3
          4: pygame.Color(138, 43, 226), # Purple for weight 4
          5: pygame.Color(75, 0, 130)}   # Indigo for weight 5

pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((HEIGHT, WIDTH))
fps = pygame.time.Clock()

snake_position = [100, 50]
snake_body = [[100, 50], [80, 50], [60, 50], [40, 50]]
score = 0
level = 1

#timer
food_lifetime = 6000  #6 seconds

def generate_food():
    """Generates a new food item with random weight and timer."""
    pos = [random.randrange(1, (HEIGHT // segment_size)) * segment_size,
           random.randrange(1, (WIDTH // segment_size)) * segment_size]
    weight = random.randint(1, 5)  # Random weight between 1 and 5
    color = colors[weight]         # Get color based on weight
    spawn_time = pygame.time.get_ticks()  # Record spawn time
    return pos, weight, color, spawn_time

# Generate initial food
fruit_position, fruit_weight, fruit_color, spawn_time = generate_food()
fruit_spawn = True

direction = 'RIGHT'
change_to = direction

def show_score_level():
    font = pygame.font.SysFont('times new roman', 20)
    score_surface = font.render(f'Score: {score}  Level: {level}', True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (HEIGHT / 10, 15)
    game_window.blit(score_surface, score_rect)

def game_over():
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render('Your Score: ' + str(score), True, red)
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
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Restrict the snake from moving in the opposite direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_position[1] -= segment_size
    elif direction == 'DOWN':
        snake_position[1] += segment_size
    elif direction == 'LEFT':
        snake_position[0] -= segment_size
    elif direction == 'RIGHT':
        snake_position[0] += segment_size

    # Grow the snake
    snake_body.insert(0, list(snake_position))

    # Check if snake eats the food
    snake_head_rect = pygame.Rect(snake_position[0], snake_position[1], segment_size, segment_size)
    fruit_rect = pygame.Rect(fruit_position[0], fruit_position[1], segment_size, segment_size)
    if snake_head_rect.colliderect(fruit_rect):
        score += fruit_weight  # Increase score based on food weight
        fruit_spawn = False
    else:
        snake_body.pop()

    # Check if food lifetime expired
    if pygame.time.get_ticks() - spawn_time > food_lifetime:
        fruit_spawn = False  # Set to False to trigger new food generation

    if not fruit_spawn:
        fruit_position, fruit_weight, fruit_color, spawn_time = generate_food()
        fruit_spawn = True

    # Level up and increase speed
    if score // 10 + 1 > level:
        level += 1
        snake_speed += 5


    game_window.fill(black)


    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], segment_size, segment_size))

    pygame.draw.rect(game_window, fruit_color, pygame.Rect(fruit_position[0], fruit_position[1], segment_size, segment_size))

    # Wall collision
    if snake_position[0] < 0 or snake_position[0] >= HEIGHT or snake_position[1] < 0 or snake_position[1] >= WIDTH:
        game_over()

    # Self-collision
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    show_score_level()

    pygame.display.update()
    fps.tick(snake_speed)
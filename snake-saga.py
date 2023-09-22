import pygame
import random

# Initialize the game
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Saga")
border_width = 10
border_color = (200, 200, 200)

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Initialize the high score
high_score = 0

# Load the high score from a file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    
# Save the high score to a file
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Set up the clock
clock = pygame.time.Clock()

# Snake properties
snake_size = 20
snake_speed = 10

# Font for displaying score
font_style = pygame.font.SysFont(None, 50)

def display_score(score):
    score_text = font_style.render("Score: " + str(score), True, white)
    screen.blit(score_text, [10, 10])

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, white, [segment[0], segment[1], snake_size, snake_size])

def game_loop():
    global high_score
    game_over = False
    game_exit = False

    # Snake starting position
    snake_x = screen_width / 2
    snake_y = screen_height / 2

    # Snake movement
    snake_x_change = 0
    snake_y_change = 0

    # Initial snake length
    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(border_width, screen_width - border_width - snake_size) / 10.0) * 10.0
    food_y = round(random.randrange(border_width, screen_height - border_width - snake_size) / 10.0) * 10.0

    while not game_exit:
        while game_over:
            screen.fill(black)
            game_over_text = font_style.render("Game Over! Press Q to Quit or C to Play Again", True, white)
            screen.blit(game_over_text, [screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2 - game_over_text.get_height() / 2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -snake_size
                    snake_y_change = 0
                if event.key == pygame.K_RIGHT:
                    snake_x_change = snake_size
                    snake_y_change = 0
                if event.key == pygame.K_UP:
                    snake_y_change = -snake_size
                    snake_x_change = 0
                if event.key == pygame.K_DOWN:
                    snake_y_change = snake_size
                    snake_x_change = 0

        # Update snake position
        snake_x += snake_x_change
        snake_y += snake_y_change


        # Check for collision with boundaries
        if (
            snake_x >= screen_width - snake_size - border_width or snake_x < border_width or
            snake_y >= screen_height - snake_size - border_width or snake_y < border_width
        ):
            game_over = True

        # Check for collision with self
        snake_head = [snake_x, snake_y]
        if snake_head in snake_list[:-1]:
            game_over = True

        # Check for collision with food
        if (food_x - snake_size <= snake_x <= food_x + snake_size) and (food_y - snake_size <= snake_y <= food_y + snake_size):
            print("Collision detected!")
            print("Snake head position: (", snake_x, ",", snake_y, ")")
            print("Food position: (", food_x, ",", food_y, ")")
            food_x = round(random.randrange(border_width, screen_width - border_width - snake_size) / 10.0) * 10.0
            food_y = round(random.randrange(border_width, screen_height - border_width - snake_size) / 10.0) * 10.0
            snake_length += 1

    # Draw game elements
        screen.fill(black)
        pygame.draw.rect(screen, border_color, (0, 0, screen_width, border_width))  # Top border
        pygame.draw.rect(screen, border_color, (0, 0, border_width, screen_height))  # Left border
        pygame.draw.rect(screen, border_color, (0, screen_height - border_width, screen_width, border_width))  # Bottom border
        pygame.draw.rect(screen, border_color, (screen_width - border_width, 0, border_width, screen_height))  # Right border
        pygame.draw.polygon(screen, red, [
            (food_x + snake_size / 2, food_y),
            (food_x + snake_size, food_y + snake_size / 2),
            (food_x + snake_size / 2, food_y + snake_size),
            (food_x, food_y + snake_size / 2)
        ])

        score_text = font_style.render("Score: " + str(snake_length - 1), True, white)
        screen.blit(score_text, [border_width, border_width])

        high_score_text = font_style.render("High Score: " + str(high_score), True, white)
        screen.blit(high_score_text, [border_width, border_width + 30])

        snake_head = []
        snake_head.append(snake_x)
        snake_head.append(snake_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        draw_snake(snake_list)
        pygame.display.update()

        # Check for collision with self
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True

        if snake_length - 1 > high_score:
            high_score = snake_length - 1
            save_high_score(high_score)

        # Update the game clock
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Load the high score at the start of the game
high_score = load_high_score()

# Start the game loop
game_loop()




    
    


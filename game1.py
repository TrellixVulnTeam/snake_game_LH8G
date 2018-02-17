import pygame
import random

# constants
white = (252, 252, 252)
black = (0, 0, 0)
red = (220, 0, 0)
green = (0, 180, 0)
blue = (0, 0, 220)

speed = 1
block_size = 10
FPS = 30

board_width = 800
board_height = 600


# initialize pygame & window size
pygame.init()
game_display = pygame.display.set_mode((board_width, board_height))
pygame.display.set_caption("Snake")

# global objects
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()


def message_to_screen(message, color):
    screen_text = font.render(message, True, color)
    game_display.blit(screen_text, [board_width/4, board_height/2])


def event_handler(game_exit, pos_change):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pos_change[0] = -speed * block_size
                pos_change[1] = 0
            if event.key == pygame.K_RIGHT:
                pos_change[0] = speed * block_size
                pos_change[1] = 0
            if event.key == pygame.K_UP:
                pos_change[0] = 0
                pos_change[1] = -speed * block_size
            if event.key == pygame.K_DOWN:
                pos_change[0] = 0
                pos_change[1] = speed * block_size
    return game_exit


def snake_draw(snake_body):
    for snake_piece in snake_body:
        game_display.fill(green, [snake_piece[0], snake_piece[1], block_size, block_size])


def random_pos():
    return [round(random.randrange(0, (board_width - block_size) / 10)) * 10,
            round(random.randrange(0, (board_height - block_size)) / 10) * 10]


# main game loop
def game_loop():
    game_exit = False
    game_over = False
    pos_change = [0, 0]
    start_position = [board_width / 2, board_height / 2]  # x, y
    snake_head = start_position
    apple_pos = random_pos()
    snake_body = []
    snake_length = 1

    while not game_exit:
        while game_over:
            game_display.fill(white)
            message_to_screen("Game over (score: ?), press C to play again or Q to quit", red)
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

        game_exit = event_handler(game_exit, pos_change)

        # MAIN LOGIC
        snake_head[0] += pos_change[0]
        snake_head[1] += pos_change[1]

        # check for collisions
        if snake_head[0] >= board_width or snake_head[0] < 0 or snake_head[1] >= board_height or snake_head[1] < 0:
            game_over = True
        for snake_element in snake_body[:-1]:
            if snake_element == snake_head:
                game_over = True

        # eat apple
        if snake_head[0] == apple_pos[0] and snake_head[1] == apple_pos[1]:
            apple_pos = random_pos()
            snake_length += 1

        snake_body.append(snake_head.copy())
        if len(snake_body) > snake_length:
            del snake_body[0]

        # drawing stuff
        game_display.fill(white)  # clean the game board
        game_display.fill(red, [apple_pos[0], apple_pos[1], block_size, block_size])
        snake_draw(snake_body)
        pygame.display.update()  # frame done, render it

        clock.tick(FPS)  # don't change fps for difficulty, change movement speed

    pygame.quit()
    quit()


# Start the game
game_loop()

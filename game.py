"""
Purpose: The purpose of this file is to recreate the game "Snake". Now that I have control of the user inputs,
         I hope to be able to apply a machine learning algorithm, Q - learning, to teach an AI to play this game.

game.py - Main file for the game snake. This is the only required file as long as the user as the 
          pygame module installed.
"""
import pygame
import random
import time
import numpy as np

# CONSTANTS
snake_block = 20
snake_speed = 20
move = snake_block # amount snake moves per frame
SCREEN_X = 800
SCREEN_Y = 600
BLUE = (0, 0, 255)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)
PURPLE = (138, 43, 226)
RED = (255, 0, 0)

# Initialize pygame
pygame.init() # REQUIRED

class Snake:

    def __init__(self):
        self.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
        self.y = round(random.randrange(0, SCREEN_Y - snake_block) / 20) * 20
        self.x_change = 0
        self.y_change = 0

    # Create Snake
    def create(self, snake_all):
        for rect in snake_all:
            pygame.draw.rect(screen, ORANGE, (rect[0], rect[1], snake_block, snake_block))


    # Actions = [Left, Right, Up, Down] w/ one-hot encoding
    def move(self, action):

        if np.array_equal(action,[1, 0, 0, 0]):
            self.x_change = -move
            self.y_change = 0
        elif np.array_equal(action,[0, 1, 0, 0]):
            self.x_change = move
            self.y_change = 0
        elif np.array_equal(action,[0, 0, 1, 0]):
            self.x_change = 0
            self.y_change = -move
        elif np.array_equal(action,[1, 0, 1, 0]):
            self.x_change = 0
            self.y_change = move

class Food:

    def __init__(self):
        self.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
        self.y = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20

    def create(self):
        pygame.draw.rect(screen, PURPLE, (self.x, self.y, snake_block, snake_block))

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
clock = pygame.time.Clock()

# Initializations
pygame.display.set_caption("Snake")
font_style = pygame.font.SysFont(None, 40)
score_font = pygame.font.SysFont("comicsansms", 35)


def points(score, x, y):
    value = score_font.render("Your Score: " + str(score), True, RED)
    screen.blit(value, [x, y])


# Create food



# Display messages
def message(msg,color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [snake_block*3, SCREEN_Y/2 - 20])


# Game Loop
def main():
    running = True
    game_close = False

    snake = Snake()
    food = Food()

    score = 0
    
    snake_list = []
    snake_length = 1

    snake.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
    snake.y = round(random.randrange(0, SCREEN_Y - snake_block) / 20) * 20
    food.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
    food.y = round(random.randrange(0, SCREEN_Y - snake_block) / 20) * 20

    while running:

        screen.fill(BLACK)

        action = [0,0,1,0]

        snake.move(action)

        snake.x += snake.x_change
        snake.y += snake.y_change
        
        snake_head = []
        snake_head.append(snake.x)
        snake_head.append(snake.y)
        snake_list.append(snake_head)
        
        if snake.x > SCREEN_X - snake_block:
            snake.x = SCREEN_X - snake_block
            game_close = True
        elif snake.x < 0:
            snake.x = 0
            game_close = True
        if snake.y > SCREEN_Y - snake_block:
            snake.y = SCREEN_Y - snake_block
            game_close = True
        elif snake.y < 0:
            snake.y = 0
            game_close = True

        # Protecting edge case of 1 element
        if len(snake_list) > snake_length:
            del snake_list[0]

        # If you hit the snake - [:-1] grabs the end of the list  
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        snake.create(snake_list)
        food.create()
        points(snake_length - 1, 0, 0)
        

        while game_close:
            screen.fill(WHITE)
            message("You Lost! Press Spacebar to play again or Q to Quit", RED)
            points(snake_length - 1, snake_block*3, SCREEN_Y/2 + 30)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    if event.key == pygame.K_q:
                        game_close = False
                        running = False
                    if event.key == pygame.K_SPACE:
                        main()
        
        pygame.display.update() # REQUIRED

        # When food is ate
        if snake.x == food.x and snake.y == food.y:
            snake_length += 1
            food.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
            food.y = round(random.randrange(0, SCREEN_Y - snake_block) / 20) * 20
            

        clock.tick(snake_speed)

    pygame.quit()
    quit()

main()

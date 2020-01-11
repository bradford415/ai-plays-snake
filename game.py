"""
game.py - Main file for the game snake. This is the only required file as long as the user as the 
          pygame module installed.
"""
import pygame
import random
import time
import math
import numpy as np
from keras.utils import to_categorical
from random import randint
from DQN import DQNAgent

# CONSTANTS
snake_block = 20
snake_speed = 50
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

pygame.init() 

class Snake:

    def __init__(self):
        self.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
        self.y = round(random.randrange(0, SCREEN_Y - snake_block) / 20) * 20
        self.x_change = 0
        self.y_change = 0
        self.game_over = 0
        self.length = 1
        self.old_dist_food = 0

    # Create Snake
    def create(self, snake_all):
        for rect in snake_all:
            pygame.draw.rect(screen, ORANGE, (rect[0], rect[1], snake_block, snake_block))


    # Actions = [Left, Right, Up, Down] w/ one-hot encoding
    def move(self, snake, food, action, agent):

        if agent.eaten:
            agent.eaten = 0

        if np.array_equal(action,[1, 0, 0, 0]):
            self.x_change = -move
            self.y_change = 0
        elif np.array_equal(action,[0, 1, 0, 0]):
            self.x_change = move
            self.y_change = 0
        elif np.array_equal(action,[0, 0, 1, 0]):
            self.x_change = 0
            self.y_change = -move
        elif np.array_equal(action,[0, 0, 0, 1]):
            self.x_change = 0
            self.y_change = move

        # When food is ate
        if snake.x == food.x and snake.y == food.y:
            snake.length += 1
            food.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
            food.y = round(random.randrange(0, SCREEN_Y - snake_block) / 20) * 20
            agent.eaten = 1

        # Crash scenario
        if snake.x > SCREEN_X - snake_block:
            snake.x = SCREEN_X - snake_block
            game_close = True
            agent.game_over = True
        elif snake.x < 0:
            snake.x = 0
            game_close = True
            agent.game_over = True
        if snake.y > SCREEN_Y - snake_block:
            snake.y = SCREEN_Y - snake_block
            game_close = True
            agent.game_over = True
        elif snake.y < 0:
            snake.y = 0
            game_close = True
            agent.game_over = True


class Food:

    def __init__(self):
        self.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
        self.y = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20

    def create(self):
        pygame.draw.rect(screen, PURPLE, (self.x, self.y, snake_block, snake_block))

class Game:

    def stats(self, score, x, y, title=""):
        value = score_font.render(str(title) + ": " + str(score), True, RED)
        screen.blit(value, [x, y])

    # Display messages
    def message(self, msg,color):
        mesg = font_style.render(msg, True, color)
        screen.blit(mesg, [snake_block*3, SCREEN_Y/2 - 20])

def initialize_game(snake, food, agent, snake_list):
    current_state = agent.get_state(snake, food, agent, snake_list)
    action = [0,0,1,0] # Random initial action
    snake.old_dist_food = math.sqrt(((food.x - snake.x)**2) + ((food.y - snake.y)**2))
    snake.move(snake, food, action, agent)
    next_state = agent.get_state(snake,food, agent, snake_list)
    reward = 0
    agent.update_memory(current_state, action, reward, next_state, agent.game_over)
    agent.replay_memory()
    

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
clock = pygame.time.Clock()

# Initializations
pygame.display.set_caption("Snake")
font_style = pygame.font.SysFont(None, 40)
score_font = pygame.font.SysFont("comicsansms", 35)

# Game Loop
def main():
    running = True

    agent = DQNAgent()
    game = Game()

    crash = 0
    score = 0
    num_games = 0
    

    while num_games < 2000:

        snake_list = []
        snake = Snake()

        food = Food()

        # First move
        initialize_game(snake, food, agent, snake_list)
        agent.game_over = 0

        agent.epsilon = 30 - num_games

        snake.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
        snake.y = round(random.randrange(0, SCREEN_Y - snake_block) / 20) * 20
        food.x = round(random.randrange(0, SCREEN_X - snake_block) / 20) * 20
        food.y = round(random.randrange(0, SCREEN_Y - snake_block) / 20) * 20


        while not agent.game_over:

            screen.fill(BLACK)
            print("")

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Close the window
                    pygame.quit()    
                    quit()

            if agent.eaten:
                agent.eaten = 0
            if agent.game_over:
                agent.game_over = 0

            current_state = agent.get_state(snake, food, agent, snake_list)

            # As the game progresses, the chacnes that a random action will be chosen decreases.
            # to_categorical converts to a one hot encoding, reshaping is because it requires a 
            # vector and not a tensor
            print("Epsilon: " + str(agent.epsilon))
            if randint(0,100) < agent.epsilon:
                action = to_categorical(randint(0,3), num_classes=4)
                print("Random")
            else:
                prediction = agent.model.predict(np.array(current_state.reshape(1,agent.state_size)))
                action = to_categorical(np.argmax(prediction[0]), num_classes=4)
                print("Calculated")

            snake.old_dist_food = math.sqrt(((food.x - snake.x)**2) + ((food.y - snake.y)**2))

            snake.move(snake, food, action, agent)

            snake.x += snake.x_change
            snake.y += snake.y_change
            
            snake_head = []
            snake_head.append(snake.x)
            snake_head.append(snake.y)
            snake_list.append(snake_head)

            next_state = agent.get_state(snake, food, agent, snake_list)
            reward = agent.reward(snake, food)
            # Protecting edge case of 1 element
            if len(snake_list) > snake.length:
                del snake_list[0]

            # If you hit the snake - [:-1] grabs the end of the list  
            for x in snake_list[:-1]:
                if x == snake_head:
                    agent.game_over = True
                    reward = -50
                    print("New Reward: " + str(reward))
                    
            agent.short_memory(current_state, action, reward, next_state, agent.game_over)
            agent.update_memory(current_state, action, reward, next_state, agent.game_over)
    
            

            snake.create(snake_list)
            food.create()
            game.stats(snake.length - 1, 0, 0, title="Score")
            game.stats(num_games, 600, 0, title="Game")
            
            pygame.display.update()

            clock.tick(snake_speed)
            pygame.time.wait(100)


        # Game over scenario
        agent.replay_memory()
        num_games += 1

        screen.fill(WHITE)
        game.message("You Lost! The game will restart automatically", RED)
        game.stats(snake.length - 1, snake_block*3, SCREEN_Y/2 + 30, "Final Score")
        pygame.display.update()
        pygame.time.wait(300)


    pygame.quit()
    quit()

main()

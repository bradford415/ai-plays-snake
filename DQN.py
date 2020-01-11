"""
States - Specific scenarios encountered in the game 
[head above food,head below food, head right of food ,head left of food]
    - Currently using these basic 4 states to get started, will most likely need 
      to update later

Actions - Action to take based of the scenarios - One-hot Encoding
[Left, Right, Up, Down]

Rewards - rewarding the network for doing good or bad - the +/- 5 are arbitrary values
 + 30 for food eating
 - 10 for game over
 + 1  for getting closer to the food
 - 1  for moving away from the food

Deep Q-Learning does NOT use a Q-table

"""
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
import random
import math
import numpy as np
import pandas as pd

REPLAY_MEM_SIZE = 1000

class DQNAgent:

    def __init__(self):
        #self.short_memory = np.array([]) # used for LSTM
        self.memory = [] # long term memory
        self.learning_rate = 0.0005
        self.gamma = 0.9 # discount factor/decay rate from Q() equations
        self.state_size = 9
        self.action_size = 4
        self.epsilon = 0 # For greedy-epsilon method
        self.model = self.create_network()
        self.game_over = 0 # flag if the snake crashes
        self.eaten = 0


    # Assign different scenarios that the snake may be in
    # This will need to be updated later, 4 does not seem to be enough
    def get_state(self, snake, food, agent, snake_list):

        state = [ 
            snake.x >= 800-20, # Right wall
            snake.x <= 0, # Left wall
            snake.y >= 600 - 20, # Bottom wall 
            snake.y <= 0, # Top wall
            snake.x < food.x, # Snake is left of food          
            snake.x > food.x, # Snake is right of food
            snake.y < food.y, # Snake is above food
            snake.y > food.y,  # Snake is below food
            snake.length > 2
            ]

        # Initialize to 1's or 0's
        for i in range(len(state)):
            if state[i]:
                state[i] = 1
            else:
                state[i] = 0

        print(state)
        
        return np.asarray(state)


    def reward(self, snake, food):

        new_dist_food = math.sqrt(((food.x - snake.x)**2) + ((food.y - snake.y)**2))

        reward = -1
        if self.game_over:
            reward = -10
            print("Reward: " + str(reward))
            return reward
        if self.eaten:
            reward = 30
            print("Reward: " + str(reward))
            return reward
        
        if snake.old_dist_food > new_dist_food and snake:
            reward = 1
            print("Reward: " + str(reward))
            return reward

        print("Reward: " + str(reward))
        return reward
        
    
    '''
    Creates basic neural network with 2 hidden dense layers. Dense layers linearly connect each 
    output of the previous layer to the input of the new layer. Currently, this architecture has
    3 layers, input not counted, the input layer => the states, two hidden layers, 
    and an output layer => the actions.
    
    Modifications:
        1) Need a deeper understanding of "dropout" which may imprpove the network
        2) May need more or less hidden layers, but as of now two seems sufficient
        3) Not exactly sure how to determine the dimensions of the hidden layer
        4) Once the network trains, the weights can be saved and preloaded through
           a keras function if desired
    '''
    def create_network(self):
        # Input_dim only needs to be specified on the first layer
        # Softmax normalizes the outputs to look like a probablity distribution
        model = Sequential()    
        model.add(Dense(output_dim=120, activation="relu", input_dim=self.state_size))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation="relu"))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation="relu"))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=self.action_size, activation="softmax"))
        model.compile(metrics=["accuracy"], loss="mse", optimizer=Adam(self.learning_rate))
        model.summary()

        return model


    # Save experience of the model for each time-step
    def update_memory(self, state, action, reward, next_state, crash):
        self.memory.append((state, action, reward, next_state, crash))

    # Keep track of current state, action, reward, and next state for each frame/time-stamp
    def replay_memory(self):
        
        # Choosing a random sample from replay memory to provide the network with an 
        # uncorrelated approach. This allows the network to learn different environments
        # rather than just learning a sequential approach.
        # Use all memory experiences up until REPLAY_MEM_SIZE, then start grabbing random 1000 samples
        if len(self.memory) > REPLAY_MEM_SIZE:
            minibatch = random.sample(self.memory, REPLAY_MEM_SIZE)
        else:
            minibatch = self.memory

        for state, action, reward, next_state, game_over in minibatch:
            if not game_over:
                # Calculate the learned value - Last part of the Q() equation
                new_q = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            else:
                new_q = reward # If the game is over there is no next state

            # Grab current q value based off the current state and update the current 
            # q value to the new q value based off the action taken. Then retrain the 
            # network off the current state and the new q values
            current_q = self.model.predict(np.array([state]))
            current_q[0][np.argmax(action)] = new_q 
            self.model.fit(np.array([state]), current_q, epochs=1, verbose=0)

    
    def short_memory(self, state, action, reward, next_state, game_over):
        if not game_over:
            # Calculate the learned value - Last part of the Q() equation
            new_q = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1,self.state_size)))[0])
        else:
            new_q = reward # If the game is over there is no next state

        # Grab current q value based off the current state and update the current 
        # q value to the new q value based off the action taken. Then retrain the 
        # network off the current state and the new q values
        current_q = self.model.predict(state.reshape((1,self.state_size)))
        current_q[0][np.argmax(action)] = new_q 
        self.model.fit(state.reshape((1,self.state_size)), current_q, epochs=1, verbose=0)

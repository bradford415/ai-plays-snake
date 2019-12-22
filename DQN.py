"""

States - Specific scenarios encountered in the game 
[head above food,head below food, head right of food ,head left of food]
    - Currently using these basic 4 states to get started, will most likely need 
      to update later

Actions - Action to take based of the scenarios - One-hot Encoding
[Left, Right, Up, Down]

Rewards - rewarding the network for doing good or bad - the +/- 5 are arbitrary values
 + 5 for food eating
 - 5 for game over

"""

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizer import Adam
import numpy as np

np.arra

class DQNAgent:

    def __init__(self):
        self.model = 
        self.memory = 
        self.learning_rate =


    def get_state(self):

        [ 


        ]

    def reward(self):
        
    
    # Keep track of current state, action, reward, and next state for each frame/time-stamp
    def replay_memory(self, state, action, reward, next_state):


    
    

        




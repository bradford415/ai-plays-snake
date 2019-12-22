"""

States - Specific scenarios encountered in the game - X-axis of Q-table
[head above food,head below food, head right of food ,head left of food]
    - Currently using these basic 4 states to get started, will most likely need 
      to update later

Actions - Action to take based of the scenarios - Y-axis of Q-table
[Left, Right, Up, Down]

Q-Table - Defined by the States and Actions to hold the Q-values = (x,y)

Rewards - rewarding the network for doing good or bad - the +/- 5 are arbitrary values
 + 5 for food eating
 - 5 for game over


"""


from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizer import Adam
import numpy as np


class DQNAgent:

    def __init__(self):
        self.model = 
        self.memory = 
        self.learning_rate =


    def get_state():


    def reward():

    
    

        




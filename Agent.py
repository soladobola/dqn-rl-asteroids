import numpy as np
import random

from collections import deque
from Game import Game
from tf_model import QNet, QTrainer
from plot_util import plot
import tensorflow as tf
import time

# only for testing
import keyboard

MAX_MEMORY = 100_000
BATCH_SIZE = 2000
NUM_ACTIONS = 6
LR = 0.00025

#ACTIONS
ACT_LEFT  = [1, 0, 0, 0, 0, 0]
ACT_RIGHT = [0, 1, 0, 0, 0, 0]
ACT_UP    = [0, 0, 1, 0, 0, 0]
ACT_SHOOT = [0, 0, 0, 1, 0, 0]
ACT_LEFT_SHOOT = [0, 0, 0, 0, 1, 0]
ACT_RIGHT_SHOOT = [0, 0, 0, 0, 0, 1]

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.95 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # circular
        self.actions = [ACT_LEFT, ACT_RIGHT, ACT_UP, ACT_SHOOT, ACT_LEFT_SHOOT, ACT_RIGHT_SHOOT]
        self.model = QNet((84, 84, 4), NUM_ACTIONS, True)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
         
    def get_init_state(self, game):
        return game.play_step(None)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            batch = random.sample(self.memory, BATCH_SIZE)
        else:
            batch = self.memory
        
        states, actions, rewards, next_states, dones = zip(*batch)
        
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    
    def get_action(self, state, training=True):
        
        if training:
            self.epsilon = 100 - self.n_games
            if random.randint(0, 300) < self.epsilon:
                move = random.randint(0, NUM_ACTIONS - 1)
                return self.actions[move]
        
        #state_t = tf.convert_to_tensor(state)
        state_t = tf.expand_dims(state, 0)
        prediction = self.model.predict(state_t)
        return self.actions[np.argmax(prediction)]


def play():
    agent = Agent()
    game = Game()
    
    old_state = None
    step = 0
    
    while(True):
        if step == 0:
            old_state = agent.get_init_state(game)[0]
            
        action = agent.get_action(old_state, False)  
        next_state, reward, done, score = game.play_step(action)
        old_state = next_state
        
        if done:
            game.reset()
            step = 0


def train(): 
    
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    best_score =  0# temp best
    agent = Agent()
    game = Game()
    step = 0
    old_state = None
    
    while True:
        
        if step == 0:
            old_state = agent.get_init_state(game)[0]
        
        action = agent.get_action(old_state)
    
        next_state, reward, done, score = game.play_step(action)
        
        agent.remember(old_state, action, reward, next_state, done)
        
        # move to next state
        old_state = next_state
        
        if done:
            # train long memory, plot result 
            game.reset()
            agent.n_games += 1
            
            if agent.n_games % 5 == 0:
                agent.train_long_memory()
            
            if score > best_score:
                best_score = score
                #Model is done
                agent.model.save('generic')
            print('Episode num: ' + str(agent.n_games))
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
    
        step += 1
            

if __name__ == "__main__":
    
    #train()
    play()
    
    
        
    
    
    
    
    
    
    
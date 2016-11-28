#! /usr/bin/env python

import random
from gridWorld import init

START_LOCATION = [0,9]

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

ALPHA = 0.01
BETA = 0.9

EPSILON = 1 #Numerator over 10

CONVERGE_LIMIT = 1000 #Number of unchanged tries

unchanged_tries = 0

class Agent:
    def initialize(self):
        self.current_location = START_LOCATION
        self.is_converged = False

    def __init__(self):
        self.current_location = START_LOCATION
        self.previous_location = None


def arg_max(l):
    m = max(l)
    while(True):
        i = random.randrange(4)
        if l[i] == m:
            return i


def choose_action(current_location, gridWorld):
    #Given a state, chooses finds the optimal action for exploitation, and depending on the epsilon value, either returns a random number between 0 and 4
    state = gridWorld[current_location[0]][current_location[1]]
    q_values = state[0]
    exploit_action = arg_max(q_values)

    #Find the probability
    rand_var = random.randrange(0,10)
    if (rand_var < EPSILON):
        #EXPLOIT
        return random.randrange(0,4)

    return exploit_action

def update_agent_location(agent, action, gridWorld):
    #Find the agent's current location, use the action to check what the next location is.
    wall = False
    old_location = agent.current_location
    #If agent is at goal state, then update location to start state no matter what the action
    if (gridWorld[old_location[0]][old_location[1]][1] == 1):
        agent.previous_location = agent.current_location
        agent.current_location = START_LOCATION
        return
    new_location = old_location[:]
    if action == UP:
        new_location[1] += 1
    if action == DOWN:
        new_location[1] -= 1
    if action == LEFT:
        new_location[0] -= 1
    if action == RIGHT:
        new_location[0] += 1
    if (new_location[0] < 0 or new_location[0] > 9 or new_location[1] < 0 or new_location[1] > 9):
        wall = True
    if (wall == False and gridWorld[new_location[0]][new_location[1]] == 0):
        wall = True

    if wall == True:
        print "WALL"
        agent.current_location = old_location
        agent.previous_location = old_location
        return
    
    #if (gridWorld[new_location[0]][new_location[1]][1] == 1):
        #Goal state
    #    agent.current_location = START_LOCATION
    #    agent.previous_location = new_location

    agent.current_location = new_location
    agent.previous_location = old_location


def update_q_value(agent, action, gridWorld):
    global unchanged_tries
    current_location = agent.current_location
    previous_location = agent.previous_location
    print current_location, previous_location
    cur_x, cur_y = current_location[0], current_location[1]
    pre_x, pre_y = previous_location[0], previous_location[1]
    new_q = gridWorld[cur_x][cur_y][0]
    q_values = gridWorld[pre_x][pre_y][0][:]
    reward = gridWorld[pre_x][pre_y][1]
    q_values[action] += ALPHA * (reward + (BETA * max(new_q)) - q_values[action])
    if gridWorld[pre_x][pre_y][0] != q_values[:]:
        unchanged_tries = 0
    else: unchanged_tries += 1
    gridWorld[pre_x][pre_y][0] = q_values[:]


def print_optimal_policy(gridWorld):
    agent = Agent()

def main():
    global unchanged_tries
    #Repeat until convergence:
    #pick an action
    #Execute the action and get the resulting location from the world
    #Based on the new location, update the Q values of the previous location
    #If new location is goal state, reset back to START_LOCATION
    agent = Agent()
    gridWorld = init()
    is_converged = False
    while (unchanged_tries < CONVERGE_LIMIT):
        action = choose_action(agent.current_location, gridWorld)
        print action
        update_agent_location(agent, action, gridWorld)
        update_result = update_q_value(agent, action, gridWorld)

    print gridWorld

if __name__ == "__main__":
    main()

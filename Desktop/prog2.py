import random
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from prog1 import *

# initial states is structured as follows: [value of state taking only action 0 [Q(s,0)], value of
# state taking only action 1, number of times state visited and taken action 0, number of times
# state visited and taken action 1
# [V(s,0), V(s,1), N(s,0), N(s,1)]						
						
def monte_carlo(initial_states):
	state = State();
	state.dealercard = random.randint(1,10)
	state.playersum = random.randint(1,21)
	
	phase = 0
	initial_index = index = (state.dealercard - 1) + (state.playersum - 1) * 10
	total_return = 0
	N_0 = 100.0
		
	while(state != "terminal"):
			
		# calculating index of current state on iteration
		index = (state.dealercard - 1) + (state.playersum - 1) * 10 # creates an index from 0 to 209 for initial_states access
		N_S = initial_states[index][2] + initial_states[index][3] # calculates total number of times this state has been visited (for the first time)
	
		# calculation of e-greedy exploration strategy
		epsilon = N_0 / (N_0 + N_S)
		
		# exploration phase
		if(random.random() < epsilon):
			action = random.randint(0,1)
			
		# exploitation phase (chose action which has higher proven value function)
		else:
			if(initial_states[index][0] > initial_states[index][1]):
				action = 0
			else:
				action = 1
		
		if(phase == 0):
			initial_action = action
			phase = 1
		# actual iteration of step function	
		initial_states[index][action + 2] = initial_states[index][action + 2] + 1	
		state, reward = step(state, action)
		
		total_return = total_return + reward
	
	alpha = 1.0/initial_states[initial_index][initial_action + 2] # deciding alpha based on the action taken
	
	# updating value function (initial_states[initial_index][action] is the value function of state s having chosen action a)
	old_value = initial_states[initial_index][action]
	new_value = old_value + alpha * (total_return - old_value)
	
	initial_states[initial_index][action] = new_value
	
	return initial_states
	
#########################################################################################

initial_states = [[0 for i in range(2)] for j in range(210)]
'''
random.random()/1000
'''
for counter in range(0,210):
	initial_states[counter].append(0)
	initial_states[counter].append(0)
	
for i in range(1,100000):
	initial_states = monte_carlo(initial_states)

# plotting

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(1,11):
	for j in range(1,22):
		index = (i - 1) + (j - 1) * 10
		xs = i
		ys = j
		zs = max(initial_states[index][0], initial_states[index][1])
		ax.scatter(xs, ys, zs)

ax.set_xlabel('Dealer Sum')
ax.set_ylabel('Player Sum')
ax.set_zlabel('Value of State')

plt.show()


	
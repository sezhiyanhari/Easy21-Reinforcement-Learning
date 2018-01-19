import random
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from prog1 import *
from prog2 import *

# same state structure as in prog2.py
initial_states = np.zeros((210,4))
copy_states = initial_states
monte_states = copy_states

def sarsa(lambda_value):
	
	initial_states = copy_states	
	episode = 0
	N_0 = 100.0
	state = State();
	state_prime = State();
		
	while(episode != 100000):
		
		episode = episode + 1	
			
		eligibility = np.zeros((210,2))
		state.dealercard = random.randint(1,10)
		state.playersum = random.randint(1,21)
		initial_index = index = (state.dealercard - 1) + (state.playersum - 1) * 10
		N_S = initial_states[initial_index][2] + initial_states[initial_index][3] # calculates total number of times this state has been visited (for the first time)
		epsilon = 1/episode
	
		# exploration phase
		if(random.random() < epsilon):
			action = random.randint(0,1)
			
		# exploitation phase (chose action which has higher proven value function)
		else:
			if(initial_states[index][0] > initial_states[index][1]):
				action = 0
			else:
				action = 1

		while(state != "terminal"):
			
			index = (state.dealercard - 1) + (state.playersum - 1) * 10
			initial_states[index][action + 2] += 1
			state_prime, reward = step(state, action)
			alpha = 1.0 / initial_states[index][action + 2]
			eligibility[index][action] += 1.0

			if(state_prime == "terminal"):
				error = reward + 0.0 - initial_states[index][action]
				initial_states[:,0:2] += alpha * error * eligibility
				eligibility *= lambda_value
				break

			index_prime = (state_prime.dealercard - 1) + (state_prime.playersum - 1) * 10

			epsilon = 1.0 / episode
	
			if(random.random() < epsilon):
				action_prime = random.randint(0,1)
			else:
				if(initial_states[index_prime][0] > initial_states[index_prime][1]):
					action_prime = 0
				else:
					action_prime = 1
	   
			error = reward + initial_states[index_prime][action_prime] - initial_states[index][action]
			initial_states[:,0:2] += alpha * error * eligibility
			eligibility *= lambda_value		 
			
			state = state_prime
			action = action_prime
				
def calc_mean_squared_error(lambda_value):
	sarsa(lambda_value)
	for iter in range(1, 500000):
		monte_states = monte_carlo(copy_states)
	mean_error = np.sum(np.power(monte_states[:,0:2] - initial_states[:,0:2], 2.0))
	
	return(mean_error)

sarsa(0.9)
print("About to print Sarsa plot ...")


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(1,11):
	for j in range(1,22):
		index = (i - 1) + (j - 1) * 10
		xs = i
		ys = j
		zs = max(initial_states[index][0], initial_states[index][1])
		ax.scatter(xs, ys, zs)
print("Finished initial states")

ax.set_xlabel('Dealer Sum')
ax.set_ylabel('Player Sum')
ax.set_zlabel('Value of State')

plt.show()




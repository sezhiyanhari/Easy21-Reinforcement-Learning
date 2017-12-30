import random
import numpy as np

# action = 0 <- players decides to stick
# action = 1 <- players decides to hit (draw)

class State:
    dealercard = random.randint(1,10)
    playersum = random.randint(1,21)

def drawcard(current):
    if random.randint(1,3) < 3:
        current += random.randint(1,10)
    else:
        current -= random.randint(1,10)
    return current

def step(state, action):
	if(action == 0): # player decides to stick
		while(state.dealercard < 17):
			state.dealercard = drawcard(state.dealercard)
			if(state.dealercard > 21 or state.dealercard < 1):
				return "terminal", +1.0
		if state.dealercard == state.playersum:
			return "terminal", 0.0
		elif state.dealercard > state.playersum:
			return "terminal", -1.0
		else:
			return "terminal", +1.0
		
	else:	 # player decides to hit and draw another card
		state.playersum = drawcard(state.playersum)
        if state.playersum < 1 or state.playersum > 21:
            return "terminal", -1.0
        else:
            return state, 0
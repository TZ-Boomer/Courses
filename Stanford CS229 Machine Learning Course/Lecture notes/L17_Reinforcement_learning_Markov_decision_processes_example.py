import numpy as np

"""
V) Reinforcement learning and control
Chapter 15
Reinforcement learning
"""

"""
In the lecture, only the next state reward is considered when choosing among the next actions. In fact, you should 
compute the value function for multiple next steps/actions not only the first one. Otherwise it is simply a greedy 
algorithm.
Also, int the lecture, you already have all the probabilities and reward given. In real case you have to discover it
by yourself. According to me, it is here that the real notion of machine learning takes on is full meaning (I may not 
have understood the lecture very well despite several re-readings). Check Q-learning on internet to get more infos. 
"""

"""
I understand better the algo now. We do not directly compute the next value function for the future actions, instead 
we use the previously computed value function from each state and use it as a prediction. Then multiply the previously 
computed value function by gamma to give them less importance and make the algorithm converge.
"""

""" 
Bellman equation : 
For each possible action at each step.
action_values[a] = np.sum(P[s, a] * (R[s, a] + gamma * V))

Multiply the potential value function you can get for each next step "V" by "gamma" to reduce its 
importance over time. Add this with the value function of each next step "R[s, a]". Finally multiply the
whole with the probability of going to each next step "P[s, a]". Then sum it to get the value function 
of this action. 

Why "V" represent the potential value you can get for going to the next state ?
"V" represent the value function of each state. When using "V" in the equation, you estimate of much value you can get 
after reaching a particular state. If the reward you get for going to a particular state is low "R[s, a]", but the value 
you can get after reaching to this next state is high "V", you more likely going to this next state.

Ex : 
   
    |---> s1(R=4) ---> s3(R=3)
s0 --
    |---> s2(R=2) ---> s4(R=10)  more likely, immediate reward lower, future reward higher.
"""


# Define MDP parameters
n_states = 3
n_actions = 2
gamma = 0.9
threshold = 1e-3

# Here you are on state s and chose action a, you have a certain probability to go to s0, s1 or s2 with action a. The
# sum of the possible results of your action sum up to 1
# Transition probabilities P[s, a, s']
P = np.array([
    [[0.8, 0.2, 0.0], [0.0, 1.0, 0.0]],  # From state 0
    [[1.0, 0.0, 0.0], [0.7, 0.0, 0.3]],  # From state 1
    [[0.1, 0.0, 0.9], [1.0, 0.0, 0.0]]   # From state 2
])

# Rewards R[s, a, s']
R = np.array([
    [[1, 2, 0], [0, 3, 0]],  # From state 0
    [[3, 0, 1], [0, 0, 2]],  # From state 1
    [[2, 0, 3], [0, 1, 0]]   # From state 2
])

# Initialize value function
V = np.zeros(n_states)


def value_iteration(V, P, R, gamma, threshold):
    iteration = 0

    while True:
        delta = 0

        for s in range(n_states):
            action_values = np.zeros(n_actions)

            for a in range(n_actions):
                action_values[a] = np.sum(P[s, a] * (R[s, a] + gamma * V))

            new_V = np.max(action_values)
            delta = max(delta, np.abs(new_V - V[s]))
            V[s] = new_V

        iteration += 1
        if delta < threshold:
            print(f"Value iteration converged in : {iteration} iterations." )
            break

    return V


# Compute optimal policy
def get_optimal_policy(V, P, R, gamma):
    policy = np.zeros(n_states, dtype=int)

    for s in range(n_states):
        action_values = np.zeros(n_actions)

        for a in range(n_actions):
            action_values[a] = np.sum(P[s, a] * (R[s, a] + gamma * V))

        policy[s] = np.argmax(action_values)

    return policy


# Compute optimal value function
V = value_iteration(V, P, R, gamma, threshold)
# Compute optimal policy
optimal_policy = get_optimal_policy(V, P, R, gamma)

print("Optimal value function : ", V)
print("Optimal policy : ", optimal_policy)


# Initialize policy randomly
policy = np.zeros(n_states, dtype=int)

def policy_evaluation(policy, P, R, gamma, threshold):
    V = np.zeros(n_states)

    while True:
        delta = 0

        for s in range(n_states):
            v = V[s]
            a = policy[s]
            V[s] = np.sum(P[s, a] * (R[s, a] + gamma * V))
            delta = max(delta, np.abs(v - V[s]))

        if delta < threshold:
            break

    return V


def policy_iteration(P, R, gamma, threshold):
    iteration = 0

    while True:
        # Policy Evaluation
        V = policy_evaluation(policy, P, R, gamma, threshold)

        # Policy Improvement
        policy_stable = True

        for s in range(n_states):
            old_action = policy[s]
            action_values = np.zeros(n_actions)

            for a in range(n_actions):
                action_values[a] = np.sum(P[s, a] * (R[s, a] + gamma * V))

            policy[s] = np.argmax(action_values)

            if old_action != policy[s]:
                policy_stable = False

        iteration += 1

        if policy_stable:
            print(f"Policy iteration converged in : {iteration} iterations." )
            break

    return V, policy


# Compute optimal policy and value function
V, optimal_policy = policy_iteration(P, R, gamma, threshold)

print("Optimal value function from policy computed : ", V)
print("Optimal policy re-computed : ", optimal_policy)

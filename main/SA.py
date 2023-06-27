#Simulated Annealing Algorithm general template

import math
import random

# Define your objective function f(x) here
# You need to implement this function according to your problem
def objective_function(x):
    # Example: minimize a quadratic function (x^2)
    return x * x

# Generate a random neighbor within the neighborhood N(s)
def generate_neighbor(s):
    # Example: randomly generate a neighbor by adding a small random value (-0.1 to 0.1)
    range_value = 0.1
    return s + random.uniform(-range_value, range_value)

# Set the algorithm parameters
alpha = 0.9    # Cooling rate
SAmax = 100    # Maximum number of iterations at each temperature
T0 = 100.0     # Initial temperature
T = T0         # Current temperature
s = 0.0        # Current solution
s_star = s     # Best solution obtained so far
iterT = 0      # Iteration counter at current temperature

while T > 0:
    iterT = 0

    while iterT < SAmax:
        iterT += 1

        # Generate a random neighbor
        s_prime = generate_neighbor(s)

        # Calculate the difference in objective function values
        delta = objective_function(s_prime) - objective_function(s)

        if delta < 0:
            s = s_prime
        else:
            x = random.random()
            if x < math.exp(-delta / T):
                s = s_prime

        # Update the best solution found so far
        if objective_function(s_prime) < objective_function(s_star):
            s_star = s_prime

    # Cool down the temperature
    T = alpha * T

print("Best solution found:", s_star)

#Simulated Annealing usando a heurística FirstFitDecreasing como solução inicial

import math
import random
import importlib
from FFD import Le_Instancia 
from FFD import FirstFitDecreasing

import random
import math

# Objective function using the FirstFitDecreasing heuristic
def objective_function(weight, n, c):
    return FirstFitDecreasing(weight, n, c)

# Technique 1: Relocation of a single selected item from one bin to another randomly selected bin
def technique1(weight, n, c):
    # Randomly select an item and its current bin
    item_idx = random.randint(0, n - 1)
    current_bin = weight[item_idx]
    
    # Randomly select a new bin
    new_bin = random.randint(0, n - 1)
    
    # Relocate the item to the new bin
    weight[item_idx] = new_bin
    
    return weight

# Technique 2: Random selection of two items allocated in two different bins and exchanging their positions
def technique2(weight, n, c):
    # Randomly select two items allocated in different bins
    item_idx1, item_idx2 = random.sample(range(n), 2)
    
    # Exchange the positions of the two items
    weight[item_idx1], weight[item_idx2] = weight[item_idx2], weight[item_idx1]
    
    return weight

# Simulated Annealing implementation
def simulated_annealing(weight, n, c, initial_temperature, cooling_rate, stopping_temperature):
    # Initial solution
    current_solution = objective_function(weight, n, c)
    best_solution = current_solution

    # Initialize temperature
    temperature = initial_temperature

    # Simulated Annealing loop
    while temperature > stopping_temperature:
        # Apply Technique 1 at higher temperatures, and Technique 2 at lower temperatures
        if temperature > (initial_temperature / 2):
            new_weight = technique1(list(weight), n, c)
        else:
            new_weight = technique2(list(weight), n, c)

        # Calculate the objective function for the new solution
        new_solution = objective_function(new_weight, n, c)

        # Accept the new solution if it improves the objective function
        if new_solution < current_solution:
            weight = new_weight
            current_solution = new_solution
        else:
            # Accept the new solution probabilistically based on the temperature
            probability = math.exp((current_solution - new_solution) / temperature)
            if random.random() < probability:
                weight = new_weight
                current_solution = new_solution

        # Update the best solution
        if current_solution < best_solution:
            best_solution = current_solution

        # Decrease the temperature
        temperature *= cooling_rate

    return best_solution

# Test a single instance using Simulated Annealing
filename = "/home/TEO/main/Wäscher/Waescher_TEST0005.txt"

weight = Le_Instancia(filename)

if weight:
    n = len(weight)
    c = 10000 # Capacity of each bin (given in each instance, modify as needed)
    initial_temperature = 100.0
    cooling_rate = 0.95
    stopping_temperature = 0.1

    best_solution = simulated_annealing(weight, n, c, initial_temperature, cooling_rate, stopping_temperature)
    print("Best solution found using Simulated Annealing for", filename, ":", best_solution)



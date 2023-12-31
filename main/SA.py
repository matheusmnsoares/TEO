import random
import math
from time import process_time

def Le_Instancia(filename):
    try:
        with open(filename, 'r') as file:
            # Skip the first two lines
            for _ in range(2):
                next(file)
            
            # lê os pesos dos itens a partir da 3ª linha (1° e 2° linha são informações sobre a instancia)
            weight = [int(line.strip()) for line in file]
            return weight
    except FileNotFoundError:
        print("Arquivo não encontrado. (Verifique se o arquivo está na pasta correta)")
        return []

def FirstFitDecreasing(weight, n, bin_capacity):
    # Inicializa objetivo (número de bins)
    # Pior caso: n = objetivo
    objetivo = 0

    # Cria uma lista para armazenar o espaço restante nos bins
    bin_rem = [0]*n

    # Lista de listas para armazenar as bins utilizadas com os itens dentro
    bins_used = [[] for _ in range(n)]

    # Ordena os itens em ordem decrescente de peso
    weight.sort(reverse=True)

    # Adiciona os itens um por um
    for i in range(n):
        # Acha a primeira bin que pode acomodar weight[i]
        j = 0
        while j < objetivo:
            if bin_rem[j] >= weight[i]:
                bin_rem[j] = bin_rem[j] - weight[i]
                bins_used[j].append(weight[i])  # Adiciona o item na bin
                break
            j += 1

        # Caso não exista bin que possa acomodar weight[i], cria um novo bin
        if j == objetivo:
            bin_rem[objetivo] = bin_capacity - weight[i]
            bins_used[objetivo].append(weight[i])  # Adiciona o item na nova bin
            objetivo = objetivo + 1

    bins_used = bins_used[:objetivo]

    return objetivo, bins_used


def cost_function(bins_used):
    return len(bins_used)

def simulated_annealing(weight, n, bin_capacity, initial_temperature, cooling_rate, max_iterations):
    # First Fit Decreasing initial solution
    objective, bins_used = FirstFitDecreasing(weight, n, bin_capacity)
    best_objective = objective
    best_solution = bins_used

    # Initialize temperature
    temperature = initial_temperature

    for i in range(max_iterations):
        # Generate a neighbor solution by perturbing the current solution
        neighbor_bins_used = generate_neighbour(bins_used, bin_capacity)
        #print(neighbor_bins_used)
        # Calculate the cost (number of bins) of the neighbor solution
        neighbor_objective = cost_function(neighbor_bins_used)
        #print(neighbor_objective)

        # Calculate the cost of the current solution
        current_objective = cost_function(bins_used)

        # Determine if the neighbor solution is accepted
        if neighbor_objective < current_objective:
            # Accept the neighbor solution if it's better
            bins_used = neighbor_bins_used
            objective = neighbor_objective

            # Update the best solution if necessary
            if neighbor_objective < best_objective:
                best_objective = neighbor_objective
                best_solution = neighbor_bins_used
        else:
            # Calculate the probability of accepting a worse solution
            probability = math.exp((current_objective - neighbor_objective) / temperature)

            # Accept the neighbor solution with a probability
            if random.random() < probability:
                bins_used = neighbor_bins_used
                objective = neighbor_objective
        
        # Cool down the temperature
        temperature *= cooling_rate
    #print(len(neighbor_bins_used))
    return best_objective, best_solution

def generate_neighbour(bins_used, bin_capacity):
    num_bins = len(bins_used)
    if num_bins < 2:
        return bins_used
    
    new_bins_used = [bin_content.copy() for bin_content in bins_used]

    # Perform item transfer: Try to move items from one bin to another if there's enough space
    for bin_from in range(num_bins):
        for bin_to in range(num_bins):
            if bin_from != bin_to:
                for item in new_bins_used[bin_from]:
                    if sum(new_bins_used[bin_to]) + item <= bin_capacity:
                        new_bins_used[bin_from].remove(item)
                        new_bins_used[bin_to].append(item)
                        break

    # Perform item swap: Choose two bins randomly
    bin1, bin2 = random.sample(range(num_bins), 2)

    # Swap items between bins
    item1 = random.choice(new_bins_used[bin1])
    item2 = random.choice(new_bins_used[bin2])
    if sum(new_bins_used[bin1]) - item1 + item2 <= bin_capacity and sum(new_bins_used[bin2]) - item2 + item1 <= bin_capacity:
        new_bins_used[bin1].remove(item1)
        new_bins_used[bin2].remove(item2)
        new_bins_used[bin1].append(item2)
        new_bins_used[bin2].append(item1)

    # Remove empty bins
    new_bins_used = [bin_content for bin_content in new_bins_used if bin_content]

    return new_bins_used



"""def generate_neighbour(bins_used, bin_capacity):
    num_bins = len(bins_used)
    if num_bins < 2:
        return bins_used
    
    new_bins_used = [bin_content.copy() for bin_content in bins_used]

    # Choose two bins randomly
    bin1, bin2 = random.sample(range(num_bins), 2)

    # Choose a random number of items to swap
    num_items_to_swap = random.randint(1, min(len(new_bins_used[bin1]), len(new_bins_used[bin2])))

    # Swap items between bins
    for _ in range(num_items_to_swap):
        item1 = random.choice(new_bins_used[bin1])
        item2 = random.choice(new_bins_used[bin2])
        if sum(new_bins_used[bin1]) - item1 + item2 <= bin_capacity and sum(new_bins_used[bin2]) - item2 + item1 <= bin_capacity:
            new_bins_used[bin1].remove(item1)
            new_bins_used[bin2].remove(item2)
            new_bins_used[bin1].append(item2)
            new_bins_used[bin2].append(item1)

    # Remove empty bins
    new_bins_used = [bin_content for bin_content in new_bins_used if bin_content]

    return new_bins_used"""



# Mede o tempo de execução do Simulated Annealing
def measure_execution_time(weight, n, bin_capacity, initial_temperature, cooling_rate, max_iterations):
    start_time = process_time()
    best_objective, best_solution = simulated_annealing(weight, n, bin_capacity, initial_temperature, cooling_rate, max_iterations)
    end_time = process_time()
    execution_time = end_time - start_time
    return best_objective, best_solution, execution_time

filename = "/home/TEO/main/Scholl/Scholl_3/HARD0.txt"  
weight = Le_Instancia(filename)
n = len(weight)
bin_capacity = 100000 # Replace with the bin capacity
initial_temperature = 1000
cooling_rate = 0.95
max_iterations = 1000

best_objective, best_solution, execution_time = measure_execution_time(weight, n, bin_capacity, initial_temperature, cooling_rate, max_iterations)

print("Best number of bins:", best_objective)
print("Tempo de execução:", execution_time, "segundos")
print("Best solution (bins used):", best_solution)

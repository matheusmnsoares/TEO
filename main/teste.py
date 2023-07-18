import random
import math

def Le_Instancia(filename):
    try:
        with open(filename, 'r') as file:
            weight = [int(line.strip()) for line in file]
            return weight
    except FileNotFoundError:
        print("Arquivo não encontrado. (Verifique se o arquivo está na pasta correta)")
        return []

def FirstFitDecreasing(weight, n, c):
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
            bin_rem[objetivo] = c - weight[i]
            bins_used[objetivo].append(weight[i])  # Adiciona o item na nova bin
            objetivo = objetivo + 1

    return objetivo, bins_used

def cost_function(bins_used):
    return len(bins_used)

def simulated_annealing(weight, n, c, initial_temperature, cooling_rate, max_iterations):
    # First Fit Decreasing initial solution
    objective, bins_used = FirstFitDecreasing(weight, n, c)
    best_objective = objective
    best_solution = bins_used

    # Initialize temperature
    temperature = initial_temperature

    for iteration in range(max_iterations):
        # Generate a neighbor solution by perturbing the current solution
        neighbor_bins_used = perturb_solution(bins_used,temperature)

        # Calculate the cost (number of bins) of the neighbor solution
        neighbor_objective = cost_function(neighbor_bins_used)

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

    return best_objective, best_solution

def perturb_solution(bins_used, temperature):
    # Randomly select two bins and exchange a random item between them (Technique 2)
    # Random selection of a single item and relocation to another package (Technique 1)

    num_bins = len(bins_used)
    if num_bins < 2:
        return bins_used

    new_bins_used = bins_used.copy()

    if temperature < 100:  # Use Technique 2 at lower temperatures
        bin1, bin2 = random.sample(range(num_bins), 2)
        if len(new_bins_used[bin1]) > 0 and len(new_bins_used[bin2]) > 0:
            item1 = random.choice(new_bins_used[bin1])
            item2 = random.choice(new_bins_used[bin2])

            new_bins_used[bin1].remove(item1)
            new_bins_used[bin1].append(item2)

            new_bins_used[bin2].remove(item2)
            new_bins_used[bin2].append(item1)
    else:  # Use Technique 1 at higher temperatures
        bin1, bin2 = random.sample(range(num_bins), 2)
        if len(new_bins_used[bin1]) > 0:
            item = random.choice(new_bins_used[bin1])

            new_bins_used[bin1].remove(item)
            new_bins_used[bin2].append(item)

    return new_bins_used


filename = "/home/TEO/main/Wäscher/Waescher_TEST0005.txt"  
weight = Le_Instancia(filename)
n = len(weight)
c = 10000 # Replace with the bin capacity
initial_temperature = 10000
cooling_rate = 0.75
max_iterations = 10000

best_objective, best_solution = simulated_annealing(weight, n, c, initial_temperature, cooling_rate, max_iterations)

print("Best number of bins:", best_objective)
#print("Best solution (bins used):", best_solution)

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


def apply_2opt(bins):
    # Initialize the best cost and best solution
    best_cost = cost_function(bins)
    best_bins = bins

    # Apply the 2-opt technique to find a better solution
    improved = True
    while improved:
        improved = False
        for i in range(len(bins)):
            for j in range(i+1, len(bins)):
                # Reverse the items between i and j
                new_bins = bins[:i] + list(reversed(bins[i:j+1])) + bins[j+1:]
                new_cost = cost_function(new_bins)

                # If the new solution is better, update the current solution
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_bins = new_bins
                    improved = True
                    break
            if improved:
                break

    return best_bins


def perturb_solution(bins_used, bin_capacity, k=2):
    # Select k random non-empty bins
    bins = [i for i in range(len(bins_used)) if bins_used[i]]
    if len(bins) < k:
        return bins_used
    selected_bins = random.sample(bins, k)

    # Apply 2-opt within each selected bin to find a better solution
    improved_bins = [apply_2opt(bins_used[i]) if i in selected_bins else bins_used[i] for i in range(len(bins_used))]

    # Swap items between the selected bins to create a perturbed solution
    for i in range(len(selected_bins)):
        for j in range(i+1, len(selected_bins)):
            bin1, bin2 = selected_bins[i], selected_bins[j]
            if not improved_bins[bin1] or not improved_bins[bin2]:
                continue
            # Select a random item to swap between the two bins
            item = random.choice(improved_bins[bin1])
            if sum(improved_bins[bin2]) + item <= bin_capacity:
                improved_bins[bin1].remove(item)
                improved_bins[bin2].append(item)

    # Apply 2-opt to the perturbedsolution to further improve it
    improved_bins = apply_2opt(improved_bins)

    return improved_bins


def simulated_annealing(weight, n, bin_capacity, initial_temperature=100, cooling_rate=0.95, stopping_temperature=1e-8, max_iterations=1000):
    # Initialize the current solution
    current_obj, current_sol = FirstFitDecreasing(weight, n, bin_capacity)

    # Initialize the best solution and its cost
    best_obj = current_obj
    best_sol = current_sol

    # Initialize the temperature
    temperature = initial_temperature

    # Iterate until reaching the stopping temperature or maximum number of iterations
    for i in range(max_iterations):
        # Generate a perturbed solution
        perturbed_sol = perturb_solution(current_sol, bin_capacity)

        # Compute the cost of the perturbed solution
        perturbed_obj = cost_function(perturbed_sol)

        # Compute the delta of the cost between the perturbed and current solutions
        delta_obj = perturbed_obj - current_obj

        # Accept the perturbed solution if it is better or with a probability based on the temperature
        if delta_obj < 0 or math.exp(-delta_obj/temperature) > random.random():
            current_obj = perturbed_obj
            current_sol = perturbed_sol

        # Update the best solution if the current solution is better
        if current_obj < best_obj:
            best_obj = current_obj
            best_sol = current_sol

        # Decrease the temperature
        temperature *= cooling_rate

        # Stop if the temperature is below the stopping temperature
        if temperature < stopping_temperature:
            break

    return best_obj, best_sol


filename = '/home/TEO/main/Falkenauer/Falkenauer_U/Falkenauer_u120_00.txt'
bin_capacity = 150
initial_temperature = 100
cooling_rate = 0.95
stopping_temperature = 1e-8
max_iterations = 1000

weight = Le_Instancia(filename)
n = len(weight)

best_obj, best_sol = simulated_annealing(weight, n, bin_capacity, initial_temperature, cooling_rate, stopping_temperature, max_iterations)

print(f"Number of bins used: {best_obj}")
print("Bins used with items inside:")
for bin_items in best_sol:
    print(bin_items)



""" def generate_neighbour(bins_used, bin_capacity):
    num_bins = len(bins_used)
    if num_bins < 2:
        return bins_used
    
    new_bins_used = [bin_content.copy() for bin_content in bins_used]

    # Choose a source bin randomly
    bin1 = random.randint(0, num_bins - 1)
    
    
    if len(new_bins_used[bin1]) > 0:
        item = random.choice(new_bins_used[bin1])
        bin2 = random.randint(0, num_bins - 1)
        
       
        if sum(new_bins_used[bin2]) + item <= bin_capacity:   
            new_bins_used[bin1].remove(item)
            new_bins_used[bin2].append(item)
            
            if not new_bins_used[bin1]:
                new_bins_used.pop(bin1)
                
    return new_bins_used"""
#Simulated Annealing usando a heurística FirstFitDecreasing como solução inicial

import math
import random
import time
import importlib
from FFD import Le_Instancia 
from FFD import FirstFitDecreasing

# Gerando a solução inicial usando a heurística FirstFitDecreasing
def objective_function(weight, n, c):
    return FirstFitDecreasing(weight, n, c)

# Técnica 1
def technique1(weight, n, c):
    item_idx = random.randint(0, n - 1)
    
    new_item = random.randint(0, n - 1)
    #print(new_item)
    
    weight[item_idx] = new_item
    
    return weight

# Técnica 2
def technique2(weight, n, c):
    # Aleatoriamente seleciona dois itens alocados em bins diferentes
    item_idx1, item_idx2 = random.sample(range(n), 2)
    
    # Troca as posições dos dois itens
    weight[item_idx1], weight[item_idx2] = weight[item_idx2], weight[item_idx1]
    
    return weight

def simulated_annealing(weight, n, c, initial_temperature, cooling_rate, stopping_temperature):
    # Inicializa a solução atual com a função objetivo
    current_solution = objective_function(weight, n, c)
    best_solution = current_solution

    # Inicializa a temperatura
    temperature = initial_temperature

    # Simulated Annealing loop
    while temperature > stopping_temperature:
        # Aplica a técnica 1 quando a temperatura é maior que a metade da temperatura inicial e a técnica 2 caso contrário
        if temperature > (initial_temperature / 2):
            new_weight = technique1(list(weight), n, c)
        else:
            new_weight = technique2(list(weight), n, c)

        # Calcula a função objetivo da nova solução
        new_solution = objective_function(new_weight, n, c)

        # Aceita a nova solução se ela for melhor que a solução atual
        if new_solution < current_solution:
            weight = new_weight
            current_solution = new_solution
        else:
            # Aceita a nova solução probabilisticamente baseado na temperatura
            probability = math.exp((current_solution - new_solution) / temperature)
            if random.random() < probability:
                weight = new_weight
                current_solution = new_solution

        # Atualiza a melhor solução
        if current_solution < best_solution:
            best_solution = current_solution

        # Diminui a temperatura
        temperature *= cooling_rate

    return best_solution

# Mede o tempo de execução do Simulated Annealing
def measure_execution_time(weight, n, c, initial_temperature, cooling_rate, stopping_temperature):
    start_time = time.time()
    best_solution = simulated_annealing(weight, n, c, initial_temperature, cooling_rate, stopping_temperature)
    end_time = time.time()
    execution_time = end_time - start_time
    return best_solution, execution_time

# Testa uma única instancia usando Simulated Annealing
filename = "/home/TEO/main/Wäscher/Waescher_TEST0005.txt"

weight = Le_Instancia(filename)

if weight:
    n = len(weight)
    c = 10000 # Capacidade de cada bin ( dada em cada uma das instancias, alterar conforme necessário)
    initial_temperature = 100.0
    cooling_rate = 0.95
    stopping_temperature = 0.1

    best_solution, execution_time = measure_execution_time(weight, n, c, initial_temperature, cooling_rate, stopping_temperature)
    print("Melhor solução encontrada com o Simulated Annealing:", filename, ":", best_solution)
    print("Tempo de execução:", execution_time, "segundos")




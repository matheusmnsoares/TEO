#Implementação da heurística de solução inicial First Fit Decreasing (FFD)
#Instancias disponíveis para o teste: Falkenauer_U, Falkenauer_T, Scholl_1, Scholl_2 e Scholl_3 (copiar o path)
#Encontradas em https://site.unibo.it/operations-research/en/research/bpplib-a-bin-packing-problem-library

# weight[]: lista de pesos dos itens
# n: número de itens
# c: capacidade de cada bin

import os

# Lê os pesos do arquivo de instancias e cria a lista weight
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

    bins_used = bins_used[:objetivo]

    return objetivo, bins_used




# Testa uma única instancia

filename = "/home/TEO/main/Falkenauer/Falkenauer_U/Falkenauer_u120_00.txt"

weight = Le_Instancia(filename)

if weight:
    n = len(weight)
    c = 150 # Capacidade de cada bin ( dada em cada uma das instancias, alterar conforme necessário)
    best_objective, best_solution = FirstFitDecreasing(weight, n, c)
    print("Numero mínimo de bins necessarias em", filename, ":" , best_objective) 
    print("Bins utilizadas:", best_solution)
    print("Custo:", len(best_solution))




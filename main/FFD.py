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
            weight = [int(line.strip()) for line in file]
            return weight
    except FileNotFoundError:
        print("Arquivo não encontrado. (Verifique se o arquivo está na pasta correta)")
        return []
    
    
# Retorna o número mínimo de bins necessários para alocar os itens com a heurística FFD
def FirstFitDecreasing(weight, n, c):
    # Inicializa objetivo (número de bins)
    # Pior caso: n = objetivo
    objetivo = 0
    
    # Cria uma lista para armazenar o espaço restante nos bins
    bin_rem = [0]*n

    # Ordena os itens em ordem decrescente de peso
    weight.sort(reverse=True)
    # Adiciona os itens um por um
    for i in range(n):
        # Acha a primeira bin que pode acomodar weight[i]
        j = 0
        while j < objetivo:
            if bin_rem[j] >= weight[i]:
                bin_rem[j] = bin_rem[j] - weight[i]
                break
            j += 1

        # Caso não exista bin que possa acomodar weight[i], cria um novo bin
        if j == objetivo:
            bin_rem[objetivo] = c - weight[i]
            objetivo = objetivo + 1
    return objetivo

# Testa uma única instancia

capacidade = input("Defina a capacidade do bin: ")

filename = "/home/TEO/main/Falkenauer/Falkenauer_U/Falkenauer_u120_04.txt"

weight = Le_Instancia(filename)

if weight:
    n = len(weight)
    c = int(capacidade) # Capacidade de cada bin ( dada em cada uma das instancias, alterar conforme necessário)
    print("Numero mínimo de bins necessarias em", filename, ":", FirstFitDecreasing(weight, n, c))

# Testa múltiplas instancias de uma pasta

"""folder_path = "/home/TEO/main/Falkenauer/Falkenauer_U"

file_list = os.listdir(folder_path)
file_list.sort()  # Ordena os arquivos por ordem alfabética
    
for filename in file_list:
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        weight = Le_Instancia(file_path)
        if weight:
            n = len(weight)
            c = int(capacidade) # Capacidade de cada bin ( dada em cada uma das instancias, alterar conforme necessário)
            print("Numero mínimo de bins necessarias em", filename, ":", FirstFitDecreasing(weight, n, c))"""
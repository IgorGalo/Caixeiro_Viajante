"""
Algoritmo Genético para o Problema do Caixeiro Viajante (PCV)
===============================================================
Implementação baseada nos slides "Grafos - Algoritmo genético para
solução do Problema do Caixeiro Viajante" (Prof. Vinícius da Fonseca
Vieira - UFSJ) e no exemplo manuscrito de execução do AG.

Elementos implementados conforme os slides:
    - Representação: vetor de n posições com permutação das cidades (slide 11)
    - Função objetivo: soma das distâncias do circuito, ver Eq. (1) (slide 7 e 10)
    - Seleção: roleta viciada, proporcional ao fitness (slides 19-20)
    - Cruzamento: OX - order crossover (slides 12-14)
    - Mutação: troca de posição gene a gene, com taxa pm (slides 15-17)
    - Elitismo: mantém os melhores indivíduos entre gerações (slide 18)
    - Critério de parada: número máximo de gerações (slide 24)
"""

import random
import time
import itertools


# =============================================================== #
#  Estrutura do indivíduo
# =============================================================== #
class Individuo:
    def __init__(self, dna):
        self.dna = dna       # permutação das cidades (o cromossomo)
        self.fitness = 0     # distância total do circuito


# =============================================================== #
#  Leitura da instância (matriz de distâncias, ex.: lau15_dist.txt)
# =============================================================== #
def carregaMatrizDistancias(caminho_arquivo):
    """
    Lê um arquivo de matriz de distâncias no formato n x n
    (uma linha por cidade, valores separados por espaço),
    como o lau15_dist.txt / sgb128_dist.txt citados no slide 22.
    """
    matriz = []
    with open(caminho_arquivo, "r") as arquivo:
        for linha in arquivo:
            valores = linha.split()
            if valores:
                matriz.append([float(v) for v in valores])
    return matriz


# =============================================================== #
#  Criação do DNA (representação - permutação das cidades)
# =============================================================== #
def criaDNA(n_cidades):
    dna = list(range(n_cidades))
    random.shuffle(dna)
    return dna


# =============================================================== #
#  Função objetivo (Equação 1 do slide 7)
#  f(pi) = soma_{i=1}^{n-1} rho(pi(i), pi(i+1)) + rho(pi(n), pi(1))
# =============================================================== #
def calculaFitness(individuo, matriz_distancias):
    n = len(individuo.dna)
    distancia_total = 0.0
    for i in range(n - 1):
        cidade_atual = individuo.dna[i]
        proxima_cidade = individuo.dna[i + 1]
        distancia_total += matriz_distancias[cidade_atual][proxima_cidade]
    # fecha o circuito, voltando para a cidade de origem
    distancia_total += matriz_distancias[individuo.dna[n - 1]][individuo.dna[0]]
    individuo.fitness = distancia_total


# =============================================================== #
#  Seleção por roleta viciada (slides 19-20)
#  Como o problema é de MINIMIZAÇÃO, o peso é o inverso do fitness:
#  quanto menor a distância, maior a "fatia" da roleta.
# =============================================================== #
def selecaoPais(populacao):
    pesos = [1 / individuo.fitness for individuo in populacao]
    return random.choices(populacao, weights=pesos, k=2)


# =============================================================== #
#  Cruzamento OX - order crossover (slides 12-14)
#  1) Sorteiam-se dois pontos de corte
#  2) O trecho entre os pontos do pai1 é preservado no filho,
#     na mesma posição
#  3) O restante do filho é preenchido na ordem em que os genes
#     aparecem no pai2, pulando os que já estão no trecho herdado
# =============================================================== #
def cruzamentoOX(pai1, pai2):
    n = len(pai1.dna)

    ponto1 = random.randint(0, n - 1)
    ponto2 = random.randint(0, n - 1)
    inicio, fim = min(ponto1, ponto2), max(ponto1, ponto2)

    trecho_preservado = pai1.dna[inicio:fim + 1]

    dna_filho = [None] * n
    dna_filho[inicio:fim + 1] = trecho_preservado

    # percorre o pai2 a partir da posição subsequente ao 2º ponto
    # sorteado (como descrito no slide 14), preenchendo o filho
    # de forma circular e pulando genes já usados
    genes_pai2 = pai2.dna[fim + 1:] + pai2.dna[:fim + 1]
    genes_restantes = [gene for gene in genes_pai2 if gene not in trecho_preservado]

    posicao = (fim + 1) % n
    for gene in genes_restantes:
        dna_filho[posicao] = gene
        posicao = (posicao + 1) % n

    return Individuo(dna_filho)


# =============================================================== #
#  Mutação por troca de posição (slides 15-17)
#  Para cada gene do cromossomo sorteia-se r em [0,1];
#  se r <= taxa_mutacao, sorteia-se outra posição e troca-se
#  os dois valores.
# =============================================================== #
def mutacao(individuo, taxa_mutacao):
    n = len(individuo.dna)
    for i in range(n):
        r = random.random()
        if r <= taxa_mutacao:
            j = random.randint(0, n - 1)
            individuo.dna[i], individuo.dna[j] = individuo.dna[j], individuo.dna[i]


# =============================================================== #
#  Loop principal do AG (segue o fluxograma do slide 23)
# =============================================================== #
def algoritmoGenetico(matriz_distancias, tam_populacao, taxa_cruzamento,
                       taxa_mutacao, num_geracoes, tam_elite=2):
    n_cidades = len(matriz_distancias)

    # população inicial (aleatória)
    populacao = [Individuo(criaDNA(n_cidades)) for _ in range(tam_populacao)]
    for individuo in populacao:
        calculaFitness(individuo, matriz_distancias)

    historico_melhor_fitness = []

    for geracao in range(num_geracoes):
        populacao.sort(key=lambda ind: ind.fitness)
        historico_melhor_fitness.append(populacao[0].fitness)

        # elitismo: os melhores indivíduos passam direto para a
        # próxima geração (slide 18)
        nova_populacao = [Individuo(populacao[i].dna[:]) for i in range(tam_elite)]
        for i in range(tam_elite):
            nova_populacao[i].fitness = populacao[i].fitness

        # seleção + cruzamento + mutação até completar a população
        while len(nova_populacao) < tam_populacao:
            pai1, pai2 = selecaoPais(populacao)

            if random.random() <= taxa_cruzamento:
                filho1 = cruzamentoOX(pai1, pai2)
                filho2 = cruzamentoOX(pai2, pai1)
            else:
                filho1 = Individuo(pai1.dna[:])
                filho2 = Individuo(pai2.dna[:])

            mutacao(filho1, taxa_mutacao)
            mutacao(filho2, taxa_mutacao)

            calculaFitness(filho1, matriz_distancias)
            calculaFitness(filho2, matriz_distancias)

            nova_populacao.append(filho1)
            if len(nova_populacao) < tam_populacao:
                nova_populacao.append(filho2)

        populacao = nova_populacao

    populacao.sort(key=lambda ind: ind.fitness)
    return populacao[0], historico_melhor_fitness


# =============================================================== #
#  Execução principal - experimento fatorial (slide 25)
#  Varia: tamanho da população, taxa de cruzamento, taxa de mutação
# =============================================================== #
if __name__ == "__main__":

    caminho_arquivo = "lau15_dist.txt"   # troque pelo caminho da sua instância
    matriz_distancias = carregaMatrizDistancias(caminho_arquivo)

    num_geracoes = 500
    numero_de_testes_por_config = 5   # repetições de cada configuração

    # defina aqui os 3 valores de cada parâmetro para o fatorial
    tamanhos_populacao = [20, 50, 100]
    taxas_cruzamento = [0.7, 0.85, 0.95]
    taxas_mutacao = [0.01, 0.05, 0.10]

    melhor_global = None
    melhor_fitness_global = float("inf")

    tempo_inicio = time.time()

    with open("tabela_de_resultados.txt", "w") as arquivo:
        arquivo.write("===== RESULTADOS DO EXPERIMENTO FATORIAL - AG PCV =====\n\n")

        combinacoes = itertools.product(tamanhos_populacao, taxas_cruzamento, taxas_mutacao)

        for tam_pop, taxa_cx, taxa_mut in combinacoes:
            fitness_dos_testes = []

            for teste in range(numero_de_testes_por_config):
                melhor_individuo, historico = algoritmoGenetico(
                    matriz_distancias,
                    tam_populacao=tam_pop,
                    taxa_cruzamento=taxa_cx,
                    taxa_mutacao=taxa_mut,
                    num_geracoes=num_geracoes,
                )

                fitness_dos_testes.append(melhor_individuo.fitness)

                if melhor_individuo.fitness < melhor_fitness_global:
                    melhor_fitness_global = melhor_individuo.fitness
                    melhor_global = melhor_individuo

            media_fitness = sum(fitness_dos_testes) / len(fitness_dos_testes)
            melhor_fitness_config = min(fitness_dos_testes)

            linha_resultado = (
                f"Pop={tam_pop:4d} | Cruzamento={taxa_cx:.2f} | Mutacao={taxa_mut:.2f} "
                f"-> melhor={melhor_fitness_config:.2f} | media={media_fitness:.2f}\n"
            )
            arquivo.write(linha_resultado)
            print(linha_resultado.strip())

        tempo_fim = time.time()
        tempo_total = tempo_fim - tempo_inicio
        minutos = int(tempo_total // 60)
        segundos = int(tempo_total % 60)

        arquivo.write(f"\nMelhor solução encontrada em toda a bateria: {melhor_fitness_global:.2f}\n")
        arquivo.write(f"Rota: {melhor_global.dna}\n")
        arquivo.write(f"Tempo total: {minutos} minuto(s) e {segundos} segundo(s)\n")

    print(f"\nMelhor solução encontrada: {melhor_fitness_global:.2f}")
    print(f"Rota: {melhor_global.dna}")
    print(f"Tempo total: {minutos} minuto(s) e {segundos} segundo(s)")
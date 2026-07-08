import random
import time
import itertools
import sys


class Individuo:
    def __init__(self, dna):
        self.dna = dna       # permutação das cidades (o cromossomo)
        self.fitness = 0     # distância total do circuito


def listaNomesGrafos(caminho_arquivo="grafos.txt"):

    nomes = []
    with open(caminho_arquivo, "r") as arquivo:
        for linha in arquivo:
            linha_simples = linha.strip()
            if linha_simples.startswith("[") and linha_simples.endswith("]"):
                nomes.append(linha_simples[1:-1])
    return nomes

def carregaMatrizDistancias(grafo_escolhido, caminho_arquivo="grafos.txt"):

    matriz = []
    lendo_alvo = False
 
    with open(caminho_arquivo, "r") as arquivo:
        for linha in arquivo:
            linha_simples = linha.strip()
 
            # pula linha vazia
            if not linha_simples:
                continue
 
            # se a linha é um título
            if linha_simples.startswith("[") and linha_simples.endswith("]"):
                # e esse for o grafo requisitado, aciona a flag
                if linha_simples[1:-1] == grafo_escolhido:
                    lendo_alvo = True
                # caso contrário, abaixa a flag
                else:
                    lendo_alvo = False
                continue
 
            # se a flag estiver acionada, guarda a linha da matriz
            if lendo_alvo:
                valores = linha_simples.split()
                matriz.append([float(v) for v in valores])
 
    if not matriz:
        raise ValueError(
            f"Grafo '{grafo_escolhido}' não encontrado em '{caminho_arquivo}'."
        )
 
    return matriz


def escolheInstancia(caminho_arquivo="grafos.txt"):

    nomes_disponiveis = listaNomesGrafos(caminho_arquivo)
 
    if not nomes_disponiveis:
        raise ValueError(f"Nenhum grafo (seção [nome]) encontrado em '{caminho_arquivo}'.")
 
    if len(sys.argv) > 1:
        nome_escolhido = sys.argv[1]
        if nome_escolhido in nomes_disponiveis:
            print(f"Usando grafo informado por linha de comando: {nome_escolhido}")
            return nome_escolhido
        else:
            print(f"Aviso: grafo '{nome_escolhido}' não encontrado em '{caminho_arquivo}'. "
                  f"Prosseguindo com seleção interativa.\n")
 
    print("===== Grafos disponíveis =====")
    for indice, nome in enumerate(nomes_disponiveis, start=1):
        print(f"  [{indice}] {nome}")
    print("=" * 31)
 
    while True:
        escolha = input(f"Escolha o grafo (1-{len(nomes_disponiveis)}): ").strip()
 
        if escolha.isdigit():
            escolha_num = int(escolha)
            if 1 <= escolha_num <= len(nomes_disponiveis):
                return nomes_disponiveis[escolha_num - 1]
 
        print("Opção inválida. Digite um número da lista.\n")


def criaDNA(n_cidades):
    dna = list(range(n_cidades))
    random.shuffle(dna)
    return dna


def calculaFitness(individuo, matriz_distancias):
    n = len(individuo.dna)
    distancia_total = 0.0
    for i in range(n - 1):
        cidade_atual = individuo.dna[i]
        proxima_cidade = individuo.dna[i + 1]
        distancia_total += matriz_distancias[cidade_atual][proxima_cidade]
    
    distancia_total += matriz_distancias[individuo.dna[n - 1]][individuo.dna[0]]
    individuo.fitness = distancia_total


def selecaoPais(populacao):
    pesos = [1 / individuo.fitness for individuo in populacao]
    return random.choices(populacao, weights=pesos, k=2)


def cruzamentoOX(pai1, pai2):
    n = len(pai1.dna)

    ponto1 = random.randint(0, n - 1)
    ponto2 = random.randint(0, n - 1)
    inicio, fim = min(ponto1, ponto2), max(ponto1, ponto2)

    trecho_preservado = pai1.dna[inicio:fim + 1]

    dna_filho = [None] * n
    dna_filho[inicio:fim + 1] = trecho_preservado

    genes_pai2 = pai2.dna[fim + 1:] + pai2.dna[:fim + 1]
    genes_restantes = [gene for gene in genes_pai2 if gene not in trecho_preservado]

    posicao = (fim + 1) % n
    for gene in genes_restantes:
        dna_filho[posicao] = gene
        posicao = (posicao + 1) % n

    return Individuo(dna_filho)


def mutacao(individuo, taxa_mutacao):
    n = len(individuo.dna)
    for i in range(n):
        r = random.random()
        if r <= taxa_mutacao:
            j = random.randint(0, n - 1)
            individuo.dna[i], individuo.dna[j] = individuo.dna[j], individuo.dna[i]


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


if __name__ == "__main__":

    caminho_arquivo_grafos = "grafos.txt"  
    grafo_escolhido = escolheInstancia(caminho_arquivo_grafos)  
    print(f"\nGrafo selecionado: {grafo_escolhido}\n")
    matriz_distancias = carregaMatrizDistancias(grafo_escolhido, caminho_arquivo_grafos)

    num_geracoes = 500
    numero_de_testes_por_config = 5   # repetições de cada configuração

    tamanhos_populacao = [20, 50, 100]
    taxas_cruzamento = [0.7, 0.85, 0.95]
    taxas_mutacao = [0.01, 0.05, 0.10]

    melhor_global = None
    melhor_fitness_global = float("inf")

    tempo_inicio = time.time()

    with open("tabela_de_resultados.txt", "w") as arquivo:

        arquivo.write("===== RESULTADOS =====\n\n")
        arquivo.write(f"Grafo utilizado: {grafo_escolhido}\n")
        arquivo.write(f"Numero de cidades: {len(matriz_distancias)}\n\n")

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
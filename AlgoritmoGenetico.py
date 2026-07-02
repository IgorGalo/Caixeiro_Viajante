import networkx as nx
import random
import time
class Individuo:
    def __init__(self, dna):
        self.dna = dna          # ordem das cidades
        self.fitness = 0        # distância total


def criaDNA(Grafo):

    dna = []

    for esquina in Grafo.nodes:

        if Grafo.degree[esquina] > 0:
            dna.append(esquina)

    random.shuffle(dna)
    return dna

def calculaFitness(individuo, Grafo):

    grafo_aux = Grafo.copy()
    gene_atual = 0
    fitness = 0

    individuo.esquinas_com_camera_ind.clear()

    while(grafo_aux.number_of_edges() > 0):
        
        novas_cameras = limpaGrafo(grafo_aux)

        if(len(novas_cameras) > 0):

            fitness = fitness + len(novas_cameras)
            individuo.esquinas_com_camera_ind.update(novas_cameras)
            continue

        else:

            esquina_escolhida = individuo.dna[gene_atual]

            if(grafo_aux.degree[esquina_escolhida] == 0):
                gene_atual += 1
            
            else:

                ruas_perigosas = list(grafo_aux.edges(esquina_escolhida))
                grafo_aux.remove_edges_from(ruas_perigosas)
                individuo.esquinas_com_camera_ind.add(esquina_escolhida)
                gene_atual += 1
                fitness += 1

    individuo.fitness = fitness

def selecaoPais(populacao):
    
    pesos = []

    for individuo in populacao:
        pesos.append(1 / individuo.fitness)

    return random.choices(populacao, weights=pesos, k = 2)

def criaFilho(pai1, pai2):

    tam_corte = int(len(pai1.dna) * 0.4)
    limite = len(pai1.dna) - tam_corte
    inicio = random.randint(0, limite)
    corte = pai1.dna[inicio : inicio + tam_corte]

    dna_usado = []

    for gene in pai2.dna:

        if(gene not in corte):
            dna_usado.append(gene)

    ponto_do_corte = random.randint(0, len(dna_usado))

    dna_filho = dna_usado[: ponto_do_corte] + corte + dna_usado[ponto_do_corte:]

    filho = Individuo(dna_filho)

    return filho

def mutacao(individuo, taxa_mutacao=0.05):

    if random.random() < taxa_mutacao:

        gene01 = random.randint(0, len(individuo.dna) - 1)
        gene02 = random.randint(0, len(individuo.dna) - 1)

        individuo.dna[gene01], individuo.dna[gene02] = individuo.dna[gene02], individuo.dna[gene01]


# =============================================================================================== #

caminho_arquivo = "sjdr.gml"
Grafo = nx.read_gml(caminho_arquivo)
grafo_limpo = Grafo.copy()
cameras_base = limpaGrafo(grafo_limpo)

melhor_fitness = float('inf')
melhor_individuo = None
cobertura_camera = {}

numero_de_testes = 10

tempo_inicio = time.time()

with open("tabela_de_resultados.txt", "w") as arquivo:
    
    arquivo.write("===== RESULTADOS DA BATERIA =====\n")

    for teste in range(numero_de_testes):

        populacao = []

        for i in range(20):

            individuo = Individuo(criaDNA(grafo_limpo))
            populacao.append(individuo)

        for individuo in populacao:

            calculaFitness(individuo, grafo_limpo)

        flag = 0

        for geracao in range(100):

            nova_populacao = []

            populacao.sort(key=lambda ind: ind.fitness)

            nova_populacao.append(populacao[0])
            nova_populacao.append(populacao[1])

            for i in range(9):

                pais = selecaoPais(populacao)
                filho01 = criaFilho(pais[0], pais[1])
                filho02 = criaFilho(pais[1], pais[0])
                mutacao(filho01)
                mutacao(filho02)
                nova_populacao.append(filho01)
                nova_populacao.append(filho02)

            for individuo in nova_populacao:

                if(individuo.fitness == 0):
                    calculaFitness(individuo, grafo_limpo)

            populacao = nova_populacao

        
        populacao.sort(key=lambda ind: ind.fitness)
        mais_apto = populacao[0]
        total_cameras = mais_apto.fitness + len(cameras_base)

        if total_cameras < melhor_fitness:

            melhor_fitness = total_cameras
            melhor_individuo = mais_apto

        linha_resultado = f"Teste {teste + 1:02d}: {total_cameras} cameras\n"
        arquivo.write(linha_resultado)
        print(f"Teste {teste + 1:02d} concluído com {total_cameras} câmeras.")
    
    loc_cameras = melhor_individuo.esquinas_com_camera_ind.union(cameras_base)

    tempo_fim = time.time()

    tempo_total = tempo_fim - tempo_inicio
    minutos = int(tempo_total // 60)
    segundos = int(tempo_total % 60)

    print(f'O programa demorou {minutos} minuto(s) e {segundos} segundo(s) para concluir a bateria.\n')
    
    for camera_atual in loc_cameras:

            ruas_camera_atual = set()

            for vizinho in Grafo.neighbors(camera_atual):

                rua = Grafo[camera_atual][vizinho]
                nome_rua = rua.get('name')

                if isinstance(nome_rua, list):
                    ruas_camera_atual.update(nome_rua)
                
                else:
                    ruas_camera_atual.add(nome_rua)

            cobertura_camera[camera_atual] = list(ruas_camera_atual)


with open("relatorio_cameras", "w", encoding="utf-8") as arquivo:

    arquivo.write("Segue a relação de quais ruas cada câmera está monitorando.\n\n")

    for camera, ruas in cobertura_camera.items():
        
        arquivo.write(f"Camera na esquina [{camera}] monitora as seguinte(s) rua(s):\n")

        for rua in ruas:

            arquivo.write(f'- {rua}\n')

        arquivo.write('\n')


    


    
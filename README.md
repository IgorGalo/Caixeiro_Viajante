# Caixeiro Viajante

Implementação de um Algoritmo Genético para resolver o **Problema do Caixeiro Viajante**.

## O Problema do Caixeiro Viajante

Dado um conjunto de cidades e as distâncias entre cada par delas, o objetivo é encontrar a rota mais curta possível que visite todas as cidades exatamente uma vez e retorne à cidade de origem.


## Algoritmo Genético

Um Algoritmo Genético é uma metaheurística inspirada na evolução biológica e na seleção natural. Em vez de buscar a solução ótima de forma exaustiva, é trabalhado com uma **população** de soluções candidatas que evolui ao longo de sucessivas **gerações**, favorecendo indivíduos mais aptos e combinando suas características para gerar descendentes potencialmente melhores.

No contexto do nosso problema, cada indivíduo possuí um **dna**, o qual representa uma possível rota, codificada como uma permutação das cidades. A qualidade de cada indivíduo é medida pelo seu **fitness**, calculado como a distância total do circuito — quanto menor o fitness, melhor o indivíduo.

### Parâmetros e mecanismos utilizados

- **Seleção dos pais**: Feita por roleta ponderada pelo inverso do fitness (`1/fitness`), de forma que rotas mais curtas tenham maior probabilidade de serem escolhidas para reprodução.
- **Cruzamento**: Utiliza o método *Order Crossover* (OX), que preserva um trecho contíguo de um dos pais e completa o restante da rota com os genes do outro pai, na ordem em que aparecem, evitando cidades repetidas.
- **Taxa de cruzamento**: probabilidade de que dois pais selecionados de fato gerem filhos por cruzamento; caso contrário, os filhos são cópias diretas dos pais.
- **Mutação**: Para cada gene (cidade) da rota, existe uma probabilidade (taxa de mutação) de que ele seja trocado de posição com outro gene escolhido aleatoriamente, introduzindo diversidade genética e ajudando a evitar convergência prematura.
- **Elitismo**: Os melhores indivíduos de cada geração são copiados diretamente para a próxima geração sem sofrer cruzamento ou mutação, garantindo que boas soluções encontradas não se percam ao longo do processo evolutivo. Sempre dois indivíduos de uma população são escolhidos por meio do elitismo.
- **Tamanho da população**: Números de indivíduos de uma geração.
- **Número de gerações**: Quantidade de ciclos de seleção, cruzamento, mutação e elitismo pelos quais a população passa. Foi utilizado 500 gerações em todas as baterias de testes.

## Bateria de testes (experimento fatorial)

Para investigar como cada parâmetro influencia a qualidade das soluções encontradas, foi realizado um **experimento fatorial**, no qual os parâmetros do são variados sistematicamente de um teste para o outro, mantendo o mesmo grafo de entrada:

- **Tamanho da população**: 20, 50 e 100
- **Taxa de cruzamento**: 0.70, 0.85 e 0.95
- **Taxa de mutação**: 0.01, 0.05 e 0.10

Cada combinação possível entre esses três parâmetros (3 × 3 × 3 = 27 configurações) é executada **5 vezes**.

Para cada configuração são registrados o **melhor fitness** encontrado entre as 5 execuções e a **média de fitness** das 5 execuções. Ao final, também é registrada a melhor solução encontrada em toda a bateria de testes, junto com a rota correspondente e o tempo total de execução.

Os resultados são salvos no arquivo `tabela_de_resultados.txt`.

## Instruções de Execução

Para iniciar o algoritmo de Dijkstra:
1. É necessário ter Python 3 instalado.
2. Abra o seu terminal na pasta do projeto.
3. Digite o comando abaixo e pressione Enter:
   ```bash
   python3 AlgoritmoGenetico.py 
   ```

4. Escolha o número do grafo conforme solicitado pelo programa.

### Exemplo de Saída

```text
===== Grafos disponíveis =====
  [1] LAU15
  [2] SGB128
===============================
Escolha o grafo (1-2): 1

Grafo selecionado: LAU15

Pop=  20 | Cruzamento=0.70 | Mutacao=0.01 -> melhor=291.00 | media=303.00
Pop=  20 | Cruzamento=0.70 | Mutacao=0.05 -> melhor=291.00 | media=318.40
Pop=  20 | Cruzamento=0.70 | Mutacao=0.10 -> melhor=291.00 | media=300.20
Pop=  20 | Cruzamento=0.85 | Mutacao=0.01 -> melhor=291.00 | media=297.40
Pop=  20 | Cruzamento=0.85 | Mutacao=0.05 -> melhor=291.00 | media=309.40
Pop=  20 | Cruzamento=0.85 | Mutacao=0.10 -> melhor=291.00 | media=330.00
Pop=  20 | Cruzamento=0.95 | Mutacao=0.01 -> melhor=291.00 | media=297.40
Pop=  20 | Cruzamento=0.95 | Mutacao=0.05 -> melhor=291.00 | media=317.80
Pop=  20 | Cruzamento=0.95 | Mutacao=0.10 -> melhor=291.00 | media=299.80
Pop=  50 | Cruzamento=0.70 | Mutacao=0.01 -> melhor=291.00 | media=297.00
Pop=  50 | Cruzamento=0.70 | Mutacao=0.05 -> melhor=291.00 | media=309.40
Pop=  50 | Cruzamento=0.70 | Mutacao=0.10 -> melhor=291.00 | media=320.40
Pop=  50 | Cruzamento=0.85 | Mutacao=0.01 -> melhor=291.00 | media=303.40
Pop=  50 | Cruzamento=0.85 | Mutacao=0.05 -> melhor=291.00 | media=314.80
Pop=  50 | Cruzamento=0.85 | Mutacao=0.10 -> melhor=291.00 | media=304.60
Pop=  50 | Cruzamento=0.95 | Mutacao=0.01 -> melhor=291.00 | media=304.20
Pop=  50 | Cruzamento=0.95 | Mutacao=0.05 -> melhor=313.00 | media=334.40
Pop=  50 | Cruzamento=0.95 | Mutacao=0.10 -> melhor=291.00 | media=299.80
Pop= 100 | Cruzamento=0.70 | Mutacao=0.01 -> melhor=291.00 | media=291.00
Pop= 100 | Cruzamento=0.70 | Mutacao=0.05 -> melhor=291.00 | media=300.20
Pop= 100 | Cruzamento=0.70 | Mutacao=0.10 -> melhor=291.00 | media=323.20
Pop= 100 | Cruzamento=0.85 | Mutacao=0.01 -> melhor=291.00 | media=291.00
Pop= 100 | Cruzamento=0.85 | Mutacao=0.05 -> melhor=291.00 | media=309.20
Pop= 100 | Cruzamento=0.85 | Mutacao=0.10 -> melhor=291.00 | media=312.20
Pop= 100 | Cruzamento=0.95 | Mutacao=0.01 -> melhor=291.00 | media=299.00
Pop= 100 | Cruzamento=0.95 | Mutacao=0.05 -> melhor=291.00 | media=308.40
Pop= 100 | Cruzamento=0.95 | Mutacao=0.10 -> melhor=299.00 | media=325.40

Melhor solução encontrada: 291.00
Rota: [13, 11, 2, 6, 4, 8, 14, 1, 12, 0, 10, 3, 5, 7, 9]
Tempo total: 0 minuto(s) e 21 segundo(s)
```
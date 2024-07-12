import random

PERIODOS = 5
PROFESSORES = 12
DISCIPLINAS = 25
DIAS = 5
HORARIOS_POR_DIA = 2

# criar um indivíduo aleatório
def criar_individuo():
    return [[random.randint(0, DISCIPLINAS-1) for _ in range(HORARIOS_POR_DIA)] for _ in range(DIAS * PERIODOS)]

# criar uma população inicial
def criar_populacao(tamanho):
    return [criar_individuo() for _ in range(tamanho)]

# avaliar um indivíduo (contar choques de horários)
def avaliar_individuo(individuo):
    choques = 0
    for dia in range(DIAS):
        horarios = []
        for periodo in range(PERIODOS):
            horarios.extend(individuo[dia * PERIODOS + periodo])
        choques += len(horarios) - len(set(horarios))
    return choques

# selecionar os indivíduos (seleção aleatória com uma chance maior para os melhores)
def selecionar(populacao):
    total_fitness = sum([1 / (1 + avaliar_individuo(ind)) for ind in populacao])
    selecao_prob = [(1 / (1 + avaliar_individuo(ind))) / total_fitness for ind in populacao]
    return populacao[random.choices(range(len(populacao)), weights=selecao_prob, k=1)[0]]

# cruzar dois indivíduos
def cruzar(individuo1, individuo2, num_cortes):
    pontos_de_corte = sorted(random.sample(range(1, DIAS * PERIODOS * HORARIOS_POR_DIA), num_cortes))
    filho1, filho2 = [], []
    for i in range(num_cortes + 1):
        if i % 2 == 0:
            filho1.extend(individuo1[pontos_de_corte[i-1] if i > 0 else 0:pontos_de_corte[i] if i < num_cortes else None])
            filho2.extend(individuo2[pontos_de_corte[i-1] if i > 0 else 0:pontos_de_corte[i] if i < num_cortes else None])
        else:
            filho1.extend(individuo2[pontos_de_corte[i-1] if i > 0 else 0:pontos_de_corte[i] if i < num_cortes else None])
            filho2.extend(individuo1[pontos_de_corte[i-1] if i > 0 else 0:pontos_de_corte[i] if i < num_cortes else None])
    return filho1, filho2

# mutar um indivíduo
def mutar(individuo, prob_mutacao):
    for dia in range(DIAS * PERIODOS):
        if random.random() < prob_mutacao:
            individuo[dia] = [random.randint(0, DISCIPLINAS-1) for _ in range(HORARIOS_POR_DIA)]
    return individuo

# main
def algoritmo_genetico(tamanho_populacao, max_geracoes, prob_cruzamento, prob_mutacao, num_cortes):
    populacao = criar_populacao(tamanho_populacao)
    melhor_individuo = min(populacao, key=lambda x: avaliar_individuo(x))
    melhor_nota = avaliar_individuo(melhor_individuo)
    
    for geracao in range(max_geracoes):
        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecionar(populacao)
            pai2 = selecionar(populacao)
            if random.random() < prob_cruzamento:
                filho1, filho2 = cruzar(pai1, pai2, num_cortes)
            else:
                filho1, filho2 = pai1, pai2
            nova_populacao.append(mutar(filho1, prob_mutacao))
            if len(nova_populacao) < tamanho_populacao:
                nova_populacao.append(mutar(filho2, prob_mutacao))
        populacao = nova_populacao
        melhor_da_geracao = min(populacao, key=lambda x: avaliar_individuo(x))
        nota_melhor_da_geracao = avaliar_individuo(melhor_da_geracao)
        if nota_melhor_da_geracao < melhor_nota:
            melhor_individuo = melhor_da_geracao
            melhor_nota = nota_melhor_da_geracao
        print(f"Geração {geracao+1}: Melhor Nota = {melhor_nota}")
    
    return melhor_individuo, melhor_nota

tamanho_populacao = 100
max_geracoes = 50
prob_cruzamento = 0.9 
prob_mutacao = 0.3    
num_cortes = 2     

melhor_individuo, melhor_nota = algoritmo_genetico(tamanho_populacao, max_geracoes, prob_cruzamento, prob_mutacao, num_cortes)
print()
print("Melhor Geração:", melhor_individuo)
print()
print("Nota da Melhor Geração:", melhor_nota)
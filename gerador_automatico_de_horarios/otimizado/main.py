import random
from deap import base, creator, tools, algorithms

NUM_PERIODOS = 5
NUM_PROFESSORES = 12
NUM_DISCIPLINAS = 25
DIAS_DA_SEMANA = 5
HORARIOS_POR_DIA = 2

def avaliar(individuo):
    conflitos = 0
    for dia in range(DIAS_DA_SEMANA):
        for periodo in range(NUM_PERIODOS):
            horarios = individuo[dia][periodo]
            professores = [horario[0] for horario in horarios]
            disciplinas = [horario[1] for horario in horarios]
            if len(professores) != len(set(professores)):
                conflitos += 1 
            if len(disciplinas) != len(set(disciplinas)):
                conflitos += 1  
    return conflitos,

def criar_individuo():
    individuo = []
    for _ in range(DIAS_DA_SEMANA):
        dia = []
        for _ in range(NUM_PERIODOS):
            periodo = []
            for _ in range(HORARIOS_POR_DIA):
                professor = random.randint(0, NUM_PROFESSORES - 1)
                disciplina = random.randint(0, NUM_DISCIPLINAS - 1)
                periodo.append((professor, disciplina))
            dia.append(periodo)
        individuo.append(dia)
    return individuo

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individuo", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individuo", tools.initIterate, creator.Individuo, criar_individuo)
toolbox.register("populacao", tools.initRepeat, list, toolbox.individuo)
toolbox.register("evaluate", avaliar)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main(tam_populacao, max_geracoes, prob_cruzamento, prob_mutacao, num_cortes):
    populacao = toolbox.populacao(n=tam_populacao)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", min)
    stats.register("avg", lambda pop: sum(fit[0] for fit in pop) / len(pop))
    
    for ind in populacao:
        ind.fitness.values = toolbox.evaluate(ind)
    
    algorithms.eaSimple(populacao, toolbox, cxpb=prob_cruzamento, mutpb=prob_mutacao, ngen=max_geracoes, 
                        stats=stats, halloffame=hof, verbose=True)
    
    melhor_individuo = hof[0]
    melhor_nota = melhor_individuo.fitness.values[0]
    
    return melhor_individuo, melhor_nota

tam_populacao = 100
max_geracoes = 50
prob_cruzamento = 0.7
prob_mutacao = 0.2
num_cortes = 2

melhor_individuo, melhor_nota = main(tam_populacao, max_geracoes, prob_cruzamento, prob_mutacao, num_cortes)
print()
print("Melhor horário encontrado:", melhor_individuo)
print()
print("Nota do melhor horário:", melhor_nota)
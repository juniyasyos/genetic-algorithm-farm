# === threaded_main.py ===

import threading
from deap import base, creator, tools
from config import *
from utils import generate_individual, custom_mate, custom_mutate, is_feasible, repair, summary
from domain_logic import evaluate
import random

def run_ga(thread_name, ngen):
    print(f"🧵 Mulai {thread_name} dengan {ngen} generasi")

    creator.create(f"FitnessMax_{thread_name}", base.Fitness, weights=(1.0,))
    creator.create(f"Individual_{thread_name}", list, fitness=creator.__getattribute__(f"FitnessMax_{thread_name}"))

    toolbox = base.Toolbox()
    toolbox.register("individual", generate_individual, creator.__getattribute__(f"Individual_{thread_name}"))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", custom_mate)
    toolbox.register("mutate", custom_mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=200)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda fits: sum(f[0] for f in fits) / len(fits))
    stats.register("min", lambda fits: min(f[0] for f in fits))
    stats.register("max", lambda fits: max(f[0] for f in fits))

    # Evaluasi awal
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for gen in range(1, ngen + 1):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for c1, c2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:
                toolbox.mate(c1, c2)
                del c1.fitness.values, c2.fitness.values

        for mutant in offspring:
            if random.random() < 0.3:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid))
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring
        hof.update(pop)

        # if gen % 100 == 0 or gen == ngen:
        #     print(f"{thread_name} - Gen {gen}: {stats.compile(pop)}")

    feasible = [ind for ind in hof if is_feasible(ind)]
    if feasible:
        best = repair(feasible[0])
        toolbox.evaluate(best)
        print(f"✅ {thread_name} Selesai: Solusi feasible ditemukan.")
        summary(best)
    else:
        print(f"❌ {thread_name} Selesai: Tidak ada solusi feasible.")
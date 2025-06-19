# === threaded_main.py ===

import threading
from deap import base, creator, tools
from utils import generate_individual, custom_mate, custom_mutate, is_feasible, repair, summary
from domain_logic import make_evaluator
import random


def run_ga(
    thread_name,
    ngen,
    *,
    pop_size=200,
    mate_prob=0.5,
    mutate_prob=0.3,
    tourn_size=3,
    individual_bounds=None,
    kandang_config=None,
    biaya_config=None,
    env_config=None,
    min_profit_target=0,
    max_budget=1e9
):
    """
    Menjalankan algoritma genetik untuk satu thread dengan konfigurasi tertentu.

    Parameters:
    - thread_name: Nama thread
    - ngen: Jumlah generasi
    - pop_size: Ukuran populasi
    - mate_prob: Probabilitas crossover
    - mutate_prob: Probabilitas mutasi
    - tourn_size: Ukuran turnamen seleksi
    - individual_bounds: Batasan tiap parameter individu
    - kandang_config, biaya_config, env_config: Dict berisi parameter GA
    - min_profit_target: Target minimal pendapatan
    - max_budget: Anggaran maksimum
    """

    print(f"🧵 Mulai {thread_name} dengan {ngen} generasi")

    # Siapkan config evaluator spesifik untuk thread ini
    config = {
        "tipe_kandang": kandang_config["tipe_kandang"],
        "luas_lahan": kandang_config["luas_lahan"],
        "kandang_config": kandang_config,

        "harga_pakan": biaya_config["harga_pakan"],
        "biaya_vaksin": biaya_config["biaya_vaksin"],
        "gaji_tk": biaya_config["gaji_tk"],
        "biaya_lain": biaya_config["biaya_lain"],

        "hari_siklus": env_config["hari_siklus"],
        "siklus_bulan": env_config["siklus_bulan"],
        "harga_telur": env_config["harga_telur"],
        "maks_ayam_per_pekerja": env_config["maks_ayam_per_pekerja"],
        "konversi": env_config["konversi"],

        "min_pendapatan": min_profit_target,
        "budget_maks": max_budget
    }

    evaluate = make_evaluator(config)


    creator.create(f"FitnessMax_{thread_name}", base.Fitness, weights=(1.0,))
    creator.create(
        f"Individual_{thread_name}", list, fitness=creator.__getattribute__(f"FitnessMax_{thread_name}")
    )

    toolbox = base.Toolbox()
    toolbox.register("individual", generate_individual, creator.__getattribute__(f"Individual_{thread_name}"), individual_bounds)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", custom_mate, bounds=individual_bounds)
    toolbox.register("mutate", custom_mutate, bounds=individual_bounds)
    toolbox.register("select", tools.selTournament, tournsize=tourn_size)

    pop = toolbox.population(n=pop_size)
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
            if random.random() < mate_prob:
                toolbox.mate(c1, c2)
                del c1.fitness.values, c2.fitness.values

        for mutant in offspring:
            if random.random() < mutate_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid))
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring
        hof.update(pop)

    feasible = [ind for ind in hof if is_feasible(ind)]
    if feasible:
        best = repair(feasible[0], individual_bounds)
        toolbox.evaluate(best)
        print(f"✅ {thread_name} Selesai: Solusi feasible ditemukan.")
        summary(best, env_config, biaya_config, kandang_config)

    else:
        print(f"❌ {thread_name} Selesai: Tidak ada solusi feasible.")

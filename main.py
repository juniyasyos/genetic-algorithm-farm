from threaded_main import run_ga
import threading

# Konfigurasi tetap
individual_bounds = {
    "N": (1000, 5000),
    "F": (0.9, 1.2),
    "L": (10, 16),
    "V": (0.8, 1.0),
    "T": (1, 20),
    "C": (50, 100),
}

kandang_config = {
    "tipe_kandang": "baterai",
    "luas_lahan": 500,
    "baterai": {
        "kapasitas_maks_per_m2": 8
    }
}

biaya_config = {
    "harga_pakan": 7500,
    "biaya_vaksin": 300,
    "gaji_tk": 2000000,
    "biaya_lain": 1000000
}

env_config = {
    "harga_telur": 27000,
    "hari_siklus": 150,
    "siklus_bulan": 5,
    "maks_ayam_per_pekerja": 400,
    "konversi": 1.8
}

min_profit_target = 10_000_000
max_budget = 100_000_000

# def main():
#     thread_configs = [
#         # Thread awal
#         ("thr-1", 1000, 100, 0.5, 0.2, 3),
#         ("thr-2", 1000, 100, 0.5, 0.2, 3),
#         ("thr-3", 1000, 100, 0.5, 0.2, 3),

#         # 4 Thread tambahan
#         ("thr-4", 1000, 150, 0.6, 0.3, 4),
#         ("thr-5", 1000, 80, 0.4, 0.25, 5),
#         ("thr-6", 1000, 200, 0.7, 0.1, 2),
#         ("thr-7", 1000, 120, 0.55, 0.15, 3),
#     ]

#     threads = []

#     for name, gens, pop_size, mate_prob, mutate_prob, tourn_size in thread_configs:
#         t = threading.Thread(
#             target=run_ga,
#             args=(name, gens),
#             kwargs={
#                 "pop_size": pop_size,
#                 "mate_prob": mate_prob,
#                 "mutate_prob": mutate_prob,
#                 "tourn_size": tourn_size,
#                 "individual_bounds": individual_bounds,
#                 "kandang_config": kandang_config,
#                 "biaya_config": biaya_config,
#                 "env_config": env_config,
#                 "min_profit_target": min_profit_target,
#                 "max_budget": max_budget,
#             }
#         )
#         threads.append(t)
#         t.start()

#     for t in threads:
#         t.join()


def main():
    thread_configs = [
        # Kasus normal (baseline)
        ("normal-1", 1000, 100, 0.5, 0.2, 3),

        # 🔴 Kasus batas kapasitas kandang (ayam mendekati 5000, lahan tetap 500m²)
        ("overload-kandang", 1000, 100, 0.5, 0.2, 3),  # diharapkan gagal/terbatas

        # 🟡 Kasus jumlah ayam minimum (testing ROI tetap layak atau tidak)
        ("min-ayam", 1000, 80, 0.4, 0.25, 4),

        # 🟠 Kasus ayam maksimal dengan jumlah tenaga kerja yang terbatas (stress test pekerja)
        ("overload-tk", 1000, 120, 0.6, 0.3, 3),

        # 🔵 Kombinasi parameter ekstrem tapi masih feasible secara teori
        ("ekstrem-optimal", 1000, 150, 0.8, 0.1, 2),

        # ⚫ Biaya operasional mendekati batas maksimum budget
        ("limit-budget", 1000, 200, 0.7, 0.2, 2),

        # 🟢 Test probabilitas mutasi tinggi
        ("mutasi-tinggi", 1000, 120, 0.5, 0.6, 3),

        # 🟣 Test probabilitas crossover tinggi
        ("crossover-tinggi", 1000, 120, 0.9, 0.1, 3),
    ]

    threads = []

    for name, gens, pop_size, mate_prob, mutate_prob, tourn_size in thread_configs:
        t = threading.Thread(
            target=run_ga,
            args=(name, gens),
            kwargs={
                "pop_size": pop_size,
                "mate_prob": mate_prob,
                "mutate_prob": mutate_prob,
                "tourn_size": tourn_size,
                "individual_bounds": individual_bounds,
                "kandang_config": kandang_config,
                "biaya_config": biaya_config,
                "env_config": env_config,
                "min_profit_target": min_profit_target,
                "max_budget": max_budget,
            }
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()

import random
from deap import tools
from math import isfinite

# Fungsi untuk membuat individual baru
def generate_individual(individual_class, bounds):
    keys = list(bounds.keys())
    values = []
    for key in keys:
        low, high = bounds[key]
        if isinstance(low, float):
            values.append(round(random.uniform(low, high), 2))
        else:
            values.append(random.randint(low, high))
    return individual_class(values)

# Fungsi perbaikan individu agar tetap dalam batas
def repair(ind, bounds):
    keys = list(bounds.keys())
    for i, key in enumerate(keys):
        low, high = bounds[key]
        if isinstance(low, float):
            ind[i] = float(min(max(ind[i], low), high))
        else:
            ind[i] = int(min(max(ind[i], low), high))
    return ind

# Fungsi crossover khusus
def custom_mate(ind1, ind2, bounds):
    tools.cxBlend(ind1, ind2, alpha=0.5)
    return repair(ind1, bounds), repair(ind2, bounds)

# Fungsi mutasi khusus
def custom_mutate(ind, bounds):
    keys = list(bounds.keys())
    for i, key in enumerate(keys):
        if random.random() < 0.2:
            low, high = bounds[key]
            if isinstance(low, float):
                ind[i] = round(random.uniform(low, high), 2)
            else:
                ind[i] = random.randint(low, high)
    return repair(ind, bounds),

# Hitung kapasitas kandang
def hitung_kapasitas_kandang_tetap(tipe_kandang, luas_lahan, kandang_config):
    data = kandang_config[tipe_kandang]
    kapasitas_total = luas_lahan * data["kapasitas_maks_per_m2"]
    return kapasitas_total


# Evaluasi kelayakan
def is_feasible(ind):
    e = ind.extra
    return (
        e["kapasitas_ok"]
        and e["pekerja_ok"]
        and e["budget_ok"]
        and e["pendapatan"] > 0
        and e["profit"] > 0
    )

# Hitung penalti vaksinasi
def penalti_vaksin(V):
    if V < 2:
        return 0.3
    elif 2 <= V <= 3:
        return 0.0
    elif 4 <= V <= 5:
        return 0.05
    else:
        return 0.1

# Validasi angka
def is_angka_valid(x):
    return isinstance(x, (int, float)) and isfinite(x) and x > 0

# Ringkasan hasil
def summary(ind, env_config, biaya_config, kandang_config):
    N, F, L, V, T, C = ind
    hasil = ind.extra

    print("\n" + "="*60)
    print("📊  RINGKASAN STRATEGI PRODUKSI TELUR AYAM PETELUR")
    print("="*60)

    print("\n🔧 PARAMETER OPERASIONAL")
    print(f"- Jumlah Ayam            : {N:,} ekor")
    print(f"- Pakan per Ekor per Hari: {F:.2f} gram")
    print(f"- Jam Cahaya per Hari    : {L:.2f} jam")
    print(f"- Frekuensi Vaksin       : {V} kali/tahun")
    print(f"- Ventilasi              : {C} (skala 0–100)")
    print(f"- Tenaga Kerja           : {T} orang")
    print(f"- Tipe Kandang           : {kandang_config['tipe_kandang'].capitalize()}")
    print(f"- Luas Lahan Digunakan   : {kandang_config['luas_lahan']} m²")
    print(f"- Penalti Vaksin         : {hasil.get('penalti_vaksin', 0):.2%}")

    print("\n💰 RINGKASAN EKONOMI")
    print(f"- Total Pendapatan       : Rp {hasil['pendapatan']:,.0f}")
    print(f"- Total Biaya Operasional: Rp {hasil['biaya']:,.0f}")
    print(f"- Keuntungan Bersih      : Rp {hasil['profit']:,.0f}")

    if is_angka_valid(hasil.get('pendapatan')):
        print(f"- Profit Margin          : {hasil['profit'] / hasil['pendapatan']:.2%}")
    else:
        print(f"- Profit Margin          : N/A")

    if is_angka_valid(hasil.get('biaya')):
        print(f"- ROI (Pendapatan/Biaya) : {hasil['pendapatan'] / hasil['biaya']:.2f}x")
    else:
        print(f"- ROI (Pendapatan/Biaya) : N/A")

    print("\n📈 EVALUASI KESESUAIAN")
    print(f"- Kapasitas Kandang Cukup: {'✅' if hasil.get('kapasitas_ok') else '❌'}")
    print(f"- Jumlah Tenaga Kerja OK : {'✅' if hasil.get('pekerja_ok') else '❌'}")
    print(f"- Biaya Sesuai Budget    : {'✅' if hasil.get('budget_ok') else '❌'}")

    print("\n📌 CATATAN TAMBAHAN")
    print(f"- Durasi Produksi        : {env_config['hari_siklus']} hari ({env_config['siklus_bulan']} bulan)")
    print(f"- Harga Pakan per Kg     : Rp {biaya_config['harga_pakan']:,}")
    print(f"- Harga Telur per Kg     : Rp {env_config['harga_telur']:,}")
    print(f"- Biaya Vaksin per Ekor  : Rp {biaya_config['biaya_vaksin']:,} x {V} = Rp {biaya_config['biaya_vaksin']*V:,.0f}")
    print(f"- Gaji Pekerja/Bulan     : Rp {biaya_config['gaji_tk']:,}")
    print(f"- Biaya Operasional Lain : Rp {biaya_config['biaya_lain']:,}/bulan x {env_config['siklus_bulan']} = Rp {biaya_config['biaya_lain'] * env_config['siklus_bulan']:,.0f}")
    print("="*60)

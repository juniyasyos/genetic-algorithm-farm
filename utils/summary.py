import random
from deap import tools
from config import *
from math import isfinite


def generate_individual(creator):
    return creator.Individual([
        random.randint(*BOUNDS["N"]),
        random.uniform(*BOUNDS["F"]),
        random.uniform(*BOUNDS["L"]),
        random.randint(*BOUNDS["V"]),
        random.randint(*BOUNDS["T"]),
        random.randint(*BOUNDS["C"]),
    ])

def repair(ind):
    keys = list(BOUNDS.keys())
    for i, key in enumerate(keys):
        low, high = BOUNDS[key]
        if isinstance(low, float):
            ind[i] = float(min(max(ind[i], low), high))
        else:
            ind[i] = int(min(max(ind[i], low), high))
    return ind

def custom_mate(ind1, ind2):
    tools.cxBlend(ind1, ind2, alpha=0.5)
    return repair(ind1), repair(ind2)

def custom_mutate(ind):
    keys = list(BOUNDS.keys())
    for i, key in enumerate(keys):
        if random.random() < 0.2:
            low, high = BOUNDS[key]
            if isinstance(low, float):
                ind[i] = random.uniform(low, high)
            else:
                ind[i] = random.randint(low, high)
    return repair(ind),

def hitung_kapasitas_kandang_tetap(tipe_kandang, luas_lahan):
    data = KANDANG[tipe_kandang]
    kapasitas_total = luas_lahan * data["kapasitas_maks_per_m2"]
    return kapasitas_total

def is_feasible(ind):
    N, _, _, _, T, _ = ind
    kapasitas_total = hitung_kapasitas_kandang_tetap(TIPE_KANDANG_TETAP, LUAS_LAHAN_TOTAL)
    cukup_kandang = N <= kapasitas_total
    cukup_pekerja = T >= (N // MAKS_AYAM_PER_PEKERJA)
    return cukup_kandang and cukup_pekerja

def penalti_vaksin(V):
    if V < 2:
        return 0.3  # Risiko terlalu besar
    elif 2 <= V <= 3:
        return 0.0  # Ideal
    elif 4 <= V <= 5:
        return 0.05  # Aman tapi tidak efisien
    else:
        return 0.1  # Stres & pemborosan

def is_angka_valid(x):
    return isinstance(x, (int, float)) and isfinite(x) and x > 0

def summary(ind, information_optional=False):
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
    print(f"- Tipe Kandang           : {TIPE_KANDANG_TETAP.capitalize()}")
    print(f"- Luas Lahan Digunakan   : {LUAS_LAHAN_TOTAL} m²")
    print(f"- Penalti Vaksin         : {hasil.get('penalti_vaksin', 0):.2%}")

    print("\n💰 RINGKASAN EKONOMI")
    print(f"- Total Pendapatan       : Rp {hasil['pendapatan']:,.0f}")
    print(f"- Total Biaya Operasional: Rp {hasil['biaya']:,.0f}")
    print(f"- Keuntungan Bersih      : Rp {hasil['profit']:,.0f}")

    # Cegah ZeroDivisionError + nilai aneh (None, NaN, string, etc)
    if is_angka_valid(hasil.get('pendapatan')):
        print(f"- Profit Margin          : {hasil['profit'] / hasil['pendapatan']:.2%}")
    else:
        print(f"- Profit Margin          : N/A (Pendapatan tidak valid)")

    if is_angka_valid(hasil.get('biaya')):
        print(f"- ROI (Pendapatan/Biaya) : {hasil['pendapatan'] / hasil['biaya']:.2f}x")
    else:
        print(f"- ROI (Pendapatan/Biaya) : N/A (Biaya tidak valid)")


    print("\n📈 EVALUASI KESESUAIAN")
    print(f"- Kapasitas Kandang Cukup: {'✅' if hasil.get('kapasitas_ok') else '❌'}")
    print(f"- Jumlah Tenaga Kerja OK : {'✅' if hasil.get('pekerja_ok') else '❌'}")
    print(f"- Biaya Sesuai Budget    : {'✅' if hasil.get('budget_ok') else '❌'}")

    if (information_optional):
        print("\n📌 CATATAN TAMBAHAN")
        print(f"- Durasi Produksi        : {DAYS} hari ({SICLUS_BULAN} bulan)")
        print(f"- Harga Pakan per Kg     : Rp {PPAKAN:,}")
        print(f"- Harga Telur per Kg     : Rp {PTELUR:,}")
        print(f"- Biaya Vaksin per Ekor  : Rp {BIAYA_VAKSIN:,} x {V} = Rp {BIAYA_VAKSIN*V:,.0f}")
        print(f"- Gaji Pekerja/Bulan     : Rp {GAJI_TK:,}")
        print(f"- Biaya Operasional Lain : Rp {BIAYA_LAIN:,}/bulan x {SICLUS_BULAN} = Rp {BIAYA_LAIN*SICLUS_BULAN:,.0f}")

    print("="*60)

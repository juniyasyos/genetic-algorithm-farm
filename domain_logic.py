# === domain_logic.py ===

from config import *
from math import isfinite
from utils import hitung_kapasitas_kandang_tetap, penalti_vaksin

# Validasi kapasitas ayam dalam kandang
def is_valid_kapasitas(N, kapasitas_total):
    return N <= kapasitas_total

# Validasi jumlah pekerja terhadap jumlah ayam
def is_valid_pekerja(N, T):
    return T >= (N // MAKS_AYAM_PER_PEKERJA)

# Hitung seluruh komponen biaya
def hitung_biaya(N, F, V, T):
    biaya_pakan = N * F * DAYS * PPAKAN / 1000
    biaya_vaksin = V * BIAYA_VAKSIN * N
    biaya_tk = T * GAJI_TK * SICLUS_BULAN
    total = biaya_pakan + biaya_vaksin + biaya_tk + BIAYA_LAIN
    return total, biaya_pakan, biaya_vaksin, biaya_tk

# Hitung efisiensi cahaya dan ventilasi
def hitung_efisiensi(L, C):
    if L < 10 or L > 16:
        return 0, 0
    ef_cahaya = max(0.0, min((L - 12) / 4, 1.0)) 
    ef_ventilasi = max(0.0, min(C / 100, 1.0))
    return ef_cahaya, ef_ventilasi


# Hitung penalti jika kepadatan melebihi kapasitas
def hitung_penalti_kepadatan(N, kapasitas_total):
    kepadatan = N / kapasitas_total
    return max(0.3, 1.2 - kepadatan) if kepadatan > 1.0 else 1.0

# Buat ringkasan hasil evaluasi individu
def hasil_dict(pendapatan, total_biaya, profit, valid=True, kapasitas=True, pekerja=True, budget=True, p_vaksin=0, **kwargs):
    return {
        "pendapatan": pendapatan,
        "biaya": total_biaya,
        "profit": profit,
        "kapasitas_ok": kapasitas,
        "pekerja_ok": pekerja,
        "budget_ok": budget,
        "penalti_vaksin": p_vaksin,
        **kwargs
    }

# Fungsi evaluasi utama untuk GA
def evaluate(ind):
    N, F, L, V, T, C = ind
    kapasitas_total = hitung_kapasitas_kandang_tetap(TIPE_KANDANG_TETAP, LUAS_LAHAN_TOTAL)

    valid_kapasitas = is_valid_kapasitas(N, kapasitas_total)
    valid_pekerja = is_valid_pekerja(N, T)
    total_biaya, *_ = hitung_biaya(N, F, V, T)

    # Hitung efisiensi dan penalti
    ef_cahaya, ef_ventilasi = hitung_efisiensi(L, C)
    penalti_kepadatan = hitung_penalti_kepadatan(N, kapasitas_total)
    p_vaksin = penalti_vaksin(V)

    # Batasi nilai minimum efisiensi agar tidak 0
    ef_cahaya = max(ef_cahaya, 0.5)
    ef_ventilasi = max(ef_ventilasi, 0.5)
    penalti_kepadatan = max(penalti_kepadatan, 0.5)
    p_vaksin = min(max(p_vaksin, 0), 0.5)  # jaga di antara 0–0.5

    # Hitung produksi & pendapatan
    konversi = KONVERSI * ef_cahaya * ef_ventilasi * penalti_kepadatan * (1 - p_vaksin)
    konversi = max(konversi, 1e-6)  # Hindari 0
    produksi_telur = N * F * konversi
    pendapatan = produksi_telur * DAYS * PTELUR
    profit = pendapatan - total_biaya

    # Penalti progresif
    penalti = 1.0
    if not valid_kapasitas:
        penalti *= 0.5
    if not valid_pekerja:
        penalti *= 0.5
    if total_biaya > BUDGET_MAKS:
        penalti *= 0.3
    if pendapatan < MIN_PENDAPATAN:
        penalti *= 0.5
    if ef_cahaya < 0.6 or ef_ventilasi < 0.6:
        penalti *= 0.7

    # Apply penalti
    profit *= penalti

    # Jaga agar tidak meledak
    if not isfinite(profit) or profit <= 0 or pendapatan <= 0:
        profit = -1e6  # Penalti ringan masih bisa ikut crossover

    # Simpan informasi tambahan
    ind.extra = hasil_dict(
        pendapatan, total_biaya, profit,
        kapasitas=valid_kapasitas,
        pekerja=valid_pekerja,
        budget=(total_biaya <= BUDGET_MAKS),
        p_vaksin=p_vaksin,
        penalti=penalti
    )

    # Debug ringan (opsional)
    # if profit > 0:
    #     print(f"[GA] Gagal: N={N}, T={T}, F={F}, L={L}, V={V}, C={C}, profit={profit:.2f}, pendapatan={pendapatan:.2f}, penalti={penalti:.2f}")

    return (profit,)

# === domain_logic.py ===

from math import isfinite
from utils import hitung_kapasitas_kandang_tetap, penalti_vaksin

# Buat evaluator yang terisolasi untuk setiap thread
def make_evaluator(config):
    def is_valid_kapasitas(N, kapasitas_total):
        return N <= kapasitas_total

    def is_valid_pekerja(N, T):
        return T >= (N // config["maks_ayam_per_pekerja"])

    def hitung_biaya(N, F, V, T):
        biaya_pakan = N * F * config["hari_siklus"] * config["harga_pakan"] / 1000
        biaya_vaksin = V * config["biaya_vaksin"] * N
        biaya_tk = T * config["gaji_tk"] * config["siklus_bulan"]
        total = biaya_pakan + biaya_vaksin + biaya_tk + config["biaya_lain"]
        return total, biaya_pakan, biaya_vaksin, biaya_tk

    def hitung_efisiensi(L, C):
        if L < 10 or L > 16:
            return 0, 0
        ef_cahaya = max(0.0, min((L - 12) / 4, 1.0)) 
        ef_ventilasi = max(0.0, min(C / 100, 1.0))
        return ef_cahaya, ef_ventilasi

    def hitung_penalti_kepadatan(N, kapasitas_total):
        kepadatan = N / kapasitas_total
        return max(0.3, 1.2 - kepadatan) if kepadatan > 1.0 else 1.0

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

    def evaluate(ind):
        N, F, L, V, T, C = ind
        kapasitas_total = hitung_kapasitas_kandang_tetap(
            config["tipe_kandang"],
            config["luas_lahan"],
            config["kandang_config"]
        )


        valid_kapasitas = is_valid_kapasitas(N, kapasitas_total)
        valid_pekerja = is_valid_pekerja(N, T)
        total_biaya, *_ = hitung_biaya(N, F, V, T)

        ef_cahaya, ef_ventilasi = hitung_efisiensi(L, C)
        penalti_kepadatan = hitung_penalti_kepadatan(N, kapasitas_total)
        p_vaksin = penalti_vaksin(V)

        ef_cahaya = max(ef_cahaya, 0.5)
        ef_ventilasi = max(ef_ventilasi, 0.5)
        penalti_kepadatan = max(penalti_kepadatan, 0.5)
        p_vaksin = min(max(p_vaksin, 0), 0.5)

        konversi = config["konversi"] * ef_cahaya * ef_ventilasi * penalti_kepadatan * (1 - p_vaksin)
        konversi = max(konversi, 1e-6)
        produksi_telur = N * F * konversi
        pendapatan = produksi_telur * config["hari_siklus"] * config["harga_telur"]
        profit = pendapatan - total_biaya

        penalti = 1.0
        if not valid_kapasitas:
            penalti *= 0.5
        if not valid_pekerja:
            penalti *= 0.5
        if total_biaya > config["budget_maks"]:
            penalti *= 0.3
        if pendapatan < config["min_pendapatan"]:
            penalti *= 0.5
        if ef_cahaya < 0.6 or ef_ventilasi < 0.6:
            penalti *= 0.7

        profit *= penalti

        if not isfinite(profit) or profit <= 0 or pendapatan <= 0:
            profit = -1e6

        ind.extra = hasil_dict(
            pendapatan, total_biaya, profit,
            kapasitas=valid_kapasitas,
            pekerja=valid_pekerja,
            budget=(total_biaya <= config["budget_maks"]),
            p_vaksin=p_vaksin,
            penalti=penalti
        )

        return (profit,)
    
    return evaluate

# === config.py ===

# Umum
DAYS = 365                          # Lama produksi dalam hari
SICLUS_BULAN = 12                   # Durasi siklus dalam bulan
PPAKAN = 7500                       # Harga pakan per kg
PTELUR = 27000                      # Harga telur per kg
KONVERSI = 0.75 / 1000              # Konversi pakan ke telur (kg pakan per butir)
BIAYA_VAKSIN = 4000                # Biaya vaksin per ayam per siklus
GAJI_TK = 2_500_000                # Gaji pekerja per bulan
BIAYA_LAIN = 5_000_000             # Biaya operasional tambahan (bulanan)
BUDGET_MAKS = 4_500_000_000          # ❗ Naikkan agar feasible untuk ≥10.000 ayam
MAKS_AYAM_PER_PEKERJA = 500        # Kapasitas kerja maksimum per pekerja

MIN_PRODUKSI_TELUR = 100_000  # contoh ambang minimal produksi
MIN_PENDAPATAN = 50_000_000   # contoh minimum pendapatan

# Tipe Kandang
KANDANG = {
    "baterai": {
        "luas_per_kandang_m2": 15,
        "tinggi_m": 3,
        "kapasitas_ideal_per_m2": 7,
        "kapasitas_maks_per_m2": 9,
        "biaya_per_unit": 2_500_000
    },
    "postal": {
        "luas_per_kandang_m2": 25,
        "tinggi_m": 2.5,
        "kapasitas_ideal_per_m2": 10,
        "kapasitas_maks_per_m2": 12,
        "biaya_per_unit": 3_000_000
    }
}

TIPE_KANDANG_TETAP = "baterai"
LUAS_LAHAN_TOTAL = 2000  # ❗ Naikkan agar bisa tampung ≥10.000 ayam dengan kepadatan ideal

# Faktor penalti & kesejahteraan
PENALTI = {
    "ventilasi_min": 30,                     # jika < ini, penalti dimulai
    "ventilasi_max": 100,
    "penalty_produksi_ventilasi": 0.3,       # produksi bisa turun max 30%
    "penalty_produksi_kepadatan": 0.4,       # produksi bisa turun max 40%
    "penalty_kematian_kepadatan": 0.1        # max 10% ayam bisa mati karena stress
}

# Rentang Variabel (boundaries untuk GA)
BOUNDS = {
    "N": (8_000, 18_000),    # Jumlah ayam (kapasitas_maks = 2000 m2 * 9 ekor/m2 = 18.000 ayam)
    "F": (85, 110),           # Pakan per ekor per hari (gram) ❗ naikan batas bawah agar realistis
    "L": (14, 17),            # Jam cahaya ❗ optimalisasi produksi
    "V": (2, 4),              # Frekuensi vaksinasi per tahun ❗ ubah dari 1–6 jadi rentang realistis
    "T": (40, 70),            # Tenaga kerja ❗ disesuaikan dengan N minimal (20.000 / 500 = 40)
    "C": (50, 100),           # Ventilasi skala normal 0–100 ❗ ubah dari (100, 1000)
}

# Produksi telur per ayam berdasarkan usia (minggu), nilai ideal
PRODUKSI_TELUR_USIA = {
    0: 0.0,    # DOC (day old chick)
    6: 0.1,
    12: 0.5,
    18: 0.8,
    24: 0.95,
    30: 1.0,
    40: 0.9,
    52: 0.8
}

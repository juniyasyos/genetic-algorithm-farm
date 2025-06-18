# 🐣 Optimasi Produksi Telur Ayam Petelur dengan Algoritma Genetika

Proyek ini bertujuan untuk mencari strategi optimal dalam produksi telur ayam petelur dengan mempertimbangkan berbagai faktor teknis dan ekonomi, seperti jumlah ayam, pakan, vaksinasi, ventilasi, dan keterbatasan lahan serta anggaran.

---

## 🧠 Algoritma yang Digunakan

- **Algoritma Genetika (GA)** dengan strategi:

  - Seleksi: Tournament / Roulette
  - Crossover: Uniform / Two-point
  - Mutasi: Gaussian / Shuffle index

- Evaluasi berbasis:

  - Profitabilitas
  - Kelayakan lahan & kandang
  - Beban kerja tenaga kerja
  - Efisiensi cahaya, ventilasi, dan vaksinasi

---

## 📁 Struktur Proyek

```
genetic-algorithm-farm/
│
├── config.py              # Konfigurasi utama
├── domain_logic.py        # Fungsi evaluasi & perhitungan
├── genetic_engine.py      # GA setup (DEAP)
├── threaded_main.py       # Eksekusi threaded GA
├── utils.py               # Fungsi pendukung
└── README.md              # Dokumentasi
```

---

## 🧪 Cara Menjalankan

1. Clone repositori:

   ```bash
   git clone https://github.com/juniyasyos/genetic-algorithm-farm.git
   cd genetic-algorithm-farm
   ```

2. Jalankan virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Jalankan simulasi:

   ```bash
   python threaded_main.py
   ```

---

## 🚀 Ringkasan Hasil Akhir (Berbagai Kasus)

### ✅ Kasus 1 — *thr-1: Solusi feasible dalam 5.000 generasi*

🔧 PARAMETER OPERASIONAL
- Jumlah Ayam            : 10,659 ekor
- Pakan per Ekor per Hari: 110.00 gram
- Jam Cahaya per Hari    : 16.00 jam
- Frekuensi Vaksin       : 2 kali/tahun
- Ventilasi              : 100 (skala 0–100)
- Tenaga Kerja           : 40 orang
- Tipe Kandang           : Baterai
- Luas Lahan Digunakan   : 2000 m²
- Penalti Vaksin         : 0.00%

💰 RINGKASAN EKONOMI
- Total Pendapatan       : Rp 8,666,166,712
- Total Biaya Operasional: Rp 4,499,963,375
- Keuntungan Bersih      : Rp 4,166,203,338
- Profit Margin          : 48.07%
- ROI (Pendapatan/Biaya) : 1.93x

📈 EVALUASI KESESUAIAN
- Kapasitas Kandang Cukup: ✅
- Jumlah Tenaga Kerja OK : ✅
- Biaya Sesuai Budget    : ✅
---

### ✅ Kasus 2 — *thr-2: Solusi feasible dalam 10.000 generasi*

🔧 PARAMETER OPERASIONAL
- Jumlah Ayam            : 10,847 ekor
- Pakan per Ekor per Hari: 108.00 gram
- Jam Cahaya per Hari    : 16.00 jam
- Frekuensi Vaksin       : 2 kali/tahun
- Ventilasi              : 100 (skala 0–100)
- Tenaga Kerja           : 40 orang
- Tipe Kandang           : Baterai
- Luas Lahan Digunakan   : 2000 m²
- Penalti Vaksin         : 0.00%

💰 RINGKASAN EKONOMI
- Total Pendapatan       : Rp 8,658,671,985
- Total Biaya Operasional: Rp 4,498,691,550
- Keuntungan Bersih      : Rp 4,159,980,435
- Profit Margin          : 48.04%
- ROI (Pendapatan/Biaya) : 1.92x

📈 EVALUASI KESESUAIAN
- Kapasitas Kandang Cukup: ✅
- Jumlah Tenaga Kerja OK : ✅
- Biaya Sesuai Budget    : ✅
---

### ✅ Kasus 3 — *thr-3: Solusi feasible dalam 15.000 generasi*
============================================================
📊  RINGKASAN STRATEGI PRODUKSI TELUR AYAM PETELUR
============================================================

🔧 PARAMETER OPERASIONAL
- Jumlah Ayam            : 10,659 ekor
- Pakan per Ekor per Hari: 110.00 gram
- Jam Cahaya per Hari    : 16.00 jam
- Frekuensi Vaksin       : 2 kali/tahun
- Ventilasi              : 100 (skala 0–100)
- Tenaga Kerja           : 40 orang
- Tipe Kandang           : Baterai
- Luas Lahan Digunakan   : 2000 m²
- Penalti Vaksin         : 0.00%

💰 RINGKASAN EKONOMI
- Total Pendapatan       : Rp 8,666,166,712
- Total Biaya Operasional: Rp 4,499,963,375
- Keuntungan Bersih      : Rp 4,166,203,338
- Profit Margin          : 48.07%
- ROI (Pendapatan/Biaya) : 1.93x

📈 EVALUASI KESESUAIAN
- Kapasitas Kandang Cukup: ✅
- Jumlah Tenaga Kerja OK : ✅
- Biaya Sesuai Budget    : ✅
---

### 💡 Tips:

* Untuk **setiap generasi/case baru**, beri nama unik, seperti `thr-2`, `thr-3`, atau `case-A`, `case-B`.
* Gunakan format tabel agar perbandingan antar hasil lebih mudah dibaca.
* Jika ingin hasil ini dirender otomatis dari program, kamu bisa ekspor hasil dalam format `.md` atau `.json` dan generate README dari situ.

Kalau kamu mau, aku juga bisa bantu buat template Python untuk menulis hasil evaluasi ke file Markdown. Mau?


## 📌 Catatan Tambahan

- Kode ini dirancang fleksibel dan dapat diperluas untuk skenario lain seperti:

  - Tipe kandang yang berbeda
  - Harga dinamis atau musiman
  - Simulasi multi-tahun

---

## 🧑‍💻 Kontributor

- **Ahmad Ilyas** — _Junior Web & AI Developer_
- Proyek ini adalah bagian dari eksplorasi terhadap algoritma evolusioner dalam pertanian cerdas berbasis data.

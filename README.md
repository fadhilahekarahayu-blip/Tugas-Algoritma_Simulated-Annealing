# Simulated Annealing untuk Travelling Salesman Problem (TSP)

## Deskripsi
Program Python ini menerapkan algoritma Simulated Annealing untuk mencari rute kunjungan dengan total jarak terpendek. Studi kasus menggunakan satu Depot dan lima pelanggan (A, B, C, D, E).

Program mencakup:
- Tiga kasus uji dasar yang dapat diperiksa secara manual.
- Proses Simulated Annealing hingga 50 iterasi.
- Log keputusan kandidat diterima atau ditolak.
- Tabel hasil setiap iterasi.
- Grafik jarak saat ini dan jarak terbaik.
- Grafik penurunan suhu.
- Validasi hasil dengan pemeriksaan seluruh 120 kemungkinan urutan pelanggan.

## Struktur Folder

```text
simulated_annealing_tsp_github/
├── simulated_annealing_pengiriman.py
├── README.md
├── requirements.txt
└── .gitignore
```

Dua gambar grafik akan dibuat otomatis saat program dijalankan:
- `grafik_jarak.png`
- `grafik_suhu.png`

## Lingkungan dan Dependensi
- Python 3.9 atau lebih baru
- Matplotlib

Modul `math`, `random`, dan `itertools` sudah tersedia bersama Python.

Instal dependensi:

```bash
python -m pip install -r requirements.txt
```

## Cara Menjalankan

```bash
python simulated_annealing_pengiriman.py
```

Jalankan dari folder proyek agar file grafik tersimpan di folder tersebut.

## Data Studi Kasus

| Lokasi | Koordinat |
|---|---|
| Depot | (10, 10) |
| A | (20, 15) |
| B | (30, 25) |
| C | (15, 30) |
| D | (5, 25) |
| E | (25, 5) |

Rute dimulai dari Depot, mengunjungi setiap pelanggan satu kali, lalu kembali ke Depot. Jarak dihitung dengan jarak Euclidean.

## Parameter Algoritma

| Parameter | Nilai |
|---|---:|
| Suhu awal | 50.0 |
| Suhu minimum | 0.1 |
| Faktor pendinginan | 0.90 |
| Iterasi maksimum | 50 |
| Random seed | 42 |

## Kasus Uji

1. **Jarak dua kota:** Depot (0,0) dan A (3,4). Hasil manual adalah 5.00.
2. **Total jarak rute:** Depot (0,0), A (3,0), B (3,4), untuk rute Depot → A → B → Depot. Total manual adalah 3 + 4 + 5 = 12.00.
3. **Validitas kandidat:** setelah dua pelanggan ditukar, semua pelanggan harus tetap muncul tepat satu kali.

Program menggunakan `assert` untuk memeriksa hasil yang diharapkan pada ketiga pengujian.

## Memahami Keluaran

- **Jarak kandidat:** jarak rute baru yang sedang diuji.
- **Keputusan:** apakah kandidat diterima atau ditolak.
- **Jarak saat ini:** jarak rute yang digunakan setelah keputusan.
- **Jarak terbaik:** jarak terpendek yang pernah ditemukan hingga iterasi tersebut.
- **Suhu:** nilai suhu yang memengaruhi peluang menerima rute yang lebih buruk.

Jarak terbaik hanya dapat tetap atau menurun. Jarak saat ini dapat naik atau turun.

## Validasi Optimum

Karena ada lima pelanggan, jumlah urutan yang mungkin adalah `5! = 120`. Program membandingkan hasil Simulated Annealing dengan semua urutan tersebut. Pemeriksaan ini hanya digunakan untuk validasi pada studi kasus kecil, bukan sebagai bagian inti Simulated Annealing.

## Catatan
Hasil dapat bergantung pada parameter dan proses pengacakan. `random.seed(42)` dipakai agar proses acak dapat direproduksi pada kondisi perangkat lunak yang sama. Simulated Annealing tidak selalu menjamin optimum global untuk masalah yang lebih besar.

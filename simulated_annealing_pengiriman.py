import math, random, itertools
import matplotlib.pyplot as plt

# 1. DATA KOTA
KOTA = {
    "Depot": (10, 10), "A": (20, 15), "B": (30, 25),
    "C": (15, 30), "D": (5, 25), "E": (25, 5)
}


def jarak(a, b, kota=KOTA):
    """Menghitung jarak Euclidean antara dua kota."""
    x1, y1 = kota[a]
    x2, y2 = kota[b]
    return math.hypot(x2 - x1, y2 - y1)


def total_jarak(rute, kota=KOTA):
    """Menghitung jarak dari Depot, melalui pelanggan, lalu kembali ke Depot."""
    perjalanan = ["Depot"] + list(rute) + ["Depot"]
    return sum(
        jarak(perjalanan[i], perjalanan[i + 1], kota)
        for i in range(len(perjalanan) - 1)
    )


def format_rute(rute):
    return " -> ".join(["Depot"] + list(rute) + ["Depot"])


def buat_kandidat(rute):
    """Membuat kandidat dengan menukar posisi dua pelanggan."""
    kandidat = rute.copy()
    i, j = random.sample(range(len(kandidat)), 2)
    kandidat[i], kandidat[j] = kandidat[j], kandidat[i]
    return kandidat


# 2. TIGA KASUS UJI MANUAL
def jalankan_kasus_uji():
    print("\n=== KASUS UJI ===")

    # Uji 1: jarak dua titik (3-4-5)
    kota_uji_1 = {"Depot": (0, 0), "A": (3, 4)}
    hasil_1 = jarak("Depot", "A", kota_uji_1)
    assert math.isclose(hasil_1, 5.0)
    print("Uji 1 - Jarak Depot ke A: 5.00 | LULUS")

    # Uji 2: Depot-A = 3, A-B = 4, B-Depot = 5
    kota_uji_2 = {"Depot": (0, 0), "A": (3, 0), "B": (3, 4)}
    hasil_2 = total_jarak(["A", "B"], kota_uji_2)
    assert math.isclose(hasil_2, 12.0)
    print("Uji 2 - Total Depot -> A -> B -> Depot: 12.00 | LULUS")

    # Uji 3: semua pelanggan harus tetap muncul tepat satu kali
    random.seed(7)
    pelanggan = ["A", "B", "C", "D", "E"]
    kandidat = buat_kandidat(pelanggan)
    assert sorted(kandidat) == sorted(pelanggan)
    assert len(kandidat) == len(set(kandidat))
    print("Uji 3 - Validitas rute kandidat: semua pelanggan unik | LULUS")


# 3. ALGORITMA SIMULATED ANNEALING
def simulated_annealing(kota=KOTA, suhu_awal=50.0,
                        suhu_minimum=0.1, alpha=0.90,
                        maksimum_iterasi=50, seed=42):
    random.seed(seed)
    pelanggan = [nama for nama in kota if nama != "Depot"]

    sekarang = pelanggan.copy()
    jarak_sekarang = total_jarak(sekarang, kota)
    jarak_awal = jarak_sekarang

    terbaik = sekarang.copy()
    jarak_terbaik = jarak_sekarang
    suhu = suhu_awal
    riwayat = []

    print("\n=== SOLUSI AWAL ===")
    print("Rute :", format_rute(sekarang))
    print(f"Jarak: {jarak_awal:.2f}")

    for iterasi in range(1, maksimum_iterasi + 1):
        if suhu < suhu_minimum:
            break

        kandidat = buat_kandidat(sekarang)
        jarak_kandidat = total_jarak(kandidat, kota)
        delta = jarak_kandidat - jarak_sekarang
        angka_acak = None

        # Kriteria penerimaan Metropolis
        if delta <= 0:
            peluang = 1.0
            diterima = True
        else:
            peluang = math.exp(-delta / suhu)
            angka_acak = random.random()
            diterima = angka_acak < peluang

        # Perbarui rute saat ini jika kandidat diterima
        if diterima:
            sekarang = kandidat.copy()
            jarak_sekarang = jarak_kandidat

        # Perbarui rute terbaik hanya jika jaraknya lebih pendek
        if jarak_sekarang < jarak_terbaik:
            terbaik = sekarang.copy()
            jarak_terbaik = jarak_sekarang
            status_terbaik = "BARU"
        else:
            status_terbaik = "-"

        data = {
            "iterasi": iterasi,
            "jarak_kandidat": jarak_kandidat,
            "delta": delta,
            "peluang": peluang,
            "angka_acak": angka_acak,
            "keputusan": "DITERIMA" if diterima else "DITOLAK",
            "jarak_sekarang": jarak_sekarang,
            "jarak_terbaik": jarak_terbaik,
            "rute_sekarang": format_rute(sekarang),
            "rute_terbaik": format_rute(terbaik),
            "suhu": suhu,
            "status_terbaik": status_terbaik,
        }
        riwayat.append(data)

        # Keluaran ringkas per iterasi
        print(f"\nIterasi {iterasi:02d} | Suhu={suhu:.3f} | "
              f"Kandidat={jarak_kandidat:.2f} | Delta={delta:+.2f}")
        print(f"  Peluang={peluang:.3f} | "
              f"{'DITERIMA' if diterima else 'DITOLAK'}")
        print(f"  Saat ini: {format_rute(sekarang)} ({jarak_sekarang:.2f})")
        print(f"  Terbaik : {format_rute(terbaik)} ({jarak_terbaik:.2f}) "
              f"{status_terbaik}")

        # Pendinginan
        suhu = max(suhu_minimum, suhu * alpha)

    hasil = {
        "rute_awal": pelanggan.copy(),
        "jarak_awal": jarak_awal,
        "rute_terbaik": terbaik.copy(),
        "jarak_terbaik": jarak_terbaik,
        "riwayat": riwayat,
    }

    print("\n=== HASIL AKHIR ===")
    print("Rute terbaik :", format_rute(terbaik))
    print(f"Jarak terbaik: {jarak_terbaik:.2f}")
    print(f"Iterasi dijalankan: {len(riwayat)}")
    return hasil


# 4. TABEL HASIL
def tampilkan_tabel(hasil):
    print("\n=== TABEL HASIL ITERASI ===")
    print(f"{'Iter':>4} {'Kandidat':>10} {'Keputusan':>10} "
          f"{'Saat ini':>10} {'Terbaik':>10} {'Suhu':>8}")
    print("-" * 60)
    print(f"{'Awal':>4} {'-':>10} {'-':>10} "
          f"{hasil['jarak_awal']:>10.2f} "
          f"{hasil['jarak_awal']:>10.2f} {'-':>8}")

    for d in hasil["riwayat"]:
        print(f"{d['iterasi']:>4} {d['jarak_kandidat']:>10.2f} "
              f"{d['keputusan']:>10} {d['jarak_sekarang']:>10.2f} "
              f"{d['jarak_terbaik']:>10.2f} {d['suhu']:>8.3f}")


# 5. GRAFIK
def buat_grafik(hasil):
    data = hasil["riwayat"]
    x = [0] + [d["iterasi"] for d in data]
    saat_ini = [hasil["jarak_awal"]] + [
        d["jarak_sekarang"] for d in data
    ]
    terbaik = [hasil["jarak_awal"]] + [
        d["jarak_terbaik"] for d in data
    ]

    plt.figure(figsize=(9, 4.5))
    plt.plot(x, saat_ini, marker=".", label="Jarak saat ini")
    plt.plot(x, terbaik, linewidth=2, label="Jarak terbaik")
    plt.title("Perkembangan Jarak Simulated Annealing")
    plt.xlabel("Iterasi")
    plt.ylabel("Total jarak")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafik_jarak.png", dpi=300)
    plt.show()

    plt.figure(figsize=(9, 4.5))
    plt.plot([d["iterasi"] for d in data],
             [d["suhu"] for d in data], marker=".")
    plt.title("Penurunan Suhu Simulated Annealing")
    plt.xlabel("Iterasi")
    plt.ylabel("Suhu")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("grafik_suhu.png", dpi=300)
    plt.show()

    print("\nGrafik tersimpan: grafik_jarak.png dan grafik_suhu.png")


# 6. VALIDASI DENGAN SELURUH KEMUNGKINAN RUTE
def validasi_optimum(hasil):
    pelanggan = [nama for nama in KOTA if nama != "Depot"]
    rute_optimal, jarak_optimal = min(
        ((list(r), total_jarak(r, KOTA))
         for r in itertools.permutations(pelanggan)),
        key=lambda item: item[1]
    )

    print("\n=== VALIDASI OPTIMUM ===")
    print("Rute SA      :", format_rute(hasil["rute_terbaik"]))
    print(f"Jarak SA     : {hasil['jarak_terbaik']:.2f}")
    print("Rute optimal :", format_rute(rute_optimal))
    print(f"Jarak optimal: {jarak_optimal:.2f}")

    cocok = math.isclose(hasil["jarak_terbaik"], jarak_optimal,
                         rel_tol=1e-9, abs_tol=1e-9)
    print("Status:", "MENCAPAI OPTIMUM" if cocok else "BELUM OPTIMUM")


# 7. PROGRAM UTAMA
if __name__ == "__main__":
    jalankan_kasus_uji()
    hasil = simulated_annealing()
    tampilkan_tabel(hasil)
    buat_grafik(hasil)
    validasi_optimum(hasil)

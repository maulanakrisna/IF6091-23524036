# 📊 Dashboard Monitoring Gangguan Jaringan – Streamlit

Dashboard ini digunakan untuk **monitoring, analisis, dan visualisasi gangguan jaringan telekomunikasi PLN** berbasis data tiket gangguan multi-bulan.
Dibangun menggunakan **Python + Streamlit**, dashboard ini mendukung analisis risiko, durasi gangguan, serta distribusi penyebab gangguan secara interaktif.

---

## 🎯 Tujuan

Dashboard ini bertujuan untuk:

* Menyajikan **ringkasan KPI gangguan jaringan**
* Mengidentifikasi **lokasi dan risiko gangguan dominan**
* Mendukung **pengambilan keputusan operasional dan manajerial**
* Menjadi **alat bantu analisis Kerja Praktik / laporan internal**

---

## 🗂️ Struktur Proyek

```
dashboard/
│
├── app.py                # Aplikasi Streamlit
├── data_tiket.csv        # Dataset tiket gangguan
├── requirements.txt      # Dependency Python
└── README.md             # Dokumentasi proyek
```

---

## 🧾 Deskripsi Data

Dataset berisi **2366 tiket gangguan** dengan atribut utama berikut:

| Kolom             | Deskripsi                                   |
| ----------------- | ------------------------------------------- |
| No Tiket          | ID unik tiket gangguan                      |
| Produk            | Jenis layanan (IP VPN, VSAT, METRONET, dll) |
| Unit Pengguna     | Unit terdampak                              |
| Tiket Open        | Waktu mulai gangguan                        |
| Tiket Close       | Waktu gangguan selesai                      |
| Durasi (Menit)    | Total durasi gangguan                       |
| penyebab_norm     | Penyebab gangguan (hasil normalisasi)       |
| Lokasi_POP        | Lokasi POP terdekat                         |
| Lokasi_KM         | Jarak gangguan dari POP (km)                |
| kategori_risiko   | Klasifikasi risiko (Low / Medium / High)    |
| bulan             | Periode bulan kejadian                      |

---

## 🧭 Fitur Dashboard

### 🔎 Filter Interaktif

* Bulan
* Kategori Risiko
* Produk
* Unit

### 📌 KPI Utama

* Total tiket gangguan
* Total durasi gangguan (jam)
* Rata-rata durasi gangguan
* Persentase gangguan risiko tinggi

### 📈 Visualisasi

* Jumlah tiket per bulan
* Distribusi kategori risiko
* Top 10 penyebab gangguan
* Heatmap **POP × Risiko**
* Scatter plot **Jarak Gangguan vs Durasi**

### 📋 Tabel Detail

* Data tiket terfilter
* Bisa di-sort & search

---

## ⚙️ Instalasi & Menjalankan Aplikasi

### 1️⃣ Install dependency

```bash
pip install -r requirements.txt
```

### 2️⃣ Jalankan Streamlit

```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser.

---

## 🧠 Teknologi yang Digunakan

* **Python 3.10+**
* **Streamlit**
* **Pandas**
* **Matplotlib**
* **NumPy**

---

## 🚀 Pengembangan Lanjutan (Roadmap)

Beberapa pengembangan yang dapat dilakukan:

* 🔮 Prediksi risiko gangguan (rolling window)
* 📊 Analisis Pareto 80/20 penyebab gangguan
* 📍 Integrasi peta GIS
* 📤 Export laporan ke PDF / Excel
* 🧠 Scoring risiko otomatis berbasis histori

---

## 👤 Kontributor

Maulana Krisna Adhitya
Disusun untuk keperluan **Kerja Praktik**
Bidang: **Data Science / Data Analytics**

---

## 📄 Lisensi

Proyek ini digunakan untuk keperluan **akademik**.

---

✨ *Dashboard ini diharapkan dapat menjadi dasar pengembangan sistem monitoring gangguan jaringan yang lebih proaktif dan berbasis data.*

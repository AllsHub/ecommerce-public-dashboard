# E-Commerce Public Dataset Dashboard

Proyek ini merupakan submission **Proyek Analisis Data** yang menganalisis **E-Commerce Public Dataset**. Analisis difokuskan pada performa kategori produk, hubungan pengiriman dengan review pelanggan, serta segmentasi pelanggan menggunakan RFM Analysis.

## Project Overview

Tujuan proyek ini adalah mengolah data transaksi e-commerce menjadi insight bisnis yang dapat membantu perusahaan dalam menentukan prioritas promosi, pengelolaan stok, dan perbaikan layanan logistik.

Pertanyaan bisnis yang dijawab dalam proyek ini adalah:

1. Kategori produk apa yang menghasilkan total revenue dan jumlah pesanan delivered tertinggi selama periode 2016–2018?
2. Bagaimana perbedaan skor ulasan pelanggan berdasarkan durasi pengiriman dan status keterlambatan terhadap estimasi?

Analisis lanjutan dilakukan menggunakan **RFM Analysis** untuk mengelompokkan pelanggan berdasarkan Recency, Frequency, dan Monetary tanpa algoritma machine learning.

## Dashboard Features

Dashboard Streamlit menyediakan beberapa fitur utama:

- Filter berdasarkan rentang tanggal pembelian.
- Filter berdasarkan kategori produk.
- Filter berdasarkan state pelanggan.
- Ringkasan metrik utama: total revenue, total orders, total customers, dan average review score.
- Visualisasi tren revenue bulanan.
- Visualisasi kategori produk dengan revenue tertinggi.
- Visualisasi review pelanggan berdasarkan durasi dan keterlambatan pengiriman.
- Ringkasan segmentasi pelanggan berdasarkan RFM Analysis.

## Repository Structure

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   ├── main_data.csv
│   └── rfm_data.csv
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment

### Anaconda

```bash
conda create --name ecommerce-dashboard python=3.9
conda activate ecommerce-dashboard
pip install -r requirements.txt
```

### Shell/Terminal

```bash
mkdir ecommerce-dashboard
cd ecommerce-dashboard
pip install -r requirements.txt
```

## Run Notebook

Pastikan seluruh file CSV tersedia di folder `data/`, lalu jalankan notebook berikut dari awal sampai akhir:

```text
notebook.ipynb
```

Notebook akan melakukan data wrangling, EDA, visualization & explanatory analysis, RFM Analysis, serta menyimpan dataset bersih ke folder `dashboard/`.

## Run Streamlit App

Jalankan dashboard dari root folder submission dengan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka di browser lokal.

## Deployment

Untuk menjalankan dashboard di Streamlit Community Cloud:

1. Upload isi folder `submission` ke repository GitHub.
2. Buka Streamlit Community Cloud.
3. Pilih repository dan branch yang digunakan.
4. Isi **Main file path** dengan:

```text
dashboard/dashboard.py
```

5. Klik **Deploy**.
6. Simpan URL dashboard ke file `url.txt`.

## Analysis Notes

- Dataset utama yang digunakan berasal dari **E-Commerce Public Dataset**.
- Analisis utama hanya menggunakan order berstatus `delivered`.
- Revenue dihitung sebagai `price + freight_value` pada level item pesanan.
- Analisis review menggunakan data pada level order agar satu order tidak dihitung berulang akibat memiliki lebih dari satu item.
- RFM Analysis digunakan sebagai teknik analisis lanjutan tanpa algoritma machine learning.

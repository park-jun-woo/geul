---
title: "Arsitektur"
date: 2026-02-26T12:00:00+09:00
image: "/images/og-default.webp"
summary: "Bagaimana GEUL dibangun: pengindeksan yang diselaraskan secara semantik, unit kata 16-bit, memori terstruktur, dan representasi pengetahuan berbasis klaim."
---

## Subtopik

### Mengapa 16-Bit
Semua data di GEUL dalam satuan 16-bit (1 kata). Ini adalah satuan minimum yang menggabungkan efisiensi kode mesin dengan makna bahasa manusia dalam satu kata.

### Mengapa Menyimpan Penalaran sebagai Kode
Membuang hasil setiap kali AI bernalar adalah pemborosan komputasi. Mencatat penalaran dalam bahasa terstruktur memungkinkan penggunaan ulang dan akumulasi.

### Mengapa Klaim, Bukan Fakta
Kalimat bahasa alami terlihat seperti fakta tetapi sebenarnya adalah klaim seseorang. Menyematkan sumber, waktu, dan tingkat keyakinan secara struktural mengurangi ruang untuk halusinasi.

### Mengapa Indeks yang Selaras Secara Semantik
SIDX adalah pengenal 64-bit yang mengkodekan makna dalam bit itu sendiri. Tipe dapat ditentukan hanya dari bit atas, dan semakin sedikit bit yang diisi, semakin abstrak ekspresinya.

### Mengapa Memori Terstruktur Diperlukan
Jendela konteks LLM terbatas. Untuk memasukkan pengalaman tak terbatas ke dalam jendela terbatas, memori harus terstruktur.

---
title: "Mengapa Pemeriksaan Konsistensi Diperlukan"
weight: 6
date: 2026-02-26T12:00:08+09:00
lastmod: 2026-02-26T12:00:08+09:00
tags: ["konsistensi", "kontradiksi", "koherensi"]
summary: "Informasi yang secara individual benar bisa secara kolektif salah"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Informasi yang secara individual benar bisa secara kolektif salah.

---

## Verifikasi Lolos. Penyaringan Lolos.

Verifikasi mekanis menyaring error format.
Penyaringan menyeleksi berdasarkan relevansi, kepercayaan, dan kebaruan.

30 informasi tersisa.
Semuanya valid, semuanya relevan, semuanya terpercaya, semuanya terkini.

Apakah Anda memasukkan 30 ini ke konteks?

Tidak.
Satu hal lagi harus diperiksa.
Apakah ke-30 ini saling bertentangan?

---

## Kontradiksi Bukan Properti Informasi Individual

Perhatikan dua pernyataan ini.

- Sumber: pengungkapan IR Samsung Electronics, Oktober 2024. "CEO Samsung Electronics: Jun Young-hyun."
- Sumber: pengungkapan IR Samsung Electronics, Maret 2024. "CEO Samsung Electronics: Kyung Kye-hyun."

Secara individual, keduanya valid.
Formatnya benar, sumbernya ada, waktunya ada, dan terpercaya.
Mereka lolos verifikasi. Mereka lolos penyaringan.

Tetapi ketika keduanya masuk ke konteks yang sama, ada masalah.
Apakah CEO Samsung Electronics itu Jun Young-hyun atau Kyung Kye-hyun?

Tidak ada pernyataan yang salah.
Pada bulan Maret, Kyung Kye-hyun benar. Pada bulan Oktober, Jun Young-hyun benar.
Secara individual, keduanya benar.
Tetapi ketika mereka hadir bersama dalam konteks, LLM menjadi bingung.

Ini adalah masalah konsistensi.
Ia muncul bukan dari informasi individual tetapi dari kumpulan informasi.
Verifikasi memeriksa informasi individual. Penyaringan memeriksa informasi individual.
Konsistensi memeriksa ruang di antara informasi.

---

## Jenis-Jenis Kontradiksi

Kontradiksi dalam konteks terbagi menjadi beberapa jenis.

### Kontradiksi Temporal

Yang paling umum.

Properti yang sama dari entitas yang sama berubah seiring waktu,
dan nilai dari titik waktu yang berbeda hadir bersama dalam konteks.

"CEO Tesla: Elon Musk" dan
"Harga saham Tesla: $194" berada dalam konteks yang sama,
tetapi informasi CEO per 2024 dan harga saham dari Juni 2023.
LLM mungkin memperlakukannya sebagai informasi dari titik waktu yang sama.

Kasus yang lebih halus juga muncul.
"Suku bunga dasar Korea Selatan: 3,50%" per Januari 2024, dan
"Inflasi harga konsumen Korea Selatan: 2,0%" per Oktober 2024.
Keduanya valid dan keduanya berkaitan dengan ekonomi Korea,
tetapi ada jarak 9 bulan.
Apakah jarak ini memengaruhi inferensi bergantung pada konteks.

### Kontradiksi Antar Sumber

Sumber yang berbeda menyajikan nilai yang berbeda untuk fakta yang sama.

- Sumber A: "Ukuran pasar AI global 2024: $184 miliar."
- Sumber B: "Ukuran pasar AI global 2024: $214 miliar."

Tidak ada yang bisa dinyatakan secara pasti "salah."
Definisi cakupan pasar mungkin berbeda. Metode pengukuran mungkin berbeda.
Tetapi jika keduanya ada dalam konteks,
LLM harus memilih salah satu, mencampur keduanya, atau menjadi bingung.

### Kontradiksi Inferensial

Bukan nilai yang secara langsung bertentangan,
tetapi secara logis tidak kompatibel ketika ditempatkan bersama.

"Pangsa pasar Perusahaan A: 60%."
"Pangsa pasar Perusahaan B: 55%."

Masing-masing valid. Tetapi jumlahnya 115%.
Menambahkan kompetitor yang tersisa akan melebihi 100%.
Salah satunya dari waktu yang berbeda, menggunakan definisi pasar yang berbeda, atau salah.

Jenis kontradiksi ini tidak bisa ditemukan dengan melihat pernyataan individual.
Anda harus memeriksa kumpulannya.

---

## LLM Tidak Menangani Kontradiksi dengan Baik

Secara teori, LLM seharusnya bisa mendeteksi dan menyelesaikan kontradiksi.
"Kedua informasi ini berbeda waktu, jadi saya akan menjawab berdasarkan yang lebih baru."

Dalam praktiknya, bukan itu yang terjadi.

**LLM cenderung mempercayai informasi dalam konteks.**
Tindakan memasukkan sesuatu ke konteks itu sendiri adalah sinyal yang mengatakan "rujuk ini."
Ketika dua informasi yang bertentangan hadir,
LLM cenderung merujuk keduanya daripada mengabaikan salah satu.
Hasilnya adalah campuran atau kebingungan.

**Deteksi kontradiksi memerlukan penalaran.**
Mengetahui bahwa "CEO: Jun Young-hyun" dan "CEO: Kyung Kye-hyun" bertentangan
memerlukan pengetahuan latar bahwa hanya ada satu CEO pada satu waktu.
Memeriksa apakah jumlah pangsa pasar melebihi 100% memerlukan aritmetika.
Ini bergantung pada kemampuan penalaran LLM.

**Penyelesaian bahkan lebih sulit.**
Bahkan jika kontradiksi terdeteksi, harus ada penilaian tentang sisi mana yang dipilih.
Yang lebih baru? Sumber yang lebih terpercaya? Yang didukung lebih banyak sumber?
Jika penilaian ini diserahkan ke LLM, konsistensi tidak terjamin.
Untuk kontradiksi yang sama, ia memilih A kadang-kadang dan B di lain waktu.

Kesimpulannya, menangani kontradiksi setelah masuk ke konteks
itu mahal dan hasilnya tidak pasti.
Kontradiksi harus diselesaikan sebelum masuk ke konteks.

---

## Mengapa Pemeriksaan Konsistensi Sulit dalam Bahasa Alami

Misalkan Anda memeriksa konsistensi 30 chunk bahasa alami.

Pertama, Anda harus menentukan apakah mereka tentang subjek yang sama.
Apakah "Samsung Electronics," "Samsung Electronics," dan "Samsung" merujuk ke entitas yang sama.
Dalam bahasa alami, ini tidak pasti.
Apakah "Samsung" berarti Samsung Electronics, Samsung C&T, atau Samsung Life memerlukan pembacaan konteks.

Selanjutnya, Anda harus menentukan apakah mereka mendeskripsikan properti yang sama.
Apakah "pendapatan," "revenue," "total pendapatan," dan "pendapatan kotor" hal yang sama.
Apakah "laba operasional," "operating profit," dan "margin operasional" sama atau berbeda.

Selanjutnya, Anda harus mengekstrak referensi waktu.
Kapan "kuartal lalu"? Kapan "baru-baru ini"? Kapan "tahun ini"?

Hanya setelah semua ini barulah Anda bisa membandingkan apakah dua pernyataan saling bertentangan.

Dengan 30 pernyataan, ada 435 pasangan perbandingan.
Setiap pasangan harus melalui proses di atas.
Semuanya penalaran LLM.
Semuanya mahal.
Semuanya probabilistik.

---

## Pemeriksaan Konsistensi dalam Representasi Terstruktur

Dalam representasi terstruktur, situasinya berbeda.

**Identifikasi entitas bersifat deterministik.**
Entitas "Samsung Electronics" memiliki pengidentifikasi unik.
"Samsung Electronics" menunjuk ke pengidentifikasi yang sama.
Tidak diperlukan penalaran untuk menentukan identitas.

**Properti bersifat eksplisit.**
"Pendapatan" adalah properti bertipe.
"Margin operasional" adalah properti yang berbeda.
Apakah dua properti sama atau berbeda dikonfirmasi dengan perbandingan field.

**Waktu adalah field.**
Ada nilai seperti "2024-Q3."
Tidak perlu menginterpretasi "kuartal lalu."
Apakah dua pernyataan memiliki waktu yang sama adalah satu perbandingan nilai.

Ketika ketiga hal ini deterministik, pola deteksi kontradiksi menjadi bisa dimekanisasi.

Entitas sama + properti sama + waktu sama + nilai berbeda = kontradiksi.
Entitas sama + properti sama + waktu berbeda + nilai berbeda = perubahan. Bukan kontradiksi.
Entitas berbeda + properti sama + waktu sama + jumlah nilai > 100% = kontradiksi inferensial.

Tidak perlu LLM untuk ini.
Perbandingan field dan aritmetika.

Tidak semua kontradiksi bisa ditangkap.
Apakah "pasar AI sedang tumbuh" dan "investasi AI sedang menurun" saling bertentangan
masih memerlukan penilaian semantik.
Tetapi jika kontradiksi yang bisa dideteksi secara mekanis ditangkap lebih dulu,
hanya kasus yang memerlukan penilaian semantik yang tersisa.
Sekali lagi, yang murah lebih dulu.

---

## Strategi Penyelesaian untuk Pemeriksaan Konsistensi

Setelah mendeteksi kontradiksi, ia harus diselesaikan.

Strategi penyelesaian bervariasi sesuai konteks, tetapi dalam representasi terstruktur mereka bisa dinyatakan sebagai kebijakan.

**Yang terbaru lebih dulu.** Ketika properti yang sama dari entitas yang sama bertentangan, pilih yang memiliki timestamp lebih baru. Cocok untuk nilai yang berubah seperti CEO, harga saham, populasi.

**Kepercayaan tertinggi lebih dulu.** Pilih yang memiliki kepercayaan lebih tinggi. Atau jika hierarki sumber terdefinisi, pilih sumber dengan peringkat lebih tinggi. Sumber primer > sumber sekunder > sumber tidak resmi.

**Sajikan keduanya.** Jangan selesaikan kontradiksinya. Masukkan keduanya ke konteks, tetapi tandai kontradiksinya secara eksplisit. "Sumber A menyatakan $184 miliar; Sumber B menyatakan $214 miliar. Kemungkinan karena perbedaan definisi." Biarkan LLM bernalar dengan kesadaran akan kontradiksi.

**Kecualikan keduanya.** Jika kontradiksi tidak bisa diselesaikan, kecualikan kedua sisi. Tidak ada informasi lebih baik daripada informasi yang salah.

Dalam pipeline bahasa alami, strategi-strategi ini ditulis dalam bahasa alami di prompt.
"Tolong prioritaskan informasi yang paling baru."
Apakah LLM mengikuti ini secara konsisten adalah, lagi-lagi, masalah probabilitas.

Dalam representasi terstruktur, strategi-strategi ini dinyatakan sebagai kebijakan.
"Pada konflik entitas-sama + properti-sama: timestamp terbaru lebih dulu. Jika timestamp sama: kepercayaan tertinggi lebih dulu. Jika kepercayaan sama: sajikan keduanya."
Mesin mengeksekusinya. Bukan probabilitas.

---

## Posisi dalam Pipeline

Pemeriksaan konsistensi datang setelah penyaringan.

Verifikasi -> Penyaringan -> Konsistensi.

Mengapa urutan ini?

Verifikasi menyaring error format.
Penyaringan menghapus informasi yang tidak diperlukan.
Pemeriksaan konsistensi hanya perlu memproses apa yang lolos verifikasi dan penyaringan.

Pemeriksaan konsistensi membandingkan pasangan.
Untuk n pernyataan, ada n(n-1)/2 pasangan.
1.000 menghasilkan sekitar 500.000 pasangan. 30 menghasilkan 435.

Jika verifikasi dan penyaringan mengurangi 1.000 menjadi 30,
biaya pemeriksaan konsistensi turun dari 500.000 menjadi 435 -- seperseribu.

Urutan itu penting.

---

## Ringkasan

Informasi yang secara individual valid, relevan, dan terpercaya
bisa saling bertentangan ketika dikumpulkan sebagai satu set.

Ada tiga jenis kontradiksi.
Kontradiksi temporal -- nilai dari titik waktu yang berbeda hadir bersama.
Kontradiksi antar sumber -- sumber yang berbeda menyajikan nilai yang berbeda.
Kontradiksi inferensial -- secara individual valid, tetapi secara logis tidak kompatibel ketika digabungkan.

LLM tidak menangani kontradiksi dengan baik.
Mereka cenderung mempercayai informasi dalam konteks,
deteksi kontradiksi memerlukan penalaran,
dan konsistensi penyelesaian tidak terjamin.

Dalam bahasa alami, pemeriksaan konsistensi adalah penalaran LLM sepenuhnya.
Identitas entitas, identitas properti, ekstraksi waktu, perbandingan nilai -- semuanya probabilistik dan mahal.

Dalam representasi terstruktur, pengidentifikasi entitas, tipe properti, dan field waktu ada,
sehingga sebagian besar deteksi kontradiksi berubah menjadi perbandingan field dan aritmetika.
Strategi penyelesaian juga dinyatakan sebagai kebijakan.

Pemeriksaan konsistensi datang setelah penyaringan dalam pipeline.
Verifikasi dan penyaringan harus mengurangi set agar jumlah pasangan perbandingan menyusut.
Yang murah lebih dulu, dan pemeriksaan kolektif datang setelah pemeriksaan individual selesai.

---
title: "Mengapa RAG Tidak Cukup"
weight: 2
date: 2026-02-26T12:00:11+09:00
lastmod: 2026-02-26T12:00:11+09:00
tags: ["RAG", "pencarian", "embedding"]
summary: "Tampak relevan dan benar-benar relevan adalah dua hal yang berbeda"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Tampak relevan dan benar-benar relevan adalah dua hal yang berbeda.

---

## RAG Adalah Standar Saat Ini

Per 2024, RAG adalah cara paling umum perusahaan memanfaatkan LLM.

Retrieval-Augmented Generation.
Cari dokumen eksternal, masukkan ke konteks, dan biarkan model menjawab berdasarkan itu.

RAG berhasil.
RAG memungkinkan LLM merujuk dokumen internal yang tidak pernah ada dalam data pelatihan mereka.
RAG memungkinkan mereka mencerminkan informasi terkini.
RAG secara signifikan mengurangi halusinasi.

Tanpa RAG, adopsi LLM di perusahaan akan jauh lebih lambat.
RAG adalah teknologi yang patut dihormati.

Tetapi RAG memiliki keterbatasan fundamental.
Keterbatasan ini tidak terselesaikan dengan membangun RAG yang lebih baik.
Mereka berasal dari premis RAG itu sendiri.

---

## Cara Kerja RAG

Inti RAG adalah tiga langkah.

**Langkah 1: Bagi dokumen menjadi chunk.**
PDF, wiki, dokumen internal dibagi menjadi ukuran tetap (biasanya 200--500 token).

**Langkah 2: Ubah setiap chunk menjadi vektor embedding.**
Vektor bilangan real berdimensi ratusan hingga ribuan.
"Makna" teks dipetakan ke satu titik dalam ruang vektor.

**Langkah 3: Ketika kueri masuk, cari vektor yang mirip.**
Kueri juga diubah menjadi vektor.
5--20 chunk teratas dengan cosine similarity tertinggi dipilih dan dimasukkan ke konteks.

Sederhana dan elegan.
Dan di sinilah tiga masalah fundamental bersembunyi.

---

## Masalah 1: Mirip Bukan Berarti Relevan

Kemiripan embedding mengukur "apakah dua teks menggunakan kata-kata yang mirip dalam konteks yang mirip."

Itu bukan relevansi.

Contoh.

Kueri: "Berapa pendapatan Apple di Q3 2024?"

Chunk yang mungkin dikembalikan pencarian embedding:
- "Pendapatan Apple Q3 2024 adalah $94,9 miliar." -- Relevan
- "Pendapatan Apple Q3 2023 adalah $81,8 miliar." -- Mirip tapi periode waktu berbeda
- "Pendapatan Samsung Electronics Q3 2024 adalah 79 triliun won." -- Mirip tapi perusahaan berbeda
- "Satu potong pai apel mengandung sekitar 296 kkal." -- Tumpang tindih kata kunci

Kemiripan embedding tidak bisa membedakan keempatnya.
Dalam ruang vektor, "Apple revenue" berkumpul di satu kawasan.
Entah itu 2023 atau 2024, Apple atau Samsung --
jarak vektor tidak bisa memisahkan mereka secara andal.

Menambahkan reranker memperbaiki keadaan.
Tetapi reranker juga membaca dan menilai teks bahasa alami,
jadi masalah ambiguitas fundamental tetap ada.

Pencarian berbasis struktur semantik berbeda.
Jika "Apple" sebagai entitas memiliki pengidentifikasi unik,
ia tidak pernah tertukar dengan "apple" buah.
Jika "Q3 2024" adalah sebuah field waktu,
ia secara mekanis dibedakan dari "Q3 2023."

Tidak perlu menghitung kemiripan.
Cocok atau tidak? Ya atau tidak.

---

## Masalah 2: Chunk Bukan Satuan Makna

Lihat kembali langkah pertama RAG.
"Bagi dokumen menjadi chunk."

"Pembagian" itulah masalahnya.

Ketika Anda membagi dokumen menjadi unit 500 token,
makna terpotong di tengah.
Satu paragraf terbagi menjadi dua chunk.
Premis dan kesimpulan suatu argumen terpisah.

"Yi Sun-sin menghadapi 133 kapal hanya dengan 12 kapal di Pertempuran Myeongnyang" ada di Chunk A,
dan "para sejarawan memperdebatkan angka-angka ini" ada di Chunk B.
Jika hanya Chunk A yang diambil untuk suatu kueri,
informasi tingkat kepercayaan masuk ke konteks dalam keadaan sudah hilang.

Perbesar chunk? Mereka memakan lebih banyak jendela.
Perkecil chunk? Lebih banyak konteks terpotong.
Tambahkan overlap? Anda membuang jendela untuk duplikat.

Bagaimana pun Anda menyesuaikan, masalah fundamental tetap sama.
Memecah teks bahasa alami berdasarkan jumlah token
sama dengan memecah makna berdasarkan jumlah token.
Makna memiliki ukuran alaminya sendiri,
dan membaginya dengan satuan yang tidak berhubungan menimbulkan masalah.

Dalam representasi terstruktur, satuan makna bersifat eksplisit.
Satu predikasi adalah satu edge.
Edge tidak dipecah.
Pencarian beroperasi di level edge.
Tidak ada pemotongan di tengah makna.

---

## Masalah 3: Kualitas Hasil Pencarian Tidak Diketahui

RAG mengembalikan 5 chunk.
Sebelum memasukkan 5 chunk ini ke konteks, ada pertanyaan yang harus dijawab.

Apa sumber informasi ini?
Kapan tanggal referensinya?
Seberapa pasti informasinya?
Apakah kelima chunk ini saling bertentangan?

Dalam chunk bahasa alami, hal-hal ini tidak bisa diketahui.

Sumber mungkin atau mungkin tidak disebutkan di suatu tempat dalam chunk sebagai bahasa alami.
Referensi waktu mungkin ada di suatu tempat dalam dokumen, atau mungkin hilang saat chunk dipecah.
Tingkat kepercayaan tidak memiliki slot struktural dalam bahasa alami, sehingga hampir selalu tidak ada.
Pemeriksaan kontradiksi memerlukan pembacaan semua 5 chunk dan penalaran atasnya.

Pada akhirnya, Anda harus mendelegasikan penilaian kualitas ke LLM.
Anda menggunakan RAG untuk mengurangi biaya pemanggilan LLM,
tetapi Anda memanggil LLM untuk memverifikasi hasil RAG.

Dalam representasi terstruktur, sumber, waktu, dan kepercayaan adalah field.
"Kecualikan pernyataan tanpa sumber" adalah satu baris kueri.
"Kecualikan informasi sebelum 2023" adalah satu perbandingan field.
"Kecualikan kepercayaan di bawah 0,5" adalah satu perbandingan numerik.
Tidak perlu pemanggilan LLM.

---

## Premis Fundamental RAG

Akar dari ketiga masalah ini adalah satu hal.

RAG mencari bahasa alami sebagai bahasa alami.

Dokumennya adalah bahasa alami.
Chunk-nya adalah bahasa alami.
Embedding-nya adalah aproksimasi statistik dari bahasa alami.
Hasil pencariannya adalah bahasa alami.
Yang masuk ke konteks adalah bahasa alami.

Ambiguitas bahasa alami meresap ke seluruh pipeline.

Pencarian tidak akurat karena Anda mencari konten ambigu dalam bentuknya yang ambigu.
Konteks hilang karena Anda memecah konten ambigu berdasarkan ukuran yang tidak berhubungan dengan makna.
Verifikasi tidak mungkin karena Anda tidak bisa mengekstrak informasi kualitas dari konten ambigu.

Sebagian besar upaya memperbaiki RAG beroperasi dalam premis ini.

Gunakan model embedding yang lebih baik. -- Aproksimasi statistik menjadi lebih halus, hanya itu.
Gunakan strategi chunking yang lebih baik. -- Posisi pemotongan membaik, hanya itu.
Tambahkan reranker. -- Anda membaca bahasa alami sekali lagi, hanya itu.
Gunakan hybrid search. -- Anda mencampur kata kunci dan kemiripan, hanya itu.

Semuanya berhasil.
Semuanya tetap dalam kerangka bahasa alami.
Tidak ada yang fundamental.

---

## Syarat untuk Alternatif Fundamental

Untuk melampaui batas RAG, premisnya harus berubah.
Bukan mencari bahasa alami sebagai bahasa alami,
melainkan mencari representasi terstruktur secara struktural.

Alternatif ini harus memenuhi tiga syarat.

**Pencarian berdasarkan kecocokan, bukan kemiripan.**
Bukan menemukan "hal-hal yang tampak mirip"
tetapi menemukan "hal-hal yang cocok."
Apakah pengidentifikasinya cocok? Apakah dalam rentang waktu?
Ya atau tidak. Bukan probabilitas.

**Satuan makna adalah satuan pencarian.**
Bukan memecah berdasarkan jumlah token
tetapi menyimpan per predikasi dan mencari per predikasi.
Tidak ada pemotongan di tengah makna.

**Metadata tertanam dalam struktur.**
Tidak perlu memanggil LLM untuk menilai kualitas hasil pencarian.
Sumber, waktu, dan kepercayaan adalah field,
sehingga penyaringan mekanis dimungkinkan.

Ketika ketiga syarat ini terpenuhi,
pencarian bergeser dari "menebak kandidat yang masuk akal"
menjadi "mengonfirmasi apa yang cocok."

---

## RAG Adalah Teknologi Transisi

Ini bukan untuk merendahkan RAG.

RAG adalah jawaban terbaik di dunia di mana bahasa alami adalah segalanya.
Ketika dokumen adalah bahasa alami, pengetahuan disimpan dalam bahasa alami,
dan LLM adalah alat yang memproses bahasa alami,
mencari bahasa alami dengan bahasa alami adalah pilihan yang jelas.

Dan RAG memang berhasil.
LLM dengan RAG jauh lebih akurat daripada tanpa RAG.
Ini adalah fakta.

Tetapi jika premis "dunia di mana bahasa alami adalah segalanya" berubah,
posisi RAG pun berubah.

Jika representasi terstruktur ada,
RAG menjadi front end yang "menerima input bahasa alami dan mencari penyimpanan terstruktur."
Bahasa alami -> kueri terstruktur -> pencarian struktural -> hasil terstruktur -> konteks.

RAG tidak menghilang.
Backend-nya yang berubah.
Dari pencarian kemiripan embedding ke pencarian berbasis struktur semantik.

---

## Ringkasan

RAG adalah standar saat ini untuk context engineering.
Dan ia memiliki tiga keterbatasan fundamental.

1. **Mirip ≠ relevan.** Kemiripan embedding tidak menjamin relevansi. "Tampak mirip" dan "benar-benar relevan" berbeda.
2. **Chunk ≠ makna.** Memecah berdasarkan jumlah token memotong di tengah makna. Premis dan kesimpulan terpisah. Informasi kepercayaan hilang.
3. **Penilaian kualitas tidak mungkin.** Sumber, waktu, dan kepercayaan chunk yang diambil tidak bisa ditentukan secara mekanis. Menilainya memerlukan pemanggilan LLM.

Akar ketiga masalah adalah satu hal.
Mencari bahasa alami sebagai bahasa alami.

Alternatif fundamental adalah mengubah premis.
Kecocokan, bukan kemiripan.
Predikasi, bukan chunk token.
Metadata tertanam, bukan penilaian eksternal.

RAG adalah teknologi transisi.
Ia adalah jawaban terbaik di dunia di mana bahasa alami adalah segalanya.
Ketika premis itu berubah, backend RAG berubah.

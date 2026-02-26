---
title: "Mengapa Eksplorasi Diperlukan"
weight: 7
date: 2026-02-26T12:00:07+09:00
lastmod: 2026-02-26T12:00:07+09:00
tags: ["eksplorasi", "pencarian", "skala"]
summary: "Ketika indeks melebihi jendela, paradigma pencarian itu sendiri mencapai batasnya"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Ketika indeks melebihi jendela, paradigma pencarian itu sendiri mencapai batasnya.

---

## Pencarian Telah Berhasil

Kita telah membahas keterbatasan RAG.
Ketidakakuratan kemiripan embedding, keserampangan pemecahan chunk, ketidakmungkinan penilaian kualitas.

Tetapi pembahasan itu tentang kualitas pencarian.
"Bagaimana kita mencari dengan lebih akurat?"

Sekarang pertanyaan yang berbeda harus diajukan.
Asumsikan pencarian sempurna.
Asumsikan ia hanya mengembalikan informasi yang tepat relevan dengan kueri.

Masih ada kasus di mana ia tidak berhasil.

---

## Masalah Skala

Basis pengetahuan internal memiliki 1.000 pernyataan.
Ada indeks. Masukkan indeks ke konteks. Kueri. Ambil hasil.
Berhasil.

Pernyataan bertambah menjadi 100.000.
Indeks membesar. Masih muat di jendela. Berhasil.

Pernyataan bertambah menjadi 10 juta.
Indeks itu sendiri melebihi jendela.

Ini bukan masalah kualitas pencarian.
Seakurat apa pun pencariannya,
jika indeks yang harus dikonsultasi untuk mencari tidak muat di jendela,
pencarian bahkan tidak bisa dimulai.

Dan pengetahuan bertumbuh.
Dokumen perusahaan bertambah setiap hari.
Apa yang telah dipelajari agen terus terakumulasi.
Pengetahuan dunia tidak menyusut.

Apakah jendela yang lebih besar menyelesaikan ini?
Jika 128K menjadi 1M menjadi 10M?
Jika pengetahuan mencapai 100M, masalah yang sama terulang.
Jendela selalu terbatas, dan pengetahuan selalu bertumbuh.
Ketidakseimbangan ini bersifat permanen.

---

## Perbedaan Antara Pencarian dan Eksplorasi

Pencarian mendapatkan hasil dengan satu kueri.

Kueri: "Laba operasional Samsung Electronics Q3 2024"
-> Hasil: 9,18 triliun won.

Satu tembakan. Selesai.

Eksplorasi mencapai hasil melalui beberapa langkah.

Langkah 1: Lihat peta pengetahuan tingkat atas. "Korporasi," "Industri," "Makroekonomi," "Teknologi"...
-> Pilih "Korporasi."

Langkah 2: Lihat peta korporasi. "Samsung Electronics," "SK Hynix," "Hyundai Motor"...
-> Pilih "Samsung Electronics."

Langkah 3: Lihat peta Samsung Electronics. "Keuangan," "SDM," "Teknologi," "Hukum"...
-> Pilih "Keuangan."

Langkah 4: Lihat peta keuangan. "Hasil kuartalan," "Hasil tahunan," "Rencana investasi"...
-> Pilih "Hasil kuartalan."

Langkah 5: Ambil "Q3 2024" dari hasil kuartalan.
-> Laba operasional: 9,18 triliun won.

Hasilnya sama.
Prosesnya berbeda.

Pencarian adalah bertanya "Apakah Anda punya ini?"
Eksplorasi adalah melacak "Di mana mungkin ini berada?"

Pencarian mengharuskan indeks terlihat oleh pencari. Seluruh indeks harus bisa diakses.
Eksplorasi hanya perlu melihat lapisan peta saat ini. Di setiap langkah, hanya satu lapisan yang masuk ke jendela.

---

## Analogi Perpustakaan

Anda mengunjungi perpustakaan lingkungan.
Koleksinya 3.000 buku.
Anda bertanya ke pustakawan: "Apakah ada biografi Yi Sun-sin?"
Pustakawan ingat: "Ada di ujung rak 3."
Pencarian. Berhasil.

Anda mengunjungi Perpustakaan Nasional.
Koleksinya 10 juta volume.
Anda bertanya ke pustakawan: "Apakah ada biografi Yi Sun-sin?"
Pustakawan pun tidak tahu. Tidak ada yang menghafal 10 juta volume.

Sebagai gantinya, ada sistem klasifikasi.

Anda memeriksa direktori lantai satu. -> Bagian "Sejarah" ada di lantai 3.
Anda naik ke lantai 3. -> "Sejarah Korea" ada di sayap timur.
Anda ke sayap timur. -> "Dinasti Joseon" ada di baris D.
Anda ke baris D. -> "Tokoh" ada di seksi ke-3 baris D.
Anda mencari seksi ke-3. -> Ada biografi Yi Sun-sin.

Kapasitas ingatan pustakawan tidak berubah.
Skala perpustakaan yang berubah.
Metodenya bergeser dari bertanya ke pustakawan (pencarian) ke menelusuri sistem klasifikasi (eksplorasi).

Inilah kuncinya.
Di setiap langkah, ukuran yang harus dilihat muat dalam kapasitas ingatan pustakawan.
Direktori lantai satu. Peta zona lantai 3. Daftar baris di sayap timur. Daftar seksi di baris D.
Semuanya muat dalam satu pandangan.

Katalog lengkap seluruh koleksi tidak muat dalam satu pandangan.
Tetapi peta setiap lantai bisa.

Inilah perbedaan eksplorasi dari pencarian.
Anda tidak perlu melihat keseluruhan sekaligus.
Anda hanya perlu menilai arah selanjutnya dari posisi Anda saat ini.

---

## Peta dari Peta

Dalam istilah teknis, ini adalah struktur hierarkis dari peta.

**Peta Level 1**: klasifikasi tingkat atas dari seluruh pengetahuan.
"Basis pengetahuan ini berisi informasi tentang korporasi, industri, makroekonomi, dan teknologi."
Puluhan item. Muat di jendela.

**Peta Level 2**: subkategori dari setiap klasifikasi tingkat atas.
"Kategori korporasi berisi Samsung Electronics, SK Hynix, Hyundai Motor..."
Puluhan hingga ratusan item. Muat di jendela.

**Peta Level 3**: kategori detail dari setiap subkategori.
"Samsung Electronics berisi Keuangan, SDM, Teknologi, Hukum..."
Puluhan item. Muat di jendela.

**Pernyataan aktual**: informasi konkret yang ditunjuk oleh peta level terendah.
"Laba operasional Samsung Electronics Q3 2024 adalah 9,18 triliun won."

Jika ukuran setiap lapisan muat di jendela,
eksplorasi dimungkinkan terlepas dari skala total pengetahuan.

Bahkan dengan 10 juta pernyataan,
jika setiap lapisan memiliki 100 item, Anda mencapai target dalam 5 langkah eksplorasi.
100 -> 100 -> 100 -> 100 -> 100 = cakupan hingga 10 miliar.
Di setiap langkah, hanya 100 item yang masuk ke jendela.

Ini sama dengan cara B-tree menemukan data di disk.
Ia tidak memuat semua data ke memori.
Ia hanya membaca node pohon saat ini dan bergerak ke node berikutnya.
Data berskala apa pun bisa dijelajahi terlepas dari ukuran memori.

Jendela konteks adalah memori.
Basis pengetahuan adalah disk.
Peta adalah node B-tree.

---

## Agen Berjalan

Dalam eksplorasi multi-langkah, siapa yang memilih arah di setiap langkah?

Agen.

Masukkan peta level 1 ke konteks.
Agen membacanya, membandingkannya dengan kueri, dan memilih arah "Korporasi."

Minta peta level 2.
Peta subkategori korporasi masuk ke konteks.
Agen membacanya dan memilih arah "Samsung Electronics."

Minta peta level 3.
Agen memilih "Keuangan."

Ini adalah penggunaan tool oleh agen.
Membaca peta adalah tool call.
Memilih arah adalah penilaian.
Meminta peta berikutnya adalah tool call berikutnya.

Dalam pencarian, agen mengkueri sekali dan menerima hasil. Pasif.
Dalam eksplorasi, agen membuat beberapa penilaian dan memilih arah. Aktif.

Di sinilah context engineering bertemu desain agen.
Apa yang masuk ke konteks ditentukan langkah demi langkah melalui penilaian agen.
Konstruksi konteks bergeser dari perakitan statis ke eksplorasi dinamis.

---

## Masalah Ini Nyaris Tidak Dibahas Hari Ini

Melihat diskusi di komunitas RAG,
sebagian besar energi terfokus pada kualitas pencarian.

Model embedding yang lebih baik.
Strategi chunking yang lebih baik.
Arsitektur reranker.
Hybrid search.
Graph RAG.

Semuanya penting.
Semuanya tentang "bagaimana mendapatkan hasil yang lebih baik dari satu kali pencarian."

"Bagaimana jika satu kali pencarian tidak cukup?" nyaris tidak dibahas.

Titik ketika indeks melebihi jendela.
Titik ketika hasil terlalu banyak untuk dimuat.
Titik ketika skala pengetahuan merusak premis paradigma pencarian itu sendiri.

Titik itu sedang datang.
Pengetahuan bertumbuh dan jendela terbatas.

Sebagian besar solusi saat ini adalah penghindaran.
Ambil hanya top k. Buang sisanya.
Perbesar jendela. Biaya meningkat.
Partisi pengetahuan. Pisahkan vector store per domain.

Semuanya menemui masalah yang sama lagi ketika skala bertambah.

---

## Prasyarat untuk Eksplorasi

Agar eksplorasi berhasil, pengetahuan harus dalam struktur yang bisa dijelajahi.

**Hierarki harus ada.** Jika pengetahuan disusun datar, eksplorasi tidak mungkin. Penyimpanan vektor embedding bersifat datar. Semua chunk berada di level yang sama. Tidak ada hierarki, sehingga konsep "masuk lebih dalam" tidak ada.

**Setiap lapisan harus muat di jendela.** Jika satu peta melebihi jendela, eksplorasi gagal. Jumlah pilihan di setiap level hierarki harus berukuran tepat. Ini adalah masalah desain klasifikasi.

**Jalur harus beragam.** Harus dimungkinkan untuk mencapai informasi yang sama melalui beberapa jalur. Melalui "Samsung Electronics -> Keuangan -> Laba operasional" atau melalui "Industri semikonduktor -> Perusahaan utama -> Samsung Electronics -> Hasil." Karena jalur alami bervariasi tergantung pada pertanyaan. Jika kriteria klasifikasi ditetapkan satu saja, ia cocok untuk beberapa pertanyaan dan tidak untuk yang lain.

Struktur folder memiliki hierarki tetapi hanya satu jalur.
Sebuah file hanya milik satu folder.
Hanya jalur "Samsung Electronics/Keuangan/Laba operasional" yang ada.
Ketika pertanyaan tentang "industri semikonduktor" masuk, eksplorasi alami melalui struktur folder ini tidak mungkin.

Graph memiliki hierarki dan jalur yang beragam.
Satu node bisa terhubung ke beberapa node induk.
Node Samsung Electronics bisa dicapai melalui jalur "Korporasi," jalur "Industri semikonduktor," atau jalur "Perusahaan tercatat di KOSPI."
Dari konteks mana pun sebuah pertanyaan berasal, jalur alami ada.

---

## Ini Adalah Masalah yang Belum Terpecahkan

Ada sesuatu yang harus dikatakan dengan jujur.

Kebutuhan akan eksplorasi multi-langkah jelas.
Tetapi belum ada sistem standar yang mengimplementasikan ini secara efektif.

Bagaimana Anda secara otomatis menghasilkan hierarki peta?
Bagaimana Anda menentukan ukuran tepat setiap lapisan?
Apa yang terjadi ketika agen memilih arah yang salah?
Apa yang terjadi pada latensi seiring kedalaman eksplorasi bertambah?

Ini adalah pertanyaan terbuka.

Tetapi fakta bahwa suatu masalah belum terpecahkan
tidak berarti masalah itu tidak ada.

Pengetahuan bertumbuh.
Jendela terbatas.
Titik di mana pencarian saja tidak cukup sedang datang.

Eksplorasi harus siap sebagai jawaban untuk titik itu.
Jika tidak siap,
satu-satunya pilihan yang tersisa adalah memperbesar jendela atau membuang pengetahuan.

---

## Ringkasan

Pencarian mengembalikan hasil dengan satu kueri.
Ketika skala pengetahuan cukup besar, ini tidak memadai.
Karena indeks itu sendiri melebihi jendela.

Eksplorasi mengikuti peta hierarkis, memilih arah sambil turun.
Apa yang harus dilihat di setiap langkah muat di jendela.
Setiap langkah terbatas terlepas dari skala total.
Sama seperti B-tree menemukan data tanpa memuat seluruh disk ke memori.

Agen menilai arah di setiap langkah.
Konstruksi konteks bergeser dari perakitan statis ke eksplorasi dinamis.
Di sinilah context engineering bertemu desain agen.

Agar eksplorasi berhasil, pengetahuan harus hierarkis, setiap lapisan harus terbatas, dan jalur harus beragam.
Struktur folder hanya memiliki satu jalur. Graph memiliki jalur yang beragam.

Ini masih masalah yang belum terpecahkan tanpa solusi standar.
Tetapi selama pengetahuan bertumbuh dan jendela terbatas, ini adalah masalah yang harus dipecahkan.

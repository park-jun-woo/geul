---
title: "Mengapa Vektor Embedding Tidak Cukup"
weight: 11
date: 2026-02-26T12:00:18+09:00
lastmod: 2026-02-26T12:00:18+09:00
tags: ["embedding", "vektor", "kotak putih"]
summary: "Menata ulang vektor embedding akan merusak model. Menghindari kerusakan berarti membangun ulang model dari nol. Yang dibutuhkan bukan transparansi di dalam kotak hitam, melainkan lapisan transparan di luarnya."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Vektor bagus untuk komputasi, tetapi mustahil ditafsirkan. Anda tidak bisa membuat isi kotak hitam menjadi transparan.

---

## Vektor embedding adalah teknologi yang luar biasa

"Raja - Pria + Wanita = Ratu."

Ketika word2vec menunjukkan ini, dunia tercengang.
Representasikan kata-kata sebagai vektor berdimensi ratusan,
dan hubungan semantik muncul sebagai operasi vektor.

Vektor embedding adalah fondasi LLM.
Segala sesuatu dalam transformer adalah komputasi vektor.
Token menjadi vektor.
Attention menghitung kemiripan antar vektor.
Output dikonversi dari vektor kembali menjadi token.

Makna yang mirip adalah vektor yang berdekatan.
Makna yang berbeda adalah vektor yang berjauhan.
Pencarian adalah perhitungan kemiripan vektor.
Klasifikasi adalah penetapan batas dalam ruang vektor.

Tanpa vektor embedding, AI saat ini tidak akan ada.

Lalu, mengapa tidak menggunakan vektor embedding untuk merepresentasikan pengetahuan?
Menyejajarkannya secara langsung, menyusunnya, membuatnya dapat ditafsirkan.

Tidak bisa.
Cara paling pasti untuk mengetahuinya adalah dengan mencoba.

---

## AILEV: Kami sudah mencoba

Proyek GEUL awalnya dimulai dengan nama AILEV.

AI Language Embedding Vector.

Namanya sendiri menyatakan tujuannya:
bahasa AI yang memanipulasi vektor embedding secara langsung.

Konsepnya seperti ini:

Merepresentasikan makna dengan vektor 512 dimensi.
Memberikan peran pada segmen-segmen vektor.
128 dimensi pertama untuk entitas, 128 berikutnya untuk relasi, 128 berikutnya untuk properti, sisanya untuk metadata.
Sebagaimana RGBA menguraikan warna menjadi empat kanal, menguraikan makna menjadi segmen-segmen dimensional.

Melatih BERT untuk mengonversi bahasa alami menjadi vektor terstruktur ini.
Saat dimasukkan "Seoul adalah ibu kota Korea",
segmen entitas menghasilkan vektor Seoul, segmen relasi menghasilkan vektor ibu kota, segmen properti menghasilkan vektor Korea.

Karena berupa vektor, komputasi dimungkinkan.
Pencarian kemiripan dimungkinkan.
Mengurangi dimensi memberikan degradasi anggun.
Dari 512 ke 256 dimensi, presisi menurun tetapi makna inti tetap terjaga.

Elegan. Secara teori.

---

## Mengapa gagal

### Menata ulang vektor secara sembarang merusak model

Vektor embedding LLM adalah produk pelatihan.

Setelah membaca miliaran teks,
model mengoptimalkan representasi internalnya sendiri.
Apa arti setiap dimensi adalah sesuatu yang diputuskan oleh model.
Bukan oleh manusia.

Apa yang terjadi jika Anda menetapkan "128 dimensi pertama untuk entitas"?

Dalam ruang vektor yang dipelajari model,
informasi entitas tidak berada di 128 dimensi pertama.
Ia tersebar di seluruh 768 dimensi.
Informasi relasi, informasi properti, informasi kala waktu — semuanya tercampur.

Ini bukan kesalahan desain, melainkan hakikat pembelajaran.
Backpropagation mencari
susunan vektor yang optimal untuk tugas.
Bukan susunan yang dapat ditafsirkan.
Optimal dan dapat ditafsirkan bukan hal yang sama.

Jika Anda memaksa menata ulang vektor — "entitas di sini, relasi di sana" —
hubungan statistik yang dipelajari model akan rusak.
Performa menurun.

### Menata ulang tanpa merusak berarti membangun ulang model

Lalu, mengapa tidak melatih dari awal dengan batasan "128 dimensi pertama untuk entitas"?

Bisa. Secara teori.
Tetapi ini bukan menyelaraskan vektor embedding.
Ini merancang arsitektur model baru.

Diperlukan data pelatihan. Miliaran token.
Diperlukan infrastruktur pelatihan. Ribuan GPU.
Diperlukan waktu pelatihan. Berbulan-bulan.
Dan tidak ada jaminan model yang dihasilkan akan bekerja sebaik LLM yang ada.

Upayanya terlalu besar.

Masalah "menyelaraskan vektor agar dapat ditafsirkan"
berubah menjadi "membangun ulang LLM dari nol".
Ini bukan memecahkan masalah, melainkan memperbesarnya.

### Penafsiran tidak mungkin

Anggaplah Anda berhasil membuat vektor terstruktur.
Vektor 512 dimensi.
Katakanlah 128 dimensi pertama untuk entitas.

Segmen entitas bernilai `[0.23, -0.47, 0.81, 0.12, ...]`.

Bagaimana Anda tahu apakah ini "Samsung Electronics" atau "Hyundai Motor"?

Anda harus menemukan vektor terdekat.
Anda harus menghitung kemiripan di basis data vektor.
Dan Anda mendapat jawaban probabilistik: "mungkin Samsung Electronics."

"Mungkin."

Vektor pada dasarnya kontinu.
Antara vektor Samsung Electronics dan SK Hynix
terdapat tak terhingga vektor perantara.
Tidak ada yang tahu apa arti vektor-vektor perantara itu.

Ini bukan keterbatasan teknis, melainkan kebenaran matematis.
Merepresentasikan makna diskret dalam ruang kontinu
membuat batas menjadi kabur.
Kekaburan itulah [masalah bahasa alami](/id/why/natural-language-hallucination/).
Kita beralih ke vektor, dan kekaburan muncul kembali.

Hanya bentuknya yang berubah.
Dalam bahasa alami, kekaburan kata.
Dalam vektor, kekaburan koordinat.

---

## Prinsip kotak putih

Di sinilah masalah desain fundamental terungkap.

Vektor embedding adalah kotak hitam.
Melihat vektor bernilai riil berdimensi 768,
tidak ada yang bisa mengetahui informasi apa yang dikodekan di mana.
Model sendiri pun tidak bisa menjelaskannya.

Ini bukan sifat yang merepotkan, melainkan properti ontologis.
Inilah tepatnya mengapa vektor bekerja.
Karena mereka menyusun informasi dengan cara yang tidak dirancang manusia,
mereka bekerja lebih baik daripada apa pun yang dirancang manusia.
Ketidakmampuan untuk ditafsirkan bukan cacat, melainkan fitur.

Namun pengetahuan yang digunakan sebagai konteks AI menuntut hal sebaliknya.

Perlu diketahui sumbernya.
Perlu diketahui waktu pencatatannya.
Perlu diketahui tingkat keyakinannya.
Perlu diketahui tentang apa pernyataan tersebut.
Perlu diketahui apakah dua pernyataan merujuk pada entitas yang sama.

Setiap kebutuhan adalah "perlu diketahui". Setiap kebutuhan menuntut kemampuan tafsir.

Memenuhi tuntutan kotak putih dengan vektor kotak hitam
adalah kontradiksi.

---

## Logika perpindahan

Perpindahan dari AILEV ke GEUL bukan mundur.
Melainkan mendefinisikan ulang masalah.

**Masalah awal:** LLM adalah kotak hitam. Mari buat dalamnya transparan.
→ Mari buat vektor embedding dapat ditafsirkan dengan menyelaraskannya.
→ Menyentuh vektor merusak model.
→ Menghindari kerusakan berarti membangun ulang model.
→ Jalan buntu.

**Masalah yang didefinisikan ulang:** Tidak perlu membuat isi kotak hitam transparan. Mari buat lapisan transparan di luar.
→ Bagian dalam LLM tidak disentuh.
→ Di luar LLM, diciptakan sistem representasi yang dapat ditafsirkan.
→ LLM dapat membaca dan menulis sistem itu. Karena berupa token.
→ Bahasa buatan.

Bukan vektor, melainkan bahasa.
Bukan kontinu, melainkan diskret.
Bukan tidak dapat ditafsirkan, melainkan penafsiran sebagai satu-satunya tujuan.
Bukan di dalam model, melainkan di luar model.

"Embedding Vector" dari AILEV dihilangkan,
dan lahirlah GEUL — yang berarti "tulisan". Inilah alasannya.

---

## Vektor untuk komputasi, bahasa untuk representasi

Ini bukan penolakan terhadap vektor embedding.

Vektor dioptimalkan untuk komputasi.
Pencarian kemiripan, pengelompokan, klasifikasi, pengambilan data.
Bahasa tidak bisa menggantikan apa yang dilakukan vektor.

Bahasa dioptimalkan untuk representasi.
Identitas entitas, deskripsi relasi, metadata tertanam, kemampuan tafsir.
Vektor tidak bisa menggantikan apa yang dilakukan bahasa.

Keduanya adalah alat di lapisan yang berbeda.

Di dalam LLM, vektor bekerja. Kotak hitam. Memang seharusnya begitu.
Di luar LLM, bahasa bekerja. Kotak putih. Memang seharusnya begitu.

Masalah dimulai ketika kedua lapisan ini dicampuradukkan.
Kita mencoba membuat vektor melakukan pekerjaan bahasa.
Kita mencoba memberikan kotak hitam peran kotak putih.

Masing-masing punya tempatnya.

---

## Ringkasan

Vektor embedding adalah fondasi LLM dan teknologi yang luar biasa.
Namun sebagai sarana representasi pengetahuan, ia memiliki keterbatasan fundamental.

GEUL dimulai sebagai AILEV (AI Language Embedding Vector).
Tujuannya menyelaraskan vektor secara langsung dan membuatnya dapat ditafsirkan.
Gagal. Karena dua alasan.

Menyelaraskan vektor secara sembarang merusak hubungan yang dipelajari model.
Menyelaraskan tanpa merusak berarti membangun ulang model dari nol. Upayanya terlalu besar.

Dan bahkan jika berhasil, vektor tidak dapat ditafsirkan.
Dalam ruang kontinu, batas makna diskret itu kabur.
Tidak bisa memberikan kotak hitam peran kotak putih.

Logika perpindahan:
Berusaha membuat isi kotak hitam transparan.
Menyentuh isinya akan merusaknya.
Sebagai gantinya, biarkan isinya dan bangun lapisan transparan di luar.
Bukan vektor melainkan bahasa. Bukan di dalam model melainkan di luar model.

Vektor untuk komputasi, bahasa untuk representasi.
Masing-masing punya tempatnya.

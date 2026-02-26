---
title: "Mengapa 16-Bit?"
weight: 16
date: 2026-02-26T12:00:04+09:00
lastmod: 2026-02-26T12:00:04+09:00
tags: ["16-bit", "biner", "stream"]
summary: "Satu kata menembus tiga dunia"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Satu Kata Menembus Tiga Dunia

---

## Tiga Dunia

Ada tiga dunia dalam ilmu komputer.

**Dunia jaringan.**
Data mengalir sebagai stream byte.
Byte masuk melalui soket TCP, dan byte keluar.
Kosakata insinyur jaringan adalah paket, header, dan payload.

**Dunia penyimpanan.**
Data disimpan secara persisten dalam format file.
Ditulis ke disk, dibaca dari disk.
Kosakata insinyur penyimpanan adalah blok, offset, dan alignment.

**Dunia AI.**
Data diproses sebagai urutan token.
LLM menerima token sebagai input dan menghasilkan token sebagai output.
Kosakata insinyur AI adalah embedding, attention, dan konteks.

Ketiga dunia ini berbicara dalam bahasa yang berbeda.
Dan di antara mereka, penerjemahan selalu diperlukan.

---

## Biaya Penerjemahan

Mari kita telusuri jalur yang dilalui data dalam sistem AI modern.

Pengetahuan disimpan dalam file. Sebagai JSON atau teks biasa.

Untuk menyampaikan ini kepada AI:

1. Buka file dan baca teksnya.
2. Parse teksnya. Jika JSON, interpretasikan struktur dan ekstrak field.
3. Masukkan teks yang diekstrak ke tokenizer.
4. Tokenizer mengubah teks menjadi urutan ID token.
5. Urutan token dimasukkan ke LLM.

Ketika AI menghasilkan respons:

6. LLM menghasilkan urutan token.
7. Decode token kembali menjadi teks.
8. Serialisasi teks ke format terstruktur.
9. Tulis data yang diserialisasi ke file.

Operasi sederhana "baca dan tulis" membutuhkan sembilan langkah.

Setiap langkah membutuhkan waktu.
Setiap langkah membutuhkan memori.
Setiap langkah berisiko kehilangan informasi.

Langkah 3 dan 4 -- proses tokenisasi -- terkenal bermasalah.
Karena batas kata dalam bahasa alami tidak sejajar dengan batas token tokenizer,
nama diri seperti "Yi Sun-sin" bisa dipecah menjadi fragmen sembarang,
atau satu unit semantik tersebar di beberapa token.

Inilah harga dari tiga dunia yang berbicara bahasa berbeda.

---

## Bagaimana Jika Satu Unit Menembus Ketiga Dunia?

Dalam bahasa ini, satu kata adalah 16 bit (2 byte).

Satu kata 16-bit secara bersamaan adalah tiga hal.

**Unit dari byte stream.**
Kata 16-bit datang dalam aliran kontinu melalui jaringan.
Big Endian. Disejajarkan pada batas 2-byte. Tidak perlu parsing tambahan.
Cukup baca sesuai urutan kedatangan.

**Unit dari format file.**
Tulis stream langsung ke disk, dan itulah file Anda.
Baca byte langsung dari disk dan kirimkan melalui jaringan, dan itulah stream Anda.
Tanpa serialisasi. Tanpa deserialisasi.

**Unit dari token LLM.**
16 bit = 65.536 simbol berbeda.
Ukuran kosakata LLM modern umumnya berkisar dari 50.000 hingga 100.000.
Model keluarga GPT menggunakan sekitar 50.000; model khusus bahasa Korea sekitar 100.000.
65.536 tepat di tengah rentang tersebut.
Satu kata 16-bit menjadi satu token LLM.

Tiga dunia berbagi unit yang sama.
Penerjemahan menghilang.

---

## Nol Konversi, Nol Kehilangan, Nol Overhead

Mari kita lihat apa artinya secara konkret.

**Pendekatan konvensional: 9 langkah**

```
[File] -> Baca -> Parse -> Ekstrak teks -> Tokenisasi -> [LLM]
[LLM] -> Decode -> Serialisasi -> Tulis -> [File]
```

**Pendekatan binary stream: 1 langkah**

```
[File/Stream] -> [LLM]
[LLM] -> [File/Stream]
```

Baca file, dan itu sudah menjadi urutan token.
Tulis urutan token yang dihasilkan LLM, dan itu sudah menjadi file.
Ambil stream dari jaringan dan masukkan langsung ke LLM.

Nol konversi. Nol parsing. Nol tokenisasi.
Nol kehilangan. Nol overhead.

---

## Mengapa Bukan 8-Bit?

8 bit memberikan 256 simbol berbeda.

256 simbol terlalu sedikit untuk merepresentasikan dunia.
Alokasikan alfabet, digit, dan tanda baca dasar, dan setengah ruang sudah terpakai.

Jika Anda menggunakan 8 bit sebagai unit fundamental,
sebagian besar token yang bermakna membutuhkan 2 byte atau lebih.
Ini memaksa encoding panjang variabel,
dan panjang variabel membuat parsing menjadi kompleks.

Cukup sebagai unit byte stream,
tetapi tidak cukup sebagai unit token.

---

## Mengapa Bukan 32-Bit?

32 bit memberikan sekitar 4,3 miliar simbol berbeda.

Daya ekspresif lebih dari cukup -- jauh lebih dari yang diperlukan.
Tetapi masalahnya adalah efisiensi.

Paket paling sering muncul dalam format ini adalah Tiny Verb Edge, berukuran 2 kata.
Pada 16 bit per kata, itu 4 byte. Pada 32 bit per kata, menjadi 8 byte.
Paket paling umum berlipat ganda ukurannya.

Dari perspektif LLM, juga ada masalah.
Jika satu token adalah 32 bit, hanya setengah jumlah token yang muat di jendela konteks yang sama.
Mengingat panjang konteks LLM adalah sumber daya langka saat ini,
ruang yang ditempati token menjadi tidak efisien relatif terhadap informasi yang dibawanya.

Kata 32-bit terlalu berlebihan sebagai token untuk bahasa ini.

---

## Mengapa Bukan Panjang Variabel?

UTF-8 adalah encoding panjang variabel.
Panjang karakter berkisar dari 1 byte hingga 4 byte tergantung pada karakternya.

Ini menawarkan keunggulan dalam efisiensi penyimpanan,
tetapi memperkenalkan kelemahan fatal dalam efisiensi pemrosesan.

Untuk menemukan karakter ke-n, Anda harus menghitung dari awal.
Akses acak tidak mungkin.
Pemrosesan paralel SIMD menjadi sulit.

Bahasa ini menggunakan kata 16-bit dengan lebar tetap sebagai unit fundamental.
Posisi kata ke-n selalu n * 2 byte.
Akses acak O(1).
SIMD dapat membandingkan beberapa kata dalam satu instruksi.
GPU dapat memindai miliaran kata secara paralel.

Namun di tingkat paket, panjang variabel tetap diizinkan.
Tiny Verb Edge adalah 2 kata; Event6 Edge bisa hingga 8 kata.
Unit kata tetap, tetapi unit paket fleksibel.

Efisiensi pemrosesan lebar tetap dikombinasikan dengan daya ekspresif panjang variabel.
Kata 16-bit mencapai keduanya secara bersamaan.

---

## Jalur yang Dibuktikan Unicode

Unicode adalah standar encoding paling sukses yang pernah diciptakan umat manusia.

Unit dasar UTF-16 adalah 16 bit (2 byte).
Ia merepresentasikan 65.536 karakter Basic Multilingual Plane (BMP) dalam satu kata,
dan memperluas ke karakter di luarnya menggunakan surrogate pair (2 kata = 4 byte).

Kita cukup mengikuti struktur yang telah terbukti ini.

Merepresentasikan 65.536 primitif semantik dasar dalam satu kata,
dan memperluas paket gabungan ke beberapa kata.

Seperti halnya Unicode mengekspresikan setiap karakter di dunia
di atas unit dasar "satu karakter = 2 byte,"
bahasa ini mengekspresikan setiap elemen penalaran AI
di atas unit dasar "satu kata = 2 byte."

---

## Kompatibilitas Mundur dan Perluasan ke Atas

Kekuatan lain dari 16 bit adalah alignment.

16 adalah kelipatan 8, pembagi 32, pembagi 64, dan pembagi 128.

Ini berarti alignment tidak pernah rusak, ke arah mana pun Anda memperluas.

Bagaimana jika arsitektur transformer berubah di masa depan
dan token menjadi 32 bit?
Dua kata 16-bit membuat satu token. Tidak ada masalah alignment.

Bagaimana dengan 64 bit?
Empat kata 16-bit membuat satu token. Tetap tidak ada masalah alignment.

Sebaliknya, bagaimana jika sistem embedded 8-bit memproses format ini?
Cukup baca setiap kata 16-bit sebagai byte tinggi dan byte rendah.

Kompatibilitas mundur harus dijaga secara absolut.
Kata 16-bit menjamin ini di tingkat fisik.

Kita tidak dapat memprediksi ukuran kata kecerdasan masa depan,
tetapi alignment kelipatan 16 bit menjamin kompatibilitas dengan ukuran apa pun.

---

## Struktur Tiga Rangkap

Mari kita ringkaskan.

Satu kata 16-bit secara bersamaan adalah tiga hal.

| Dunia | Peran Satu Kata |
|-------|---------------------|
| Jaringan | Unit dari byte stream |
| Penyimpanan | Unit dari format file |
| AI | Unit dari token LLM |

Satu unit menembus ketiga dunia.

Simpan stream apa adanya, dan itu adalah file.
Baca file apa adanya, dan itu adalah token.
Kirim token apa adanya, dan itu adalah stream.

Tanpa konversi.
Tanpa penerjemahan.
Tanpa kehilangan.

Inilah mengapa 16-bit.
Bukan 8-bit, bukan 32-bit, bukan panjang variabel.
Angka yang terletak tepat di persimpangan tiga dunia.

16.

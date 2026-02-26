---
title: "Mengapa Indeks yang Selaras Secara Semantik?"
weight: 15
date: 2026-02-26T12:00:03+09:00
lastmod: 2026-02-26T12:00:03+09:00
tags: ["SIDX", "penyelarasan semantik", "indeks"]
summary: "Ketika makna diukir dalam bit, pencarian menjadi penalaran"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Apa yang Terjadi Ketika ID Adalah Pengetahuan, Bukan Alamat

---

## Alamat Tidak Tahu Apa-Apa

Untuk menemukan Yi Sun-sin dalam database, Anda membutuhkan ID.

Di Wikidata, ID Yi Sun-sin adalah `Q8492`.

Angka ini menunjuk ke Yi Sun-sin.
Tetapi string `Q8492` itu sendiri tidak tahu apa-apa.

Ia tidak tahu apakah ini orang atau gedung.
Ia tidak tahu apakah ini warga Korea atau warga Prancis.
Ia tidak tahu apakah ini tokoh abad ke-16 atau abad ke-21.
Ia tidak tahu apakah mereka hidup atau mati.

`Q8492` adalah alamat.
Tukang pos yang mengantar surat tidak tahu apa yang tertulis di dalam amplop.
Mereka hanya melihat alamat pada amplop dan mengantarkannya.

UUID sama saja. `550e8400-e29b-41d4-a716-446655440000`.
128 bit angka acak. Unik hanya untuk menghindari tabrakan --
tidak memberi tahu apa-apa tentang apa yang dirujuknya.

Selama lima puluh tahun terakhir, ID database bekerja seperti ini.
ID adalah alamat, dan untuk mengetahui apa pun, Anda harus mengikuti alamat itu dan membaca datanya.

---

## Harus Mengikuti untuk Mengetahui

Mengapa ini masalah?

Misalkan Anda ingin menemukan "seorang filsuf pria berkewarganegaraan Jerman yang lahir di abad ke-19."

Dalam database tradisional, begini cara kerjanya:

```
1. Filter tabel persons di mana gender = 'male'
2. JOIN dengan tabel nationalities dan filter country = 'Germany'
3. JOIN dengan tabel birth_dates dan filter year BETWEEN 1800 AND 1899
4. JOIN dengan tabel occupations dan filter occupation = 'philosopher'
```

Empat operasi JOIN.
Setiap JOIN membandingkan baris antara dua tabel.
Jika tabelnya besar, ia menelusuri indeks; jika tidak ada indeks, ia melakukan full scan.
Dengan satu miliar rekaman, proses ini memakan waktu detik hingga puluhan detik.

Mengapa begitu kompleks?

Karena ID tidak tahu apa-apa.
Melihat `Q8492`, Anda tidak bisa tahu apakah ini orang Jerman atau Korea,
sehingga Anda harus pergi ke tabel lain untuk mengambil informasi itu.

Untuk setiap pertanyaan, Anda harus mengikuti ke mana ID menunjuk.
Inilah biaya yang dibayar database selama lima puluh tahun.

---

## Bagaimana Jika ID Sudah Tahu?

Mari kita balik premisnya.

Bagaimana jika ID itu sendiri mengandung informasi esensial?

Bagaimana jika, hanya dengan melihat ID,
Anda bisa tahu apakah ia merujuk pada manusia, dari negara mana mereka,
dari era mana mereka, dan bagaimana mereka diklasifikasikan?

Untuk menemukan "filsuf pria Jerman abad ke-19,"
JOIN menjadi tidak diperlukan.

Memindai satu miliar ID,
Anda bisa langsung menentukan kecocokan masing-masing dengan memeriksa bit-bitnya.

Inilah ide inti di balik Indeks yang Selaras Secara Semantik.

---

## Menyelaraskan Makna ke dalam ID

SIDX (Semantically-Aligned Index) adalah pengidentifikasi 64-bit.

64 bit ini bukan angka acak.
Makna ditetapkan pada posisi setiap bit.

Bit atas menyimpan informasi paling penting.
Jenis entitas apa ini? Orang, tempat, peristiwa, konsep?

Bit berikutnya menyimpan informasi klasifikasi.
Jika itu orang, dari era apa? Dari wilayah mana?

Bit bawah membawa informasi yang semakin spesifik.

Prinsip kuncinya adalah:

> Urutan bit adalah urutan kepentingan informasi.

Klasifikasi paling fundamental di atas,
pembedaan paling halus di bawah.

Ini bukan sekadar penyortiran.
Ini adalah filosofi desain.

---

## Dari Satu Miliar ke Sepuluh Ribu, dalam Satu Kali Lewat

Kekuatan praktis SIDX terlihat dalam angka-angka.

WMS menyimpan satu miliar entitas.
SIDX setiap entitas adalah 64 bit.
Total ukuran: 1 miliar x 8 byte = 8 GB.

8 GB ini muat sepenuhnya di memori.

Anda ingin menemukan "entitas yang merupakan manusia dan berasal dari Asia Timur."
Bit atas mengandung flag "manusia" dan kode "Asia Timur,"
sehingga Anda bisa memfilter dengan satu bitmask.

```
mask   = 0xFF00_0000_0000_0000  (8 bit atas: tipe + wilayah)
target = 0x8100_0000_0000_0000  (manusia + Asia Timur)

for each sidx in 1_billion:
    if (sidx & mask) == target:
        add to candidates
```

Operasi ini dapat diparalelkan dengan SIMD.
Dengan AVX-512, Anda membandingkan 8 SIDX sekaligus dalam satu instruksi.
Memindai 1 miliar entri: sekitar 12 milidetik.

Di GPU? Kurang dari 1 milidetik.

Satu miliar rekaman dipersempit menjadi sepuluh ribu.
Memfilter sepuluh ribu sisanya secara detail bersifat instan.

Nol JOIN.
Nol penelusuran pohon indeks.
Hanya satu bitwise AND.

---

## Mengapa 64 Bit Cukup

Awalnya, saya pikir ruang yang lebih besar diperlukan.

32 byte (256 bit). Vektor FP16 32-dimensi.
Saya mencoba memasukkan setiap atribut kunci entitas ke dalam ID.
Apakah mereka manusia, gender, kewarganegaraan, era, pekerjaan, wilayah, status hidup, jalur klasifikasi...

Tetapi kemudian saya menyadari sesuatu.

**ID tidak perlu tahu segalanya.**

Ia hanya perlu mempersempit satu miliar rekaman menjadi sepuluh ribu.
WMS menangani sisanya.

Bayangkan ini sebagai pos pemeriksaan.
Di gerbang tol jalan tol, untuk menentukan bahwa
"kendaraan ini menuju ke Provinsi Gyeonggi" dari plat nomor,
Anda tidak perlu tahu apa yang dimuat di bagasi.

64 bit cukup.
Gunakan bit atas untuk menangkap tipe dan klasifikasi luas,
dan bit bawah untuk klasifikasi lebih halus.
64 bit lebih dari cukup untuk mempersempit satu miliar rekaman menjadi sepuluh ribu.

Dan 64 bit = empat kata 16-bit.
Mereka mengalir secara natural dalam stream.
ID 32-byte akan membuat stream berat,
tetapi SIDX 64-bit ringan dan cepat.

---

## Degradasi Anggun: Makna Bertahan Bahkan Ketika Bit Dipotong

Kekuatan lain dari penyelarasan semantik adalah karakteristik degradasinya.

Karena bit SIDX diurutkan dari yang paling penting ke yang paling tidak penting,
bahkan jika bit bawah rusak atau terpotong,
informasi inti di bit atas tetap terjaga.

```
64 bit penuh:  "Yi Sun-sin, komandan angkatan laut Joseon abad ke-16"
48 bit:        "Perwira militer Joseon abad ke-16"
32 bit:        "Manusia Asia Timur abad ke-16"
16 bit:        "Manusia"
8 bit:         "Entitas fisik"
```

Seiring informasi terpotong, spesifisitas hilang,
tetapi klasifikasi paling fundamental bertahan hingga akhir.

Ini adalah implementasi di tingkat bit dari prinsip "degradasi anggun."

Bahkan jika gangguan jaringan hanya mengirimkan data parsial,
sistem tahu "Saya tidak tahu persis siapa ini, tetapi setidaknya ini cerita tentang manusia"
dan dapat melanjutkan penalaran.

Garis besar yang kabur lebih baik dari keheningan total.
Pemahaman parsial lebih baik dari kegagalan total.

---

## Kueri Menjadi ID

Kemungkinan paling menarik yang dibuka oleh pengindeksan yang selaras secara semantik
adalah ini: kueri bahasa alami dapat diubah menjadi SIDX sementara.

Pengguna bertanya: "Siapa jenderal yang mengalahkan angkatan laut Jepang selama Perang Imjin?"

Encoder menganalisis pertanyaan ini.
Manusia. Asia Timur. Abad ke-16. Berkaitan dengan militer.
Merakit atribut-atribut ini ke dalam bit menghasilkan SIDX sementara.

SIDX sementara ini memindai satu miliar SIDX di WMS.
Entitas yang pola bitnya paling mirip muncul sebagai kandidat.
Yi Sun-sin, Won Gyun, Gwon Yul, Yi Eok-gi...

Merujuk silang informasi detail terhadap kandidat-kandidat ini menghasilkan jawaban akhir.

Ini menyatukan pencarian dan penghubungan entitas dalam satu mekanisme.
Tidak perlu mesin pencari terpisah.
Tidak perlu pipeline NER (Named Entity Recognition) terpisah.
Satu perbandingan SIDX sudah cukup.

---

## Mengapa Bukan B-Tree?

Database tradisional menggunakan indeks B-Tree.

B-Tree unggul dalam menemukan nilai spesifik dalam data terurut dalam O(log n).
Untuk "temukan Q8492," mereka optimal.

Tetapi untuk "temukan semua entitas yang merupakan manusia dan berasal dari Asia Timur," mereka lemah.
Pencarian kondisi gabungan membutuhkan perpotongan beberapa indeks,
dan biaya perpotongan meningkat tajam dengan skala data.

SIDX + pemindaian menyeluruh SIMD mengambil pendekatan yang secara fundamental berbeda.

Jika B-Tree adalah buku telepon yang cepat menjawab "siapa yang tinggal di alamat ini,"
pemindaian SIDX adalah profiling yang cepat menjawab "siapa yang memiliki karakteristik ini."

Sifat pertanyaannya berbeda, dan demikian pula struktur data optimalnya.

| Tipe Kueri | B-Tree | Pemindaian SIDX |
|-----------|--------|-----------|
| Pencarian berdasarkan ID spesifik | O(log n), optimal | Tidak diperlukan (gunakan hash) |
| Penyaringan kondisi gabungan | Membutuhkan JOIN, lambat | Satu bitwise AND, cepat |
| Pencarian entitas serupa | Tidak mungkin | Mungkin melalui kesamaan vektor |
| Penyisipan | O(log n), rebalancing | O(1), append |
| Kompleksitas implementasi | Tinggi | Rendah |

WMS tidak menggunakan B-Tree.
Ia memuat satu miliar SIDX ke memori
dan melakukan pemindaian menyeluruh dengan bitmask SIMD.

Sederhana. Brute-force. Cepat.

---

## Kebijaksanaan Huffman

Struktur alokasi bit SIDX mengikuti prinsip pengodean Huffman.

Dalam pengodean Huffman, simbol yang sering muncul menerima kode lebih pendek,
dan simbol yang jarang muncul menerima kode lebih panjang.

Dalam SIDX, informasi klasifikasi yang paling sering dibutuhkan menempati bit atas,
dan detail yang jarang dibutuhkan menempati bit bawah.

Prinsip yang sama mengatur prefix tipe paket bahasa ini.
Tiny Verb Edge berfrekuensi tertinggi mendapat prefix terpendek.
Event6 Edge berfrekuensi rendah mendapat prefix lebih panjang.

Kebijaksanaan Huffman mengalir melalui setiap lapisan desain ini.
Tidak satu bit pun terbuang.
Biaya terendah untuk hal terpenting.

---

## Ringkasan

ID tradisional adalah alamat. Alamat tidak tahu apa-apa.

1. Ketika ID tidak membawa makna, Anda harus mengikutinya ke data setiap kali. Itulah JOIN.
2. Empat JOIN melintasi satu miliar rekaman itu lambat.
3. SIDX mengodekan makna langsung ke dalam ID melalui penyelarasan semantik.
4. Satu bitmask AND mempersempit satu miliar rekaman menjadi sepuluh ribu. Nol JOIN.
5. 64 bit cukup. ID tidak perlu tahu segalanya -- ia hanya perlu mempersempit kandidat.
6. Karena informasi terpenting menempati bit atas, makna inti bertahan bahkan ketika bit terpotong.
7. Mengubah kueri bahasa alami menjadi SIDX sementara mengubah pencarian menjadi operasi vektor.

Saat ID berhenti menjadi alamat dan menjadi pengetahuan,
aturan database berubah.

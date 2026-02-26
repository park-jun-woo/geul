---
title: "Mengapa Wikidata"
weight: 13
date: 2026-02-26T12:00:17+09:00
lastmod: 2026-02-26T12:00:17+09:00
tags: ["Wikidata", "Ontologi", "SIDX"]
summary: "GEUL tidak menolak Wikidata. GEUL mengubah sistem klasifikasi dan statistik frekuensi dari 100 juta entitas menjadi buku kode SIDX. Membangun tata bahasa di atas kamus."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## GEUL tidak menolak Wikidata. GEUL berdiri di atasnya.

---

## Bahasa tidak bisa dibuat tanpa kamus

Setiap bahasa membutuhkan kosakata.

Bahasa Korea punya kamus Korea.
Bahasa Inggris punya kamus Inggris.
Bahasa pemrograman punya pustaka standar.

Hal yang sama berlaku untuk bahasa buatan.
Daftar entitas, daftar relasi, daftar properti.
Kode apa yang mewakili "Samsung Electronics" dalam bahasa ini?
Kode apa yang mewakili relasi "ibu kota"?
Kosakata harus ada sebelum kalimat bisa ditulis.

Bagaimana membangun kosakata ini?
Ada dua cara.

Membangunnya dari nol.
Atau menggunakan yang sudah ada.

---

## Membangun dari nol: pelajaran dari CYC

Proyek CYC dimulai pada 1984.

Tujuannya adalah memformalisasi dan menyimpan pengetahuan akal sehat secara umum.
Ontologinya dirancang dari awal.
Konsep didefinisikan, relasi didefinisikan, aturan didefinisikan.
Para ahli memasukkannya secara manual.

Tiga puluh tahun berlalu.
Jutaan aturan dimasukkan.

Namun itu masih sangat jauh dari cukup untuk mencakup pengetahuan dunia.
Setiap domain memerlukan ontologi terpisah.
Menjaga konsistensi antaromain terbukti sulit.
Setiap kali muncul konsep baru, ontologi harus direvisi.
Revisi sering bertentangan dengan aturan yang sudah ada.

Yang dibuktikan CYC bukan potensinya, melainkan batasannya.
Membiarkan tim kecil ahli merancang ontologi dunia
menjadi tidak bisa dipertahankan seiring bertambahnya skala.

---

## Yang sudah ada: Wikidata

Wikidata diluncurkan pada 2012.

Basis pengetahuan terstruktur yang dioperasikan oleh Wikimedia Foundation.
Siapa pun bisa mengeditnya.
Pada 2024, berisi lebih dari 100 juta entitas.
Lebih dari 10.000 properti.
Miliaran pernyataan.
Label dalam lebih dari 300 bahasa.

Skala yang CYC tidak bisa capai dalam 30 tahun dengan tim ahli,
Wikidata capai dalam 10 tahun dengan komunitas.

Mari lihat apa yang Wikidata sediakan.

**Pengidentifikasi entitas.** Q-ID. Samsung Electronics adalah Q20718. Seoul adalah Q8684. Yi Sun-sin adalah Q217300. Pengidentifikasi unik secara global. Tidak bergantung pada bahasa.

**Pengidentifikasi properti.** P-ID. "Lokasi kantor pusat" adalah P159. "Tanggal pendirian" adalah P571. "Populasi" adalah P1082. Relasi dan properti diidentifikasi secara unik.

**Struktur hierarkis.** P31 (instance of) dan P279 (subclass of) membentuk hierarki tipe. "Seoul → kota → permukiman manusia → entitas geografis." Sistem klasifikasi dunia diekspresikan melalui dua properti ini.

**Label multibahasa.** Label Korea untuk Q20718 adalah "삼성전자", label Inggris adalah "Samsung Electronics", label Jepang adalah "サムスン電子". Satu pengidentifikasi, nama berbeda untuk setiap bahasa.

**Validasi komunitas.** Jutaan editor. Deteksi vandalisme. Persyaratan sumber. Tidak sempurna, tapi lebih skalabel daripada tim kecil ahli.

Tidak ada alasan untuk membangun semua ini dari nol.

---

## Kosakata GEUL berasal dari Wikidata

SIDX (Semantic-aligned Index) milik GEUL adalah pengidentifikasi yang selaras secara semantik dengan lebar 64-bit.
Makna dikodekan dalam bit-bit itu sendiri.
Hanya dengan memeriksa bit-bit atas, Anda bisa mengetahui apakah sesuatu itu orang, tempat, atau organisasi.

Buku kode SIDX — pola bit mana yang dipetakan ke makna apa — diekstrak dari Wikidata.

Prosesnya sebagai berikut.

**Langkah 1: Ekstraksi tipe.**
Ekstrak semua Q-ID yang digunakan sebagai objek dari P31 (instance of) di Wikidata.
Ini menghasilkan daftar "tipe".
"Manusia (Q5)", "kota (Q515)", "negara (Q6256)", "perusahaan (Q4830453)"...
Hitung berapa kali setiap tipe digunakan — jumlah instansi.

**Langkah 2: Pembangunan hierarki.**
Ekstrak relasi P279 (subclass of) antartipe.
"Kota → permukiman manusia → entitas geografis → entitas."
Ini membentuk struktur pohon dari tipe-tipe tersebut.
Identifikasi simpul akar, simpul daun, dan simpul perantara.
Deteksi dan tangani pewarisan ganda — kasus di mana satu tipe milik beberapa tipe induk.

**Langkah 3: Penugasan bit.**
Struktur pohon menentukan hubungan awalan dari pola bit.
Subtipe di bawah induk yang sama berbagi awalan yang sama.
"Kota" dan "desa" berbagi awalan dari "permukiman manusia".

Jumlah instansi memengaruhi panjang bit.
Tipe yang sering digunakan mendapat kode yang lebih efisien.
Prinsipnya sama dengan pengkodean Huffman: kode lebih pendek untuk frekuensi lebih tinggi.

---

## Apa yang Wikidata sediakan

Dalam proses ini, Wikidata menyediakan tiga hal.

**Sistem klasifikasi.**
Jawaban untuk "Jenis-jenis apa saja yang ada di dunia?"
CYC menugaskan tim ahli untuk merancang ini.
GEUL mengekstraknya dari Wikidata.
Sistem klasifikasi yang dibangun jutaan editor selama 10 tahun,
diubah menjadi pohon bit.

**Statistik frekuensi.**
Jawaban untuk "Berapa banyak dari setiap jenis yang ada di dunia?"
Jika ada 9 juta entitas manusia dan 1 juta asteroid,
tipe "manusia" harus mendapat kode yang lebih efisien daripada "asteroid".
Frekuensi penggunaan nyata menentukan desain kode.

**Pemetaan pengidentifikasi.**
Pemetaan antara Q-ID Wikidata dan SIDX GEUL.
Pola bit apa di SIDX yang sesuai dengan Q20718 (Samsung Electronics)?
Dengan pemetaan ini, pengetahuan Wikidata dapat dikonversi ke GEUL,
dan pernyataan GEUL dapat dikonversi balik ke Wikidata.

---

## Apa yang Wikidata tidak sediakan

Wikidata adalah kamus. Kamus bukan bahasa.

Kamus menyediakan daftar kata.
Bahasa menyediakan tata bahasa untuk menyusun kalimat dari kata-kata.

Apa yang tidak disediakan Wikidata adalah apa yang GEUL tambahkan.

**Dari fakta ke klaim.**
Unit dasar Wikidata adalah fakta (Fact).
"Populasi Seoul adalah 9,74 juta."
Benar atau salah.

Unit dasar GEUL adalah klaim (Claim).
"Menurut A, populasi Seoul sekitar 9,74 juta. (keyakinan 0,9, per 2023)"
Siapa yang mengklaim, dengan tingkat kepastian berapa, dan per kapan — semuanya tertanam dalam pernyataan.
Perbedaan ini dibahas secara rinci di [Mengapa klaim, bukan fakta](/id/why/claims-not-facts/).

**Pengkualifikasi kata kerja.**
Wikidata tidak punya tempat untuk mengekspresikan nuansa kata kerja.
Dalam "Yi Sun-sin menang di Pertempuran Myeongnyang",
di mana letak kala, aspek, evidensialitas, modus, dan keyakinan?
Di Wikidata, ini diekspresikan sebagian melalui qualifier,
namun tidak ada sistem kualifikasi kata kerja yang sistematis.

GEUL memiliki sistem pengkualifikasi kata kerja 28-bit.
Tiga belas dimensi — kala, aspek, polaritas, evidensialitas, modus, volisionalitas, keyakinan, dan lainnya — tertanam secara struktural di setiap pernyataan.

**Kompresi 16-bit.**
Representasi Wikidata tidak dirancang untuk jendela konteks.
JSON-LD, RDF, SPARQL.
Dapat dibaca mesin, tapi tidak efisien dalam token.

GEUL dirancang dalam unit kata 16-bit.
Pemetaan satu-ke-satu dengan token LLM.
Sistem representasi yang dibangun dengan premis jendela konteks yang terbatas.
Ini sudah dibahas di [Mengapa bukan MD/JSON/XML](/id/why/not-md-json-xml/).

**Pipeline konteks.**
Wikidata adalah repositori. GEUL adalah bagian dari pipeline.
Klarifikasi, validasi, penyaringan, pemeriksaan konsistensi, eksplorasi — semua yang dibahas dalam seri ini beroperasi di atas representasi terstruktur GEUL.
Wikidata tidak memiliki pipeline ini.
Dan tidak perlu. Tujuan Wikidata berbeda.

---

## Hubungan antara kamus dan bahasa

Ringkasnya:

Wikidata adalah kosakata dunia.
Entitas apa yang ada,
relasi apa yang ada,
tipe apa yang ada dan bagaimana mereka diklasifikasikan.
Jutaan orang membangunnya selama 10 tahun.

GEUL membangun tata bahasa di atas kosakata ini.
Sistem klasifikasi kosakata → pohon bit SIDX.
Statistik frekuensi kosakata → prioritas penugasan bit.
Pengidentifikasi kosakata → pemetaan ke SIDX.

Dan menambahkan apa yang tidak dimiliki kosakata.
Struktur klaim. Kualifikasi kata kerja. Kompresi tingkat token. Pipeline konteks.

Bisakah GEUL dibangun tanpa Wikidata?
Bisa. Dengan merancang ontologi dari nol, seperti CYC.
Tapi itu sudah dicoba 30 tahun lalu, dan hasilnya sudah jelas.

Karena Wikidata ada, GEUL tidak merancang ontologi.
GEUL mengubah konsensus yang sudah ada.

---

## Rangkuman

Bahasa buatan membutuhkan kosakata.
Membangunnya dari nol dicoba oleh CYC, dan 30 tahun membuktikan batas pendekatan itu.

Wikidata adalah kosakata dunia, dengan lebih dari 100 juta entitas, lebih dari 10.000 properti, dan miliaran pernyataan.
Dibangun oleh jutaan editor selama 10 tahun.

Buku kode SIDX GEUL diekstrak dari Wikidata.
Frekuensi instansi P31 menentukan penugasan bit,
dan hierarki P279 membentuk kerangka pohon bit.

Wikidata adalah kamus; GEUL adalah bahasa.
Kamus menyediakan kata; bahasa menyediakan tata bahasa.
GEUL membangun struktur klaim, kualifikasi kata kerja, kompresi 16-bit, dan pipeline konteks di atas kosakata Wikidata.

GEUL tidak menolak Wikidata.
GEUL berdiri di atasnya.

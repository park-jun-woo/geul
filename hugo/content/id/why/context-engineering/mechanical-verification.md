---
title: "Mengapa Verifikasi Mekanis Diperlukan"
weight: 4
date: 2026-02-26T12:00:10+09:00
lastmod: 2026-02-26T12:00:10+09:00
tags: ["verifikasi", "spesifikasi", "kompiler"]
summary: "Bahasa alami tidak mengenal konsep kalimat yang tidak valid"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Bahasa alami tidak mengenal konsep "kalimat yang tidak valid."

---

## Tidak Ada yang Memeriksa Apa yang Masuk ke Konteks

Lihat bagaimana informasi masuk ke konteks dalam pipeline LLM saat ini.

RAG mengembalikan chunk.
Agen menerima respons API.
Percakapan sebelumnya terakumulasi di riwayat.
Pengguna mengunggah dokumen.

Semuanya masuk ke jendela konteks.
Tanpa pemeriksaan.

Mengapa tidak ada pemeriksaan?
Karena bahasa alami tidak mengenal konsep "tidak valid."

---

## Bahasa Alami Menerima Setiap String

Dalam pemrograman, ada yang namanya syntax error.

```python
def calculate(x, y
    return x + y
```

Tanda kurung tidak ditutup. Ia ditolak sebelum dieksekusi.
Kode bisa secara pasti dinyatakan "ini bukan kode yang valid" sebelum dijalankan, bahkan sebelum dibaca.

Bahasa alami tidak memiliki hal seperti itu.

"He went to the bank."
Secara tata bahasa sempurna.
Anda tidak bisa tahu siapa yang pergi, bank mana, atau mengapa,
tetapi tidak ada yang melanggar aturan tata bahasa bahasa alami.

"Laporan penjualan untuk tanggal 45 bulan ke-13 tahun 2024."
Tidak ada bulan ke-13 dan tidak ada tanggal 45.
Namun tidak ada yang melanggar aturan tata bahasa bahasa alami.
Ini adalah kalimat yang valid secara gramatikal.

"Sumber: tidak diketahui. Kepercayaan: tidak diketahui. Tanggal: tidak diketahui. Kapitalisasi pasar Samsung Electronics adalah 1.200 triliun won."
Sumbernya tidak diketahui, kepercayaannya tidak diketahui, tanggal referensinya tidak diketahui.
Namun tidak ada yang melanggar aturan tata bahasa bahasa alami.

Bahasa alami menerima segalanya.
Kalimat bahasa alami yang tidak valid secara struktural tidak ada.
Oleh karena itu, tidak ada kriteria mekanis untuk "menolak" informasi yang diungkapkan dalam bahasa alami.

---

## Syarat untuk Verifikasi Mekanis

Lihat kompiler Go.

Go menolak kompilasi jika ada import yang tidak digunakan.
Bahkan jika kodenya berjalan sempurna.
Bahkan jika tidak ada yang salah dengan logikanya.
Ia menolak semata-mata karena satu baris import tidak digunakan.

Ini adalah verifikasi mekanis.

Verifikasi mekanis memiliki tiga karakteristik.

**Deterministik.** Hasilnya adalah ya atau tidak. Bukan probabilitas. Tidak ada "mungkin tidak apa-apa." Valid atau tidak valid.

**Murah.** Tidak perlu pemanggilan LLM. Perbandingan string, pemeriksaan keberadaan field, pemeriksaan rentang nilai. Operasi CPU pada skala nanodetik.

**Tidak membaca makna.** Tidak menilai apakah isinya benar atau salah. Hanya memeriksa apakah formatnya sesuai dengan spesifikasi. Tidak tahu apakah "kapitalisasi pasar Samsung Electronics adalah 1.200 triliun won" benar. Tetapi tahu apakah field sumber kosong.

Agar ketiga hal ini dimungkinkan, ada satu prasyarat.
Informasi harus memiliki spesifikasi.

Jika ada spesifikasi, pelanggaran terdefinisi.
Jika pelanggaran terdefinisi, penolakan dimungkinkan.
Jika penolakan dimungkinkan, verifikasi ada.

Bahasa alami tidak memiliki spesifikasi, sehingga tidak ada pelanggaran.
Tidak ada pelanggaran berarti tidak ada penolakan.
Tidak ada penolakan berarti tidak ada verifikasi.

---

## Mengapa Verifikasi Sebelum Konteks Diperlukan

Jendela konteks terbatas.

Entah 128K token atau 1M token, ia terbatas.
Kualitas informasi yang masuk ke ruang terbatas menentukan kualitas output.

Namun dalam pipeline saat ini,
penilaian kualitas terjadi hanya setelah informasi masuk ke konteks.
Anda mengharapkan LLM membacanya, menilainya, dan sendiri menyimpulkan bahwa "informasi ini sulit dipercaya."

Ini salah dalam tiga hal.

**Mahal.** Anda menggunakan biaya inferensi LLM untuk melakukan pemeriksaan format. Anda menjalankan model dengan miliaran parameter untuk menyaring chunk tanpa sumber. Anda menggunakan penalaran probabilistik untuk tugas yang hanya memerlukan pengecekan satu field.

**Tidak andal.** Tidak ada jaminan LLM akan selalu mengabaikan informasi tanpa sumber. Faktanya, begitu sesuatu ada di konteks, LLM cenderung menggunakannya. Mengharapkan model mengabaikan sesuatu yang Anda masukkan ke konteks adalah kontradiksi.

**Terlambat.** Ruang jendela sudah terpakai. Jika 5 chunk tanpa sumber masing-masing memakan 200 token, 1.000 token terbuang. Bahkan jika mereka disaring, ruang itu sudah terpakai.

Verifikasi mekanis datang sebelum semua ini.
Sebelum masuk ke konteks.
Sebelum LLM membacanya.
Sebelum jendela terpakai.

---

## Apa yang Diverifikasi

Verifikasi mekanis memeriksa bukan kebenaran isi tetapi kesesuaian dengan spesifikasi format.

Secara spesifik, hal-hal ini:

**Kelengkapan struktural.** Apakah field yang diperlukan ada? Apakah edge memiliki subjek dan objek? Apakah ada yang hilang?

**Validitas pengidentifikasi.** Apakah node yang dirujuk ada? Apakah yang tertulis "Samsung Electronics" benar-benar menunjuk ke entitas yang terdefinisi? Apakah referensinya menggantung?

**Kesesuaian tipe.** Apakah ada tanggal di field tanggal? Apakah ada angka di field angka? "Tanggal 45 bulan ke-13 tahun 2024" tertangkap di sini.

**Kehadiran metadata.** Apakah ada field sumber? Apakah ada field waktu? Apakah kepercayaan ditentukan? Jika tidak, tolak, tandai sebagai absen, atau berikan nilai default.

**Integritas referensial.** Apakah node yang ditunjuk oleh edge benar-benar ada? Apakah merujuk ke node yang sudah dihapus?

Pemeriksaan-pemeriksaan ini memiliki satu kesamaan.
Semuanya bisa dilakukan tanpa membaca isinya.
Anda tidak tahu apakah "kapitalisasi pasar Samsung Electronics adalah 1.200 triliun won" benar.
Tetapi Anda tahu apakah sumber dinyatakan untuk pernyataan ini.
Anda tahu apakah waktu dicatat untuk pernyataan ini.
Anda tahu apakah format pernyataan ini sesuai dengan spesifikasi.

---

## Yang Murah Lebih Dulu

Dalam pipeline context engineering, pemeriksaan memiliki urutan.

**Verifikasi mekanis**: kesesuaian spesifikasi. Biaya mendekati nol. Deterministik.
**Penyaringan semantik**: penilaian relevansi, kepercayaan, kegunaan. Biaya tinggi. Probabilistik.
**Pemeriksaan konsistensi**: kontradiksi antar informasi yang dipilih. Biaya lebih tinggi. Memerlukan penalaran.

Jika Anda mengurutkannya dari yang termurah ke yang termahal,
pemeriksaan yang mahal memiliki lebih sedikit yang harus diproses.

Jika verifikasi mekanis menyaring 30% pernyataan yang tidak memiliki sumber,
penyaringan semantik hanya perlu memproses 70%.
Jika penyaringan semantik menghapus yang tidak relevan,
pemeriksaan konsistensi menangani set yang lebih kecil lagi.

Ini adalah prinsip yang sama dengan optimasi kueri database.
Terapkan kondisi yang bisa difilter oleh indeks di klausa WHERE terlebih dahulu.
Kondisi full-scan datang kemudian.
Jika yang murah lebih dulu, beban pada yang mahal berkurang.

Sebaliknya,
jika Anda menjalankan pemeriksaan mahal lebih dulu dan pemeriksaan murah belakangan,
Anda menemukan error format hanya setelah Anda sudah mengeluarkan biaya.
Anda menganalisis makna pernyataan yang merujuk node yang tidak ada,
hanya untuk menemukan setelahnya bahwa referensinya tidak valid.

---

## Urutan Ini Tidak Mungkin dalam Pipeline Bahasa Alami

Bahasa alami tidak memiliki spesifikasi, sehingga verifikasi mekanis tidak mungkin.
Karena verifikasi mekanis tidak mungkin, pemeriksaan termurah tidak ada.

Akibatnya, setiap pemeriksaan adalah pemeriksaan semantik.
Setiap pemeriksaan memerlukan LLM.
Setiap pemeriksaan mahal.

"Apakah chunk ini memiliki sumber?" -- LLM harus membacanya.
"Apakah referensi waktu chunk ini tepat?" -- LLM harus membacanya.
"Apakah format chunk ini benar?" -- Bahasa alami tidak memiliki format, sehingga pertanyaannya sendiri tidak berlaku.

Ini adalah realitas context engineering saat ini.
Bahkan pemeriksaan paling sederhana dilakukan dengan alat paling mahal.
Tugas yang bisa selesai dengan perbandingan string ditangani oleh mesin inferensi.

---

## Prasyarat untuk Verifikasi

Agar verifikasi mekanis ada, tiga hal diperlukan.

**Spesifikasi.** Format yang harus diikuti informasi harus terdefinisi. Field mana yang wajib, nilai mana yang diizinkan, referensi mana yang valid. Tanpa spesifikasi, pelanggaran tidak bisa didefinisikan.

**Formalisasi.** Informasi harus diungkapkan dalam format yang diminta spesifikasi. Bukan sebagai kalimat bahasa alami, tetapi dikodekan dalam struktur yang dituntut spesifikasi. Informasi yang tidak diformalisasi tidak bisa diperiksa.

**Kuasa untuk menolak.** Harus dimungkinkan untuk benar-benar menolak informasi yang tidak sesuai. Jika Anda memeriksa tetapi selalu meloloskan, itu bukan verifikasi. Informasi yang tidak valid harus dicegah masuk ke konteks.

Ketiga hal ini sudah dianggap biasa dalam bahasa pemrograman.
Ada spesifikasi bernama grammar, format bernama kode, dan kuasa menolak bernama kompiler.

Dalam bahasa alami, ketiganya tidak ada.
Grammar bukanlah spesifikasi format melainkan konvensi.
Kalimat bukanlah format terstruktur melainkan teks bebas.
Konsep "bahasa alami yang tidak valid" tidak ada, sehingga tidak ada yang bisa ditolak.

Untuk memperkenalkan verifikasi mekanis ke context engineering,
representasi informasi itu sendiri harus berubah.

---

## Ringkasan

Dalam pipeline konteks saat ini, informasi masuk ke konteks tanpa pemeriksaan.
Karena bahasa alami tidak mengenal konsep "kalimat yang tidak valid."

Verifikasi mekanis memeriksa bukan kebenaran isi tetapi kesesuaian dengan spesifikasi format.
Kelengkapan struktural, validitas pengidentifikasi, kesesuaian tipe, kehadiran metadata, integritas referensial.
Deterministik, murah, dan tidak membaca makna.

Dalam pipeline, pemeriksaan yang murah harus lebih dulu.
Jika verifikasi mekanis menyaring error format,
penilaian semantik yang mahal memiliki lebih sedikit yang harus diproses.

Bahasa alami tidak memiliki spesifikasi, sehingga pemeriksaan ini tidak mungkin.
Setiap pemeriksaan menjadi pemeriksaan semantik, dan setiap pemeriksaan mahal.

Agar verifikasi mekanis dimungkinkan,
harus ada spesifikasi, formalisasi, dan kuasa untuk menolak.
Representasi informasi itu sendiri harus berubah.

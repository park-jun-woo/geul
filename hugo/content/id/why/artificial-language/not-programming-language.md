---
title: "Mengapa Bahasa Pemrograman Tidak Cukup"
weight: 10
date: 2026-02-26T12:00:19+09:00
lastmod: 2026-02-26T12:00:19+09:00
tags: ["bahasa pemrograman", "deskripsi", "representasi pengetahuan"]
summary: "Bahasa pemrograman mendeskripsikan prosedur. Ia tidak bisa mendeskripsikan dunia. JSON menyediakan struktur tapi tanpa makna. Bahkan LISP hanya meminjam sintaksisnya."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Bahasa pemrograman mendeskripsikan prosedur. Ia tidak bisa mendeskripsikan dunia.

---

## Bahasa pemrograman adalah salah satu penemuan terbesar umat manusia

Bahasa pemrograman tidak ambigu.
`x = 3 + 4` menghasilkan 7 kapan pun dan di mana pun dijalankan.
Tidak ada ruang untuk penafsiran.

Bahasa pemrograman dapat diverifikasi.
Kesalahan sintaksis tertangkap sebelum kompilasi.
Kesalahan tipe tertangkap sebelum eksekusi.
Saat tes dijalankan, hasilnya adalah lolos atau gagal.

Bahasa pemrograman adalah Turing-complete.
Semua yang dapat dihitung bisa diekspresikan.
Dengan waktu dan memori yang cukup, prosedur apa pun bisa dideskripsikan.

Semua yang disebut sebagai keterbatasan bahasa alami dalam seri ini — ambiguitas, ketidakmampuan verifikasi, ketiadaan struktur — telah diselesaikan oleh bahasa pemrograman.

Jadi, mengapa tidak menggunakan bahasa pemrograman untuk merepresentasikan konteks AI?

Tidak bisa.

---

## Bahasa pemrograman mendeskripsikan prosedur

Berikut ini adalah kode Python yang valid.

```python
def calculate_revenue(units_sold, unit_price):
    return units_sold * unit_price
```

Kode ini jelas, dapat diverifikasi, dan dapat dieksekusi.
Tapi apa yang diekspresikannya?

"Kalikan jumlah unit terjual dengan harga satuan untuk mendapatkan pendapatan."

Ini adalah prosedur. Metode. HOW.
Ia mendeskripsikan apa yang harus dilakukan ketika input masuk.

Sekarang coba ekspresikan yang berikut.

"Pendapatan Samsung Electronics pada kuartal ketiga 2024 adalah 79 triliun won."

Ini bukan prosedur. Ini fakta. WHAT.
Tidak ada yang dieksekusi. Ia mendeskripsikan keadaan dunia.

Bagaimana mengekspresikan ini dalam Python?

```python
samsung_revenue_2024_q3 = 79_000_000_000_000
```

Sebuah angka diberikan ke sebuah variabel.
Berfungsi. Tapi ini bukan deskripsi. Ini penyimpanan.
Kode ini tidak tahu:

- Jenis entitas apa "Samsung Electronics" itu.
- Apa arti "pendapatan". Apakah indikator keuangan? Besaran fisik?
- Apakah "Q3 2024" adalah waktu, versi, atau label.
- Apa sumber dari angka 79 triliun won tersebut.
- Seberapa pasti nilai ini.

Nama variabel `samsung_revenue_2024_q3` memungkinkan manusia menebak maknanya.
Bagi mesin, itu hanyalah string sembarang.
Ganti namanya menjadi `xyzzy_42` dan hasil eksekusinya tetap sama.

Dalam bahasa pemrograman, nama variabel tidak memiliki makna.
Makna hidup di luar kode, di dalam kepala programmer.

---

## Lebih canggih pun tidak membantu

Bagaimana kalau membuat class?

```python
class FinancialReport:
    def __init__(self, company, metric, period, value, currency):
        self.company = company
        self.metric = metric
        self.period = period
        self.value = value
        self.currency = currency

report = FinancialReport("삼성전자", "매출", "2024-Q3", 79_000_000_000_000, "KRW")
```

Lebih baik. Ada strukturnya sekarang.
Tapi masalahnya masih ada.

`company` adalah string "삼성전자" (Samsung Electronics).
"Samsung Electronics", "SEC", dan "005930" semua merujuk perusahaan yang sama.
Apakah kode tahu itu? Tidak.
Ia hanya bisa membandingkan apakah string-nya sama atau tidak.

`metric` adalah string "매출" (pendapatan).
Apakah "매출", "매출액", dan "revenue" adalah hal yang sama atau berbeda?
Kode tidak tahu. String-nya berbeda, maka berbeda.

Bagaimana kalau mendefinisikan schema?
Kelola daftar perusahaan dengan Enum, kelola daftar metrik.
Bisa. Berfungsi.

Sekarang coba ekspresikan yang berikut.

"Yi Sun-sin itu hebat."

```python
opinion = Opinion("이순신", "was", "위대했다")
```

Apa ini?
String "이순신" (Yi Sun-sin) diikat dengan string "위대했다" (hebat).
Ini tidak mengekspresikan "Yi Sun-sin itu hebat".
Ini menyimpan "이순신" dan "위대했다".

Kode tidak tahu makna "위대했다" (hebat).
Apakah "위대했다" (hebat) dan "훌륭했다" (luar biasa) mirip,
apakah "비겁했다" (pengecut) adalah kebalikannya —
kode tidak bisa mengetahuinya.

Fakta terstruktur seperti data keuangan masih bisa ditangani.
Evaluasi, konteks, hubungan, deskripsi abstrak berada di luar jangkauan ekspresif bahasa pemrograman.

---

## Kode tidak tahu apa yang dilakukannya

```python
def process(data):
    result = []
    for item in data:
        if item["value"] > threshold:
            result.append(transform(item))
    return result
```

Kode ini berjalan sempurna.
Tapi apa yang dilakukannya?

Apakah memfilter data pendapatan?
Menyaring catatan pasien?
Membersihkan data sensor?

Kode itu sendiri tidak tahu.
`data`, `value`, `threshold`, `transform` — semua nama abstrak.
Apakah kode ini bagian dari sistem keuangan atau sistem medis
bergantung pada konteks di luar kode.

Bisa menulis komentar.
Tapi komentar adalah bahasa alami. Mesin tidak memahaminya.
Kalau komentar bertentangan dengan kode, compiler tidak menyadarinya.
Komentar untuk manusia, bukan untuk mesin.

Ketika AI menerima kode sebagai konteks, masalah ini muncul langsung.
Karena kode tidak memiliki identitas diri,
AI harus merekonstruksi identitasnya melalui inferensi setiap kali.
Karena inferensi, maka ada biaya komputasi dan bisa salah.

---

## Alasan mendasar

Bahwa bahasa pemrograman tidak bisa mendeskripsikan dunia bukanlah cacat desain.
Tujuannya berbeda.

Tujuan bahasa pemrograman adalah menginstruksikan mesin tentang prosedur.
"Ketika input ini masuk, lakukan operasi ini."
Semantik bahasa pemrograman adalah semantik eksekusi.
Setiap konstruksi diinterpretasikan sebagai "apa yang mesin lakukan".

`x = 3` adalah instruksi "simpan 3 di lokasi memori bernama x".
`if x > 0` adalah instruksi "jika x lebih besar dari 0, jalankan blok berikutnya".
`return x` adalah instruksi "kembalikan nilai x ke pemanggil".

Semua kata kerja. Semua tindakan. Semua prosedur.

"Samsung Electronics adalah perusahaan Korea" bukan kata kerja.
Bukan tindakan. Bukan prosedur.
Ia mendeskripsikan keadaan dunia.

Bahasa pemrograman tidak punya tempat untuk ini.
Bisa disimpan dalam variabel, tapi itu penyimpanan, bukan deskripsi.
Makna dari nilai yang disimpan bukan urusan kode.

---

## Bagaimana dengan JSON, YAML, XML?

Kalau bukan bahasa pemrograman, bagaimana dengan format data?

```json
{
  "company": "삼성전자",
  "metric": "매출",
  "period": "2024-Q3",
  "value": 79000000000000,
  "currency": "KRW"
}
```

Ada struktur. Field-nya eksplisit.
Tapi tidak ada makna.

Apakah "company" berarti korporasi, JSON tidak tahu.
Apakah "삼성전자" sama dengan "Samsung Electronics" di tempat lain, JSON tidak tahu.
Apakah objek JSON ini dan objek JSON itu mendeskripsikan entitas yang sama, JSON tidak tahu.

JSON menyediakan struktur tapi bukan makna.
Ini pasangan kunci-nilai, bukan entitas-hubungan-atribut.

Mendefinisikan schema membantu.
JSON Schema, Protocol Buffers, GraphQL.
Tipe field didefinisikan, keharusan didefinisikan, referensi didefinisikan.

Tapi semua ini adalah struktur yang dirancang untuk sistem tertentu.
Bukan representasi pengetahuan tujuan umum.
Schema data keuangan tidak bisa mengekspresikan penilaian terhadap tokoh sejarah.
Schema data medis tidak bisa mengekspresikan hubungan persaingan antar perusahaan.

Schema terpisah untuk setiap domain.
Alat terpisah untuk setiap schema.
Tidak ada interoperabilitas antar schema.

Keterbatasan ini dibahas lebih detail di [Mengapa MD/JSON/XML Tidak Cukup](/id/why/not-md-json-xml/).

---

## Bagaimana dengan LISP?

Beberapa pembaca mungkin memikirkan sebuah contoh tandingan.

LISP.

```lisp
(is 삼성전자 (company korea))
(revenue 삼성전자 2024-Q3 79000000000000)
(great 이순신)
```

S-expression adalah struktur pohon,
dan kode adalah data dan data adalah kode.
Homoiconicity.

Faktanya, AI awal seluruhnya berbasis LISP.
SHRDLU, CYC, sistem pakar.
Pengetahuan direpresentasikan dalam LISP, dan mesin inferensi berjalan di atasnya.
Tampak seperti bukti historis yang membantah bahwa "bahasa pemrograman tidak bisa mendeskripsikan dunia".

Tapi contoh tandingan ini gagal karena tiga alasan.

### Apa yang LISP tahu vs. apa yang programmer tentukan

Dalam `(is 삼성전자 company)`, LISP tidak tahu
bahwa `is` berarti relasi "adalah".
Programmer yang menentukannya.

Ganti `is` dengan `zzz` dan LISP tidak peduli.
`(zzz 삼성전자 company)` adalah ekspresi yang sepenuhnya valid bagi LISP.

LISP menyediakan struktur. Sebuah pohon bernama S-expression.
Tapi makna di dalam struktur itu diberikan oleh programmer, bukan bahasa.
Ini secara fundamental sama dengan JSON yang tidak tahu makna key-nya.

Menyediakan struktur dan menanamkan makna adalah hal yang berbeda.

### 30 tahun CYC

Upaya paling ambisius adalah CYC.

Dimulai tahun 1984.
Mencoba merepresentasikan pengetahuan umum menggunakan LISP.
Jutaan aturan dimasukkan secara manual.

Yang dibuktikan 30 tahun bukanlah kelayakan, melainkan keterbatasan.

Ontologi harus dirancang secara manual untuk setiap domain.
Interoperabilitas lintas domain tidak berhasil.
Tidak bisa mengikuti fleksibilitas bahasa alami.
Semakin besar skalanya, mempertahankan konsistensi semakin mendekati mustahil.

Bahwa representasi pengetahuan "bisa dilakukan" dalam LISP itu benar.
Bahwa itu "berhasil dengan baik" — itulah yang dibantah oleh hasil 30 tahun.

### Kalau tidak mau eval, tidak ada alasan menggunakan LISP

Masalah paling mendasar.

Kekuatan LISP adalah `eval`.
Karena kode adalah data, data bisa dieksekusi.
Metaprogramming, macro, pembuatan kode saat runtime.
Inilah yang membuat LISP menjadi LISP.

Tapi apa yang terjadi kalau `eval` diterapkan pada `(is 삼성전자 company)`?

Menjadi pemanggilan fungsi yang melempar `삼성전자` dan `company` sebagai argumen ke fungsi bernama `is`.
Bukan deskripsi — eksekusi.

Untuk menggunakannya sebagai representasi pengetahuan, tidak boleh di-eval.
Kalau tidak di-eval, berarti tidak menggunakan semantik LISP.
Hanya meminjam sintaksis S-expression saja.

Itu bukan "mendeskripsikan dunia dalam LISP".
Itu "menyimpan data menggunakan notasi kurung LISP".

Semantik LISP sebagai bahasa pemrograman — semantik eksekusi —
tetap dirancang untuk mendeskripsikan prosedur.
Meminjam sintaksis tidak mengubah semantik.

---

## Apa yang dibutuhkan bahasa untuk mendeskripsikan dunia

Bahasa pemrograman mendeskripsikan prosedur.
Format data menyediakan struktur tapi tanpa makna.
Bahkan LISP hanya meminjam sintaksis tanpa semantik deskripsi.

Apa yang dibutuhkan bahasa untuk mendeskripsikan dunia?

**Identitas entitas.** "Samsung Electronics" harus memiliki pengenal unik. Mesin harus tahu bahwa itu sama dengan "삼성전자". Bukan perbandingan string, melainkan kesetaraan identitas.

**Ekspresi hubungan.** Dalam "Samsung Electronics adalah perusahaan Korea", harus bisa mengekspresikan hubungan "perusahaan Korea". Bukan penugasan variabel, melainkan deskripsi hubungan.

**Deskripsi yang mendeskripsikan dirinya sendiri.** Tentang apa deskripsi ini, siapa yang mengatakannya, per kapan, dan seberapa pasti — semua harus tercakup dalam deskripsi itu sendiri. Di dalam kode, bukan di luar.

**Independensi domain.** Data keuangan, fakta sejarah, penilaian subjektif, hubungan abstrak — semuanya harus bisa diekspresikan dalam format yang sama. Bukan schema terpisah untuk setiap domain, melainkan satu struktur universal.

Bahasa pemrograman tidak memiliki keempat sifat ini.
Karena bahasa pemrograman tidak dibuat untuk ini.
Ia dibuat untuk mendeskripsikan prosedur.

Bahasa alami bisa melakukan keempatnya. Secara ambigu.
Yang dibutuhkan adalah kombinasi jangkauan ekspresif bahasa alami dan ketepatan bahasa pemrograman.

---

## Ringkasan

Bahasa pemrograman tidak ambigu, dapat diverifikasi, dan Turing-complete.
Tapi tidak bisa mendeskripsikan dunia.

Bahasa pemrograman mendeskripsikan prosedur.
"Ketika input ini masuk, lakukan ini." Semua kata kerja, semua tindakan.
"Samsung Electronics adalah perusahaan Korea" bukan tindakan.
Bahasa pemrograman tidak punya tempat untuk itu.

Kode tidak mengenal identitasnya sendiri.
Termasuk domain apa, melayani tujuan apa —
tidak ada yang tercatat di dalam kode.

Format data seperti JSON dan YAML menyediakan struktur tapi tanpa makna.
LISP bisa meminjam sintaksis, tapi tidak punya semantik deskripsi.
CYC menghabiskan 30 tahun mencoba representasi pengetahuan berbasis LISP, dan yang dibuktikan adalah keterbatasan.

Mendeskripsikan dunia membutuhkan identitas entitas, ekspresi hubungan, deskripsi yang mendeskripsikan dirinya sendiri, dan independensi domain.
Bahasa pemrograman tidak dibuat untuk ini.
Bahasa alami bisa, tapi secara ambigu.
Yang dibutuhkan ada di suatu tempat di antara keduanya.

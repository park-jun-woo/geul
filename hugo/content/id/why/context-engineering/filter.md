---
title: "Mengapa Filter Diperlukan"
weight: 5
date: 2026-02-26T12:00:09+09:00
lastmod: 2026-02-26T12:00:09+09:00
tags: ["filter", "relevansi", "kepercayaan"]
summary: "Informasi yang valid tidak selalu merupakan informasi yang dibutuhkan"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Informasi yang valid tidak selalu merupakan informasi yang dibutuhkan.

---

## Anda Memiliki 1.000 Informasi yang Lolos Verifikasi

Misalkan verifikasi mekanis berhasil.

Formatnya benar,
field yang diperlukan ada,
pengidentifikasi valid,
tipe sesuai,
dan integritas referensial terjaga -- 1.000 pernyataan tersisa.

Semuanya adalah informasi yang valid.
Mereka sesuai dengan spesifikasi. Tidak ada alasan untuk menolaknya.

Tetapi jendela konteks hanya bisa menampung 300.

300 mana yang Anda masukkan?

Ini adalah masalah penyaringan.

---

## Verifikasi dan Penyaringan Mengajukan Pertanyaan yang Berbeda

Yang ditanyakan verifikasi: "Apakah informasi ini valid?"
Yang ditanyakan penyaringan: "Apakah informasi ini dibutuhkan sekarang?"

Verifikasi melihat properti informasi itu sendiri.
Apakah formatnya benar? Apakah field-nya ada? Apakah referensinya valid?
Ia tidak peduli tentang apa informasi itu atau untuk tujuan apa.

Penyaringan melihat hubungan antara informasi dan situasi.
Apakah relevan untuk inferensi tertentu saat ini?
Bisakah informasi ini dipercaya?
Apakah cukup terkini?

Verifikasi dimungkinkan tanpa konteks. Anda hanya memerlukan spesifikasi.
Penyaringan tidak mungkin tanpa konteks. Anda perlu tahu "apa yang dibutuhkan sekarang."

Verifikasi bersifat deterministik. Valid atau tidak valid.
Penyaringan bersifat penilaian. Relevansi memiliki derajat, kepercayaan memiliki ambang batas, kebaruan memiliki konteks.

Verifikasi murah.
Penyaringan relatif mahal.

Itulah mengapa verifikasi lebih dulu dan penyaringan datang setelahnya.
Jika verifikasi menyaring lebih dulu, maka penyaringan menilai set yang lebih kecil.
Biaya penilaian yang mahal berkurang.

---

## Tiga Hal yang Dinilai Penyaringan

Penyaringan melihat tiga hal utama.

### Relevansi: Apakah Dibutuhkan untuk Inferensi Ini?

Pengguna bertanya tentang "laba operasional Samsung Electronics Q3 2024."

Di antara pernyataan valid yang lolos verifikasi:

- Laba operasional Samsung Electronics Q3 2024 adalah 9,18 triliun won.
- Pendapatan Samsung Electronics Q3 2024 adalah 79 triliun won.
- Laba operasional Samsung Electronics Q3 2023 adalah 2,43 triliun won.
- Rencana belanja modal semikonduktor Samsung Electronics adalah 53 triliun won per 2025.
- Kantor pusat Samsung Electronics berada di Suwon.

Semuanya valid. Semuanya tentang Samsung Electronics.
Apakah Anda memasukkan semuanya ke konteks?

Lokasi kantor pusat tidak relevan.
Rencana belanja modal memiliki relevansi rendah.
Laba operasional 2023 mungkin berguna untuk perbandingan.
Pendapatan berkaitan erat dengan laba operasional.

Dalam RAG bahasa alami, penilaian ini didelegasikan ke kemiripan embedding.
Diurutkan berdasarkan jarak vektor ke "laba operasional Samsung Electronics."
Tetapi seperti sudah dibahas, mirip bukan berarti relevan.

Dalam representasi terstruktur, penilaian relevansi memiliki input yang berbeda.
Entitas mana yang ditunjuk pernyataan? Samsung Electronics.
Properti apa? Laba operasional.
Waktu kapan? Q3 2024.

Jika entitas, properti, dan waktu ada sebagai field,
Anda bisa menemukan "entitas sama, properti sama, waktu sama" secara tepat.
Dan Anda bisa dengan sengaja memasukkan atau mengecualikan "entitas sama, properti sama, waktu berbeda."
Pencocokan field, bukan jarak vektor.

Relevansi tetaplah penilaian. Bukan deterministik.
Tetapi apakah input untuk penilaian itu adalah jarak vektor atau field terstruktur membuat perbedaan dalam akurasi.

### Kepercayaan: Bisakah Informasi Ini Dipercaya?

Dua pernyataan ada tentang konten yang sama.

- Sumber: pengungkapan IR Samsung Electronics. Kepercayaan: 1,0. "Laba operasional Q3 2024: 9,18 triliun won."
- Sumber: blog anonim. Kepercayaan: 0,3. "Laba operasional Q3 2024: sekitar 10 triliun won."

Mana yang masuk ke konteks?

Jelas yang pertama.

Tetapi agar penilaian ini "jelas,"
sumber dan kepercayaan harus ada dalam bentuk yang bisa dibaca.

Dalam chunk bahasa alami, sumber terkubur di suatu tempat dalam teks atau tidak ada.
Kepercayaan tidak pernah dinyatakan.
Untuk membandingkan dua chunk dan menilai mana yang lebih terpercaya,
LLM harus membaca dan bernalar.

Dalam representasi terstruktur, sumber dan kepercayaan adalah field.
"Kecualikan kepercayaan di bawah 0,5" adalah satu perbandingan.
"Sertakan hanya sumber primer" adalah pencocokan field.

Biaya penyaringan kepercayaan bergeser dari inferensi LLM ke perbandingan field.

### Kebaruan: Apakah Informasi Ini Cukup Terkini?

"Siapa CEO Samsung Electronics?"

- Waktu: Maret 2024. "CEO Samsung Electronics: Kyung Kye-hyun."
- Waktu: Desember 2022. "Co-CEO Samsung Electronics: Han Jong-hee, Kyung Kye-hyun."

Keduanya valid. Format benar, sumber ada.
Tetapi yang terbaru yang dibutuhkan.

Dalam bahasa alami, waktu mungkin atau mungkin tidak disebutkan dalam teks.
Jika tertulis "tahun lalu," Anda juga harus menghitung kapan "tahun lalu" itu.

Dalam representasi terstruktur, waktu adalah field.
Tanggal ISO 8601.
"Sertakan hanya pernyataan terbaru" adalah satu operasi pengurutan.

Lebih penting lagi, kriteria kebaruan bergantung pada konteks.
Jika seseorang bertanya siapa CEO, entri terbaru yang dibutuhkan.
Jika seseorang bertanya semua CEO yang pernah menjabat, setiap entri dibutuhkan.
Jika seseorang bertanya tren pendapatan, 8 kuartal terakhir yang dibutuhkan.

Jika waktu ada sebagai field, kondisi-kondisi ini bisa dinyatakan sebagai kueri.
Jika waktu terkubur dalam bahasa alami, ia harus diekstrak setiap kali.

---

## Mengapa Penyaringan Bukan Verifikasi Mekanis

Ada perbedaan penting di sini.

Dari tiga kriteria penyaringan -- relevansi, kepercayaan, kebaruan --
kepercayaan dan kebaruan sebagian besar bisa diproses secara mekanis dalam representasi terstruktur.
Perbandingan field, pengurutan nilai, penyaringan rentang.

Lalu mengapa menyebut ini "penyaringan" dan bukan "verifikasi"?

Verifikasi hanya melihat properti informasi itu sendiri.
"Apakah pernyataan ini memiliki field waktu?" Ada atau tidak ada. Tidak perlu konteks.

Penyaringan melihat hubungan antara informasi dan situasi.
"Apakah waktu pernyataan ini tepat untuk pertanyaan ini?" Anda harus tahu pertanyaannya untuk menjawab.

Keduanya memeriksa field waktu yang sama,
tetapi verifikasi memeriksa "keberadaan"
dan penyaringan menilai "kesesuaian."

Keberadaan tidak memerlukan konteks.
Kesesuaian memerlukan konteks.

Perbedaan inilah yang membuat pipeline memisahkan kedua tahap ini.

---

## Struktur Biaya Penyaringan

Penyaringan lebih mahal dari verifikasi. Tetapi seberapa mahal bergantung pada representasi.

**Penyaringan dalam pipeline bahasa alami:**
Penilaian relevansi -- inferensi LLM atau komputasi kemiripan embedding.
Penilaian kepercayaan -- LLM mengekstrak informasi sumber dari teks dan mengevaluasi.
Penilaian kebaruan -- LLM mengekstrak informasi waktu dari teks dan membandingkan.
Semuanya penalaran. Semuanya mahal.

**Penyaringan dalam representasi terstruktur:**
Penilaian relevansi -- pencocokan field entitas/properti + penilaian berbasis konteks.
Penilaian kepercayaan -- perbandingan field kepercayaan. Pencocokan field sumber.
Penilaian kebaruan -- pengurutan field waktu. Perbandingan rentang.
Kepercayaan dan kebaruan adalah operasi field. Hanya relevansi yang memerlukan penilaian.

Dengan kata lain, strukturisasi mengubah dua dari tiga kriteria penyaringan menjadi operasi mekanis.
Yang tersisa hanya relevansi.
Bahkan relevansi menyempit dari "apakah gumpalan teks ini mirip dengan pertanyaan" menjadi "apakah properti ini dari entitas ini relevan dengan pertanyaan," membuat penilaian lebih jelas.

Total biaya penyaringan turun secara signifikan.

---

## Apa yang Terjadi Tanpa Penyaringan

Jika Anda memverifikasi tetapi memasukkan semuanya ke konteks tanpa penyaringan.

Semua 1.000 informasi valid masuk.
Dari jumlah itu, hanya 30 yang dibutuhkan sekarang.

LLM membaca semua 1.000.
Membaca membutuhkan biaya.
970 informasi yang tidak diperlukan menyebarkan perhatian.
Penelitian menunjukkan bahwa semakin banyak informasi tidak relevan dalam konteks, semakin tinggi kemungkinan halusinasi.
Kualitas penalaran pada 30 yang benar-benar penting menurun.

Jendela juga terbuang.
Dari ruang yang ditempati 1.000 item, ruang senilai 970 item adalah pemborosan.
Ruang itu bisa menampung informasi lain yang lebih relevan.

Penyaringan adalah tentang mengelola jendela terbatas secara terbatas.
Jika verifikasi mengonfirmasi "apakah ia layak masuk,"
penyaringan menilai "apakah ia memiliki alasan untuk masuk."

Kelayakan adalah masalah format. Alasan adalah masalah konteks.
Keduanya diperlukan.

---

## Penyaringan Adalah Kebijakan

Satu poin penting lagi.

Kriteria penyaringan tidak tetap.
Mereka bervariasi sesuai konteks.

Penyaringan untuk agen konsultasi medis:
Ambang kepercayaan tinggi. Kecualikan kepercayaan di bawah 0,9.
Standar kebaruan ketat. Kecualikan informasi medis lebih dari 3 tahun.
Kecualikan sumber yang bukan jurnal peer-reviewed.

Penyaringan untuk agen percakapan kasual:
Ambang kepercayaan rendah. Informasi perkiraan bisa diterima.
Standar kebaruan fleksibel. Informasi lama bisa disertakan tergantung konteks.
Batasan sumber longgar.

Informasi yang sama lolos di satu agen dan ditolak di agen lain.
Informasinya tidak berubah. Kebijakannya yang berbeda.

Ini berarti penyaringan bukan sekadar masalah teknis
tetapi masalah desain.
"Apa yang masuk ke konteks" adalah pertanyaan yang sama dengan
"standar apa yang kita inginkan untuk agen ini beroperasi."

Dalam representasi terstruktur, kebijakan ini dinyatakan secara deklaratif.
"confidence >= 0.9, time >= 2022, source_type = peer-reviewed."
Satu baris kueri.

Dalam bahasa alami, kebijakan ini ditulis sebagai bahasa alami dalam prompt.
"Tolong hanya rujuk informasi terpercaya yang terkini."
Apakah LLM mengikuti ini secara konsisten adalah masalah probabilitas.

---

## Ringkasan

Tidak semua informasi yang lolos verifikasi dibutuhkan.
Jendela konteks yang terbatas seharusnya hanya berisi apa yang dibutuhkan untuk inferensi saat ini.

Penyaringan menilai tiga hal.
Relevansi -- apakah informasi ini dibutuhkan untuk pertanyaan saat ini?
Kepercayaan -- bisakah informasi ini dipercaya?
Kebaruan -- apakah informasi ini cukup terkini?

Verifikasi dan penyaringan mengajukan pertanyaan yang berbeda.
Verifikasi bertanya "apakah valid?"; penyaringan bertanya "apakah dibutuhkan?"
Verifikasi dimungkinkan tanpa konteks; penyaringan memerlukan konteks.
Verifikasi lebih dulu; penyaringan setelahnya.

Dalam representasi terstruktur, dua dari tiga kriteria penyaringan -- kepercayaan dan kebaruan -- diubah menjadi operasi field. Yang tersisa hanya relevansi, dan bahkan itu menjadi lebih jelas melalui pencocokan field struktural.

Penyaringan adalah kebijakan.
Informasi yang sama disertakan atau dikecualikan tergantung konteks.
Dalam representasi terstruktur, kebijakan ini dinyatakan sebagai kueri.
Dalam bahasa alami, kebijakan ini ditulis dalam prompt sebagai harapan.

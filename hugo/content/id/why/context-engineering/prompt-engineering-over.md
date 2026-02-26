---
title: "Mengapa Era Prompt Engineering Berakhir"
weight: 1
date: 2026-02-26T12:00:12+09:00
lastmod: 2026-02-26T12:00:12+09:00
tags: ["prompt", "konteks", "engineering"]
summary: "Dari cara Anda mengatakannya ke apa yang Anda tunjukkan -- permainan telah berubah"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Mengapa Era Prompt Engineering Berakhir

### Dari "cara Anda mengatakannya" ke "apa yang Anda tunjukkan" -- permainan telah berubah.

---

### Prompt Engineering sebagai Profesi

Di 2023, profesi baru muncul.

Prompt engineer.

"Think step by step."
"You are an expert with 20 years of experience."
"Let me show you some examples first."

Kalimat-kalimat seperti ini menjadi know-how senilai puluhan ribu dolar. Pertanyaan yang sama menghasilkan jawaban yang sangat berbeda dari AI tergantung pada bagaimana Anda merumuskannya.

Prompt engineering benar-benar berhasil. Satu baris Chain-of-Thought menaikkan skor matematika 20%. Satu kalimat penugasan peran mengubah kedalaman keahlian. Tiga contoh few-shot memberikan kontrol penuh atas format output.

Ini bukan hype. Ini nyata. Jadi mengapa ia berakhir?

---

### Mengapa Berhasil: Karena Modelnya Cukup Bodoh

Lihat dari prinsip pertama mengapa prompt engineering berhasil. Sederhana.

LLM awal buruk dalam menangkap maksud pengguna. Katakan "ringkaskan" dan mereka menulis ulang. Katakan "bandingkan" dan mereka mendaftar.

Karena model salah membaca maksud, keterampilan menyampaikan maksud secara tepat menjadi bernilai. Prompt engineering pada dasarnya adalah "penerjemahan" -- menerjemahkan maksud manusia ke dalam bentuk yang bisa dipahami LLM.

Agar penerjemahan bernilai, harus ada hambatan bahasa.

---

### Apa yang Berubah: Modelnya Menjadi Pintar

Dari GPT-3.5 ke GPT-4. Dari Claude 2 ke Claude 3.5. Dengan setiap generasi, kemampuan model menangkap maksud meningkat secara dramatis.

Katakan "ringkaskan" dan mereka meringkas. Katakan "bandingkan" dan mereka membandingkan. Bahkan tanpa diberitahu "think step by step," mereka memecah masalah kompleks menjadi langkah-langkah sendiri.

Hambatan bahasa menjadi lebih rendah. Nilai penerjemahan menyusut.

Teknik prompt yang menghasilkan perbedaan dramatis di 2023 hanya menghasilkan perbedaan marginal di 2025. Ketika model cukup pintar, rumusan kata semakin tidak penting.

Jadi apa yang penting?

---

### Jendela Konteks: Hukum Fisika

LLM punya satu batasan fisik.

Jendela konteks.

Apakah 128K token atau 1M token, ia terbatas. Hanya informasi yang muat di dalam ruang terbatas ini yang memengaruhi penalaran. Informasi di luar jendela, sesignifikan apa pun, seolah tidak ada.

Ini independen dari ukuran model. Bahkan dengan triliunan parameter, jendela konteks terbatas. Bahkan dengan data pelatihan yang menjangkau seluruh internet, jendela konteks terbatas.

Sepintar apa pun modelnya, jika informasi yang salah masuk ke konteks, ia menghasilkan jawaban salah. Jika informasi yang tidak relevan memenuhi konteks, ia melewatkan yang penting. Jika informasi yang dibutuhkan tidak ada dalam konteks, ia seolah tidak diketahui.

Prompt engineering adalah masalah "cara Anda mengatakannya." Permainan baru adalah masalah "apa yang Anda tunjukkan."

Ini adalah context engineering.

---

### Analogi: Ujian Buku Terbuka

Inilah analogi untuk perbedaan antara prompt engineering dan context engineering.

Prompt engineering adalah menulis soal ujian dengan baik. Alih-alih "pilih jawaban yang benar di bawah," tulis "turunkan langkah demi langkah jawaban yang memenuhi semua kondisi berikut" -- dan siswa memberikan jawaban yang lebih baik.

Context engineering adalah pertanyaan tentang buku mana yang Anda bawa ke ujian buku terbuka. Sebaik apa pun soal ujian ditulis, jika siswa membawa buku yang salah, mereka tidak bisa menjawab. Jumlah buku yang bisa dibawa terbatas. Buku mana yang Anda bawa menentukan nilai Anda.

Ketika model bodoh, format pertanyaan (prompt) penting. Ketika model pintar, bahan referensi (konteks) penting.

---

### Era Agen Mempercepat Pergeseran

Pergeseran ini dipercepat dengan munculnya agen.

Prompt engineering ditulis manusia setiap kali. Manusia menulis pertanyaan, manusia menjelaskan konteks, manusia menentukan format.

Agen berbeda. Agen bernalar sendiri, memanggil alat, dan berkolaborasi dengan agen lain. Di setiap langkah, mereka harus menyusun konteks sendiri.

Agen memanggil API eksternal dan menerima data. Data ini perlu masuk ke konteks untuk putaran penalaran berikutnya. Bagian mana yang masuk dan mana yang ditinggal? Hasil penalaran sebelumnya mana yang disimpan dan mana yang dibuang? Bisakah informasi yang dikirim agen lain dipercaya?

Manusia tidak bisa membuat semua keputusan ini setiap kali. Agar agen beroperasi secara otonom, penyusunan konteks harus diotomatisasi.

Prompt engineering adalah keterampilan manusia. Context engineering harus menjadi kemampuan sistem.

---

### Prompt Engineering Tidak Menghilang

Izinkan saya mencegah kesalahpahaman.

Saya tidak mengatakan prompt engineering menjadi tidak bermakna. System prompt masih penting. Spesifikasi format output masih diperlukan. Deklarasi peran dan batasan masih efektif.

Yang menyusut adalah pangsa yang dipegang prompt engineering.

Jika 70% kualitas output ditentukan prompt di 2023, di 2025, 30% ditentukan prompt dan 70% oleh konteks.

Rasionya terbalik.

Dan tren ini tidak berbalik. Model akan terus menjadi lebih pintar, dan semakin pintar mereka, semakin tidak penting rumusan kata dan semakin penting konteks.

---

### Tetapi Context Engineering Tidak Punya Infrastruktur

Inilah intinya.

Prompt engineering punya alat. Template prompt, pustaka prompt, framework pengujian prompt. Seluruh ekosistem untuk mengelola "cara Anda mengatakannya" secara sistematis telah dibangun.

Context engineering belum punya ini.

Lihat bagaimana konteks ditangani dalam praktik saat ini.

Ukuran chunk pipeline RAG disetel manual. Informasi latar belakang ditulis ke system prompt manual. Apa yang disimpan di memori agen dirancang manual. Hasil pencarian mana yang dimasukkan ke konteks diputuskan manual.

Semuanya manual.

Dan bahan baku untuk semua pekerjaan manual itu adalah bahasa alami. Dokumen bahasa alami dipotong dalam bahasa alami dan ditempel ke konteks bahasa alami.

Bahasa alami punya kepadatan informasi rendah. Tidak ada sumber. Tidak ada tingkat kepercayaan. Tidak ada timestamp. Token yang tidak perlu dikonsumsi untuk menyampaikan makna yang sama. Tidak ada cara untuk mengotomatisasi penilaian kualitas.

Ini mirip era sebelum prompt engineering. Prompt engineering juga manual di awal. Ia bergantung pada intuisi dan pengalaman individu. Kemudian alat dan metodologi muncul dan ia menjadi tersistematisasi.

Context engineering ada di tahap awal itu sekarang. Masalahnya sudah dikenali, tetapi infrastrukturnya tidak ada.

---

### Apa yang Dibutuhkan Infrastruktur

Agar context engineering beralih dari pekerjaan manual ke sistem, minimal diperlukan hal-hal berikut.

**Kompresi.** Cara memuat lebih banyak makna ke jendela yang sama. Hilangkan lem gramatikal bahasa alami dan sisakan hanya makna, dan ukuran jendela efektif berlipat ganda -- tanpa mengubah model.

**Pengindeksan.** Cara menemukan informasi yang tepat secara presisi. Pencarian berdasarkan struktur semantik, bukan kesamaan embedding. Pencarian di mana mencari "pendapatan Apple" tidak menarik "fakta nutrisi apel."

**Validasi.** Cara menolak secara mekanis informasi yang tidak memenuhi spesifikasi. Seperti kompiler Go menangkap variabel yang tidak digunakan sebagai kesalahan, klaim tanpa sumber dan fakta tanpa timestamp harus difilter sebelum memasuki konteks. Pemeriksaan termurah dan paling deterministik harus didahulukan.

**Penyaringan.** Cara menilai kualitas semantik. Jika validasi melihat bentuk, penyaringan melihat isi. Relevansi, keandalan, kesegaran. Apakah informasi ini benar-benar dibutuhkan untuk putaran penalaran ini?

**Konsistensi.** Cara menjamin koherensi internal set informasi yang dipilih. Potongan informasi yang baik secara individual bisa bertentangan satu sama lain ketika digabungkan. Jika CEO dari 2020 dan CEO dari 2024 sama-sama masuk konteks secara bersamaan, LLM bingung.

**Komposisi.** Cara mengoptimalkan penempatan dan struktur di dalam jendela. Informasi yang sama menerima bobot perhatian berbeda tergantung penempatannya. Di depan atau belakang? Bagaimana dikelompokkan?

**Akumulasi.** Cara bagi sistem untuk belajar dan tumbuh seiring waktu. Caching adalah penggunaan kembali hasil individual. Akumulasi adalah mempelajari komposisi konteks mana yang menghasilkan hasil baik, dan menumbuhkan basis pengetahuan itu sendiri.

Ketujuh ini adalah stack penuh infrastruktur context engineering.

---

### Ini Bukan Tentang Alat Tertentu

Izinkan saya berterus terang.

Siapa yang membangun infrastruktur ini adalah pertanyaan terbuka. Satu alat mungkin menyelesaikan semuanya, atau beberapa alat mungkin menangani masing-masing lapisan.

Tetapi fakta bahwa infrastruktur diperlukan bukan pertanyaan terbuka.

Bahwa jendela konteks terbatas adalah fakta fisik. Bahkan jika jendela tumbuh 10x, informasi dunia tumbuh lebih cepat. Bahwa bahasa alami punya kepadatan informasi rendah adalah fakta struktural. Bahwa agen butuh manajemen konteks otomatis untuk beroperasi secara otonom adalah keharusan logis.

Seperti prompt engineering butuh alat, context engineering butuh alat. Tetapi kali ini, sifat alatnya berbeda.

Alat prompt engineering lebih dekat ke editor teks. Alat context engineering lebih dekat ke kompiler.

Kompres informasi, indeks, validasi, filter, periksa konsistensi, optimalkan penempatan, dan akumulasi hasil. Ini bukan pengeditan. Ini engineering.

Itulah mengapa disebut context "engineering."

---

### Ringkasan

Prompt engineering bernilai ketika model bodoh. Karena model tidak bisa membaca maksud, keterampilan menyampaikan maksud dengan baik penting.

Seiring model menjadi lebih pintar, permainan berubah. Dari "cara Anda mengatakannya" ke "apa yang Anda tunjukkan." Dari prompt ke konteks.

Munculnya agen mempercepat pergeseran ini. Manusia tidak bisa menyusun konteks setiap kali. Sistem harus melakukannya sendiri.

Tetapi saat ini, context engineering tidak punya infrastruktur. Bahasa alami dipotong dan ditempel secara manual.

Infrastruktur yang diperlukan memiliki tujuh lapisan: kompresi, pengindeksan, validasi, penyaringan, konsistensi, komposisi, akumulasi.

Bukan era prompt engineering yang berakhir. Yang berakhir adalah era ketika prompt engineering saja sudah cukup.

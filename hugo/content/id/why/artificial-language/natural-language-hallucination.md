---
title: "Mengapa Bahasa Alami Menciptakan Halusinasi?"
weight: 8
date: 2026-02-26T12:00:16+09:00
lastmod: 2026-02-26T12:00:16+09:00
tags: ["bahasa alami", "halusinasi", "ambiguitas"]
summary: "Halusinasi bukan bug LLM — ia adalah keniscayaan struktural dari empat cacat bahasa alami: ambiguitas, ketiadaan sumber, ketiadaan kepercayaan, dan ketiadaan waktu. Model yang lebih besar tidak bisa memperbaikinya."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Halusinasi bukan bug. Ia adalah keniscayaan struktural selama kita menggunakan bahasa alami.

---

## Keajaiban Bahasa Alami

100.000 tahun lalu, bahasa lisan muncul. Hubungan sosial yang bisa dipertahankan primata melalui saling merawat (grooming) terbatas pada sekitar 150 individu. Bahasa menghancurkan batas itu. Begitu satu orang bisa berbicara kepada banyak orang secara bersamaan, skala masyarakat baru -- suku -- menjadi mungkin.

10.000 tahun lalu, pertanian menciptakan surplus makanan, dan orang berkumpul di satu tempat membentuk kota. 5.000 tahun lalu, seseorang di Mesopotamia menekan tanda berbentuk baji ke tablet tanah liat basah. Itu untuk mencatat inventaris biji-bijian. Kelahiran tulisan. Ucapan lenyap, tetapi catatan bertahan. Begitu catatan bertahan, birokrasi menjadi mungkin, hukum menjadi mungkin, negara menjadi mungkin.

Bahasa lisan menciptakan suku. Tulisan menciptakan negara.

Bahasa alami adalah teknologi terbesar yang pernah diciptakan umat manusia. Bukan penemuan api, bukan penemuan roda, bukan penemuan semikonduktor. Yang membuat semua itu mungkin adalah bahasa alami. Karena bahasa alami ada, pengetahuan bisa ditransmisikan, kerja sama bisa terjadi, dan pikiran orang mati bisa diwarisi oleh yang hidup. Selama puluhan ribu tahun, bahasa alami adalah medium seluruh peradaban manusia.

Dan sekarang, bahasa alami yang agung itu telah menjadi bottleneck era AI.

---

## Kesalahpahaman Bernama Halusinasi

Ketika AI mengatakan sesuatu yang salah, kita menyebutnya "halusinasi."

Nama ini mengandung implikasi. Implikasi bahwa halusinasi itu abnormal. Implikasi bahwa ia bisa diperbaiki. Implikasi bahwa model yang lebih baik akan menyelesaikannya.

Ini kesalahpahaman.

Halusinasi bukan bug LLM. Halusinasi adalah keniscayaan struktural yang tidak bisa dihindari selama bahasa alami digunakan sebagai bahasa penalaran AI.

Sekeras apa pun Anda menskalakan model, sebanyak apa pun data yang diperluas, sehalus apa pun RLHF-nya, selama input-nya bahasa alami dan output-nya bahasa alami, halusinasi tidak akan hilang.

Biar saya jelaskan mengapa.

---

## Empat Cacat Struktural Bahasa Alami

Bahasa alami berevolusi untuk komunikasi antar manusia. Empat karakteristik yang diperoleh dalam proses itu menjadi cacat fatal dalam penalaran AI.

---

### Cacat 1: Ambiguitas

"He went to the bank."

Apakah "bank" itu lembaga keuangan atau tepi sungai? Siapa "he"? Kapan dia pergi?

Manusia menyelesaikan ini dengan konteks. Alur percakapan, ekspresi wajah pembicara, pengetahuan latar bersama.

AI hanya punya teks. Teks saja tidak bisa sepenuhnya menyelesaikan ambiguitas. Jika tidak bisa diselesaikan, AI menebak. Tebakan kadang salah. Ketika tebakan salah dikeluarkan dengan percaya diri, itulah halusinasi.

---

### Cacat 2: Ketiadaan Sumber

"Yi Sun-sin mengalahkan 133 kapal hanya dengan 12."

Kalimat ini tidak punya sumber.

Siapa yang membuat klaim ini? Catatan sejarah apa yang mendukungnya? Apakah ada ketidaksepakatan ilmiah tentang angka-angka ini?

Bahasa alami tidak punya tempat struktural untuk metadata. Untuk menyertakan sumber, Anda harus memperpanjang kalimat, dan memperpanjangnya mengaburkan poin utama. Jadi di sebagian besar kalimat bahasa alami, sumber dihilangkan. Masalah ini dibahas lebih mendalam di [Mengapa Klaim, Bukan Fakta?](/id/why/claims-not-facts/).

LLM dilatih pada miliaran kalimat seperti itu. Klaim dengan sumber yang dihilangkan tercampur menjadi satu sup statistik besar.

Melacak basis angka "12" di dalam sup itu secara prinsip tidak mungkin. Karena basis tidak bisa dilacak, angka tanpa basis juga bisa difabrikasi. Itulah halusinasi.

---

### Cacat 3: Ketiadaan Kepercayaan

"Bumi itu bulat." "Energi gelap menyusun 68% alam semesta." "Besok akan hujan."

Tingkat kepercayaan ketiga kalimat ini sepenuhnya berbeda.

Yang pertama adalah konsensus yang luar biasa kuat. Yang kedua adalah estimasi terbaik saat ini, tetapi teorinya bisa berubah. Yang ketiga adalah prediksi probabilistik.

Namun dalam bahasa alami, ketiganya memiliki struktur gramatikal identik. Subjek + predikat. Kalimat deklaratif. Titik.

Bahasa alami tidak bisa secara struktural mengekspresikan "seberapa yakin ini." Ada perangkat adverbial seperti "mungkin," "hampir pasti," "bisa jadi," tetapi mereka opsional, tidak presisi, dan biasanya dihilangkan.

LLM mempelajari semua kalimat pada tingkat kepercayaan identik. Tidak ada cara bagi model untuk membedakan secara internal perbedaan kepercayaan antara "Bumi itu bulat" dan "energi gelap adalah 68%."

Sehingga ia menyatakan estimasi sebagai fakta, menyatakan hipotesis sebagai pandangan mapan, dan menyatakan hal yang tidak pasti dengan kepastian. Itulah halusinasi.

---

### Cacat 4: Ketiadaan Konteks Temporal

"CEO Tesla adalah Elon Musk."

Per kapan?

Di 2024, ini benar. Di 2030, siapa tahu. Jika waktu penulisan tidak ditentukan, periode validitas kalimat ini tidak bisa ditentukan.

Sebagian besar kalimat bahasa alami menghilangkan konteks temporal. "Kalimat sekarang" bisa berarti "saat ini" atau bisa berarti "secara umum."

LLM mempelajari artikel dari 2020 dan artikel dari 2024 sebagai data yang sama. Karena informasi temporal tidak dilestarikan secara struktural, mereka menyatakan fakta masa lalu seolah-olah masa kini, atau mencampur informasi dari periode waktu berbeda. Itulah halusinasi.

---

## Pertemuan Empat Cacat

Halusinasi meningkat secara eksplosif ketika keempat cacat ini bertemu.

Mari kita analisis satu output LLM.

> "Yi Sun-sin menghancurkan 330 kapal Jepang dengan 12 kapal, dan kemudian meninggal di Pertempuran Noryang, meninggalkan kata-kata terakhir 'Jangan umumkan kematianku.'"

Dalam kalimat ini:

**Ambiguitas:** Apa tepatnya arti "menghancurkan"? Menenggelamkan? Mengalahkan? Merusak sebagian?

**Ketiadaan sumber:** Apa basis angka 12 dan 330? Catatan sejarah yang berbeda menyebutkan angka berbeda -- mana yang diikuti?

**Ketiadaan kepercayaan:** Apakah "Jangan umumkan kematianku" adalah wasiat yang dikonfirmasi secara historis, atau tradisi lisan kemudian? Tingkat kepercayaan keduanya berbeda, namun mereka terdaftar dalam kalimat deklaratif yang sama.

**Ketiadaan konteks temporal:** Titik waktu konsensus akademis mana yang direfleksikan informasi ini?

LLM mengisi semua ambiguitas ini dengan "urutan token yang paling masuk akal." Masuk akal bukan berarti akurat. Celah di antara keduanya adalah halusinasi.

---

## Mengapa Model Lebih Besar Tidak Bisa Menyelesaikan Ini

"Bukankah halusinasi akan berkurang ketika GPT-5 keluar?"

Akan berkurang. Tetapi tidak akan hilang.

Model yang lebih besar mempelajari pola yang lebih canggih dari data yang lebih banyak. Sehingga akurasi "masuk akal" naik.

Tetapi masalah fundamentalnya tidak berubah.

Selama input-nya bahasa alami, ambiguitas tetap ada. Selama data pelatihan bahasa alami, sumber tetap hilang. Selama output-nya bahasa alami, kepercayaan tidak terekspresikan. Selama informasi temporal tidak ada dalam struktur, waktu tetap kacau.

Bahkan jika Anda menskalakan model 100x, cacat struktural bahasa alami tidak tumbuh 100x -- tetapi juga tidak mencapai nol.

Ini bukan masalah resolusi. Ini masalah medium.

Sebanyak apa pun Anda meningkatkan resolusi foto hitam-putih, warna tidak muncul. Sebanyak apa pun Anda meningkatkan presisi bahasa alami, sumber, kepercayaan, dan konteks temporal tidak muncul dalam struktur.

Jika Anda ingin warna, Anda butuh film berwarna. Jika Anda ingin menghilangkan halusinasi, Anda butuh bahasa yang berbeda.

---

## Syarat untuk Solusi Struktural

Untuk menyelesaikan keempat cacat ini, struktur bahasa itu sendiri harus berbeda.

**Ambiguitas --> Strukturisasi eksplisit.** Ketika "He went to the bank" diubah ke bahasa terstruktur, "he" diselesaikan ke SIDX entitas spesifik, dan "bank" diselesaikan ke SIDX lembaga keuangan atau tepi sungai. Jika tidak bisa diselesaikan, "belum terselesaikan" dinyatakan secara eksplisit. Selesaikan ambiguitas, atau catat fakta bahwa ia ambigu.

**Ketiadaan sumber --> Sumber tertanam.** Setiap narasi secara struktural menyertakan entitas sumber. "Siapa yang membuat klaim ini" adalah bagian dari narasi. Ini bukan opsional. Jika field kosong, ditandai sebagai kosong.

**Ketiadaan kepercayaan --> Kepercayaan tertanam.** Setiap edge kata kerja memiliki field kepercayaan. "Pasti," "estimasi," "hipotetis" ditentukan secara struktural sebagai modifier kata kerja.

**Ketiadaan konteks temporal --> Konteks temporal tertanam.** Setiap narasi menyertakan konteks waktu. "Per kapan narasi ini" selalu ditentukan.

Yang dihilangkan dalam bahasa alami ada sebagai bagian dari struktur dalam bahasa terstruktur.

Ketika penghilangan tidak mungkin, ruang untuk halusinasi menyempit. [Mengapa Klarifikasi Diperlukan](/id/why/clarification/) menjelaskan prinsip ini. Ketika Anda tidak bisa berbicara tanpa basis, pernyataan tanpa basis tidak diproduksi.

---

## Akhir Halusinasi Terletak pada Penggantian Bahasa

Mari kita lihat pendekatan saat ini untuk mengurangi halusinasi.

**RAG (Retrieval-Augmented Generation):** Mengambil dokumen eksternal dan menyediakannya sebagai konteks. Efektif, tetapi dokumen yang diambil juga bahasa alami, sehingga masalah ambiguitas, ketiadaan sumber, dan ketiadaan kepercayaan ikut terbawa tanpa perubahan. [Mengapa RAG Tidak Cukup](/id/why/rag-not-enough/) membahas keterbatasan ini secara rinci.

**RLHF:** Melatih model untuk mengatakan "Saya tidak tahu" ketika tidak yakin. Mengurangi frekuensi halusinasi, tetapi tidak menyelesaikan masalah fundamental bahwa bahasa alami tidak punya struktur kepercayaan.

**Chain-of-Thought:** Mencatat proses penalaran dalam bahasa alami. Arahnya benar, tetapi medium catatannya bahasa alami, sehingga mewarisi cacat yang sama.

Semua pendekatan ini mencoba memitigasi halusinasi dalam kerangka bahasa alami. Mereka berhasil. Tetapi tidak fundamental.

Solusi fundamental adalah menghilangkan bahasa alami dari dalam AI.

Antarmuka dengan pengguna tetap dalam bahasa alami. Manusia terus berbicara dalam bahasa alami dan menerima jawaban dalam bahasa alami.

Tetapi bahasa yang digunakan AI untuk bernalar, mencatat, dan memverifikasi secara internal harus sesuatu selain bahasa alami.

Bahasa di mana sumber ada dalam struktur. Bahasa di mana kepercayaan ada dalam struktur. Bahasa di mana konteks temporal ada dalam struktur. Bahasa di mana ambiguitas ditangani secara eksplisit.

Bahasa lisan menciptakan suku. Tulisan menciptakan negara. Apa yang akan diciptakan bahasa ketiga?

Akhir halusinasi bukan pada model yang lebih besar tetapi pada bahasa yang lebih baik.

---

## Ringkasan

Halusinasi lahir dari empat cacat struktural bahasa alami.

1. **Ambiguitas:** Tidak bisa diselesaikan tanpa konteks. AI menebak, dan tebakan salah.
2. **Ketiadaan sumber:** Basis klaim hilang. Kombinasi tanpa basis difabrikasi.
3. **Ketiadaan kepercayaan:** Fakta dan estimasi diekspresikan dalam tata bahasa identik. AI tidak bisa membedakannya.
4. **Ketiadaan konteks temporal:** Informasi dari periode waktu berbeda tercampur.

Model yang lebih besar mengurangi halusinasi tetapi tidak bisa menghilangkannya. Tanpa mengubah medium, cacat struktural tetap ada.

Sebanyak apa pun Anda meningkatkan resolusi film hitam-putih, warna tidak muncul. Jika Anda ingin warna, Anda harus mengganti filmnya.

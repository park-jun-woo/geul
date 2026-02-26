---
title: "Mengapa MD/JSON/XML Tidak Bisa"
weight: 9
date: 2026-02-26T12:00:15+09:00
lastmod: 2026-02-26T12:00:15+09:00
tags: ["format", "JSON", "XML"]
summary: "Format yang ada tidak bisa membawa makna"
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Format terstruktur sudah ada. Jadi mengapa bahasa baru diperlukan?

---

## Keberatan Paling Umum

Ketika seseorang pertama kali menemui ide bahasa penalaran AI, hal pertama yang mereka katakan adalah:

"Format terstruktur sudah ada, bukan?"

Mereka benar. Sudah ada. Banyak.

Ada Markdown. Ada JSON. Ada XML. YAML, TOML, Protocol Buffers, MessagePack, CSV...

Dunia dibanjiri format data. Jadi mengapa AI masih berpikir dalam bahasa alami?

Untuk menjawab pertanyaan ini, kita harus menentukan tepat apa yang dilakukan setiap format dengan baik dan apa yang tidak bisa dilakukannya.

---

## Markdown: Memori Saat Ini Agen AI

Per 2026, format yang paling banyak digunakan oleh agen AI adalah Markdown.

Claude Code mengingat dalam file `.md`. Agen berbasis GPT juga meninggalkan catatan dalam Markdown. CLAUDE.md, memory.md, notes.md. Memori jangka panjang AI berdiri di atas Markdown saat ini.

Mengapa Markdown? Alasannya sederhana. LLM membaca dan menulis Markdown dengan baik. Markdown melimpah dalam data pelatihan, dan strukturnya cukup sederhana untuk generasi dan parsing yang mudah.

Tetapi Markdown adalah **format dokumen yang dimaksudkan untuk dibaca manusia.**

```markdown
# Status Proyek
## Strategi Cache
- Bitmask SIMD diadopsi (diputuskan 1/28)
- Akselerasi GPU sedang ditinjau
## Belum Terselesaikan
- Metode pembuatan kueri TBD
```

Bagaimana mesin menginterpretasikan ini?

Ada heading bagian bernama "Strategi Cache." Di bawahnya, ada item "Bitmask SIMD diadopsi." Ada tanggal "(1/28)" dalam tanda kurung.

Mesin tidak bisa memahami ini secara struktural. Ia bisa tahu dari `##` bahwa "Strategi Cache" adalah heading bagian, tetapi hubungan semantik bahwa itu "subtopik arsitektur" tidak ada di Markdown. Manusia tahu "1/28" adalah tanggal, tetapi mesin harus menebak. 28 Januari, atau satu per dua puluh delapan?

Pada akhirnya, untuk "memahami" Markdown, LLM harus melakukan interpretasi bahasa alami. Markdown adalah bahasa alami dengan indentasi ditambahkan -- bukan data terstruktur.

---

## JSON: Struktur Tanpa Makna

JSON melangkah satu langkah lebih jauh dari Markdown.

```json
{
  "entity": "Yi Sun-sin",
  "birth": "1545",
  "death": "1598",
  "occupation": "naval_commander"
}
```

Ada struktur. Pasangan key-value eksplisit. Mesin bisa mem-parse-nya. Field bisa diakses.

Tetapi ada masalah.

**JSON tidak tahu apa arti key "entity".**

Orang yang membuat JSON ini tahu "entity" berarti "objek." Di JSON orang lain, konsep yang sama bisa "name," "subject," atau "item."

```json
{"name": "Yi Sun-sin"}
{"subject": "Yi Sun-sin"}
{"item": "Yi Sun-sin"}
{"entity": "Yi Sun-sin"}
```

Empat JSON mengekspresikan hal yang sama, tetapi mesin tidak bisa tahu bahwa mereka sama.

JSON tidak punya **semantik bersama.** Ada struktur, tetapi tidak ada kesepakatan tentang apa arti struktur itu.

Setiap proyek membuat skemanya sendiri. Setiap API menggunakan nama field-nya sendiri. Menghubungkan skema A ke skema B membutuhkan lapisan transformasi lain.

Ini adalah Menara Babel. Struktur ada, tetapi tidak ada yang memahami struktur satu sama lain.

---

## XML: Pajak Keverbosaan

XML mencoba menyelesaikan masalah JSON.

Namespace, definisi skema (XSD), definisi tipe dokumen (DTD). Ia menyediakan meta-struktur yang mendefinisikan makna struktur.

```xml
<entity xmlns="http://example.org/schema">
  <name>Yi Sun-sin</name>
  <birth>
    <year>1545</year>
    <calendar>lunar</calendar>
  </birth>
  <death>
    <year>1598</year>
    <cause>killed_in_action</cause>
  </death>
</entity>
```

Makna bisa didefinisikan. Struktur bisa dipaksakan dengan skema. Lebih ketat dari JSON.

Tetapi XML punya masalah fatal.

**Ia verbose.**

Dalam XML di atas, informasi aktualnya adalah "Yi Sun-sin, 1545, 1598, killed_in_action." Sisanya tag. Tag pembuka dan penutup melebihi jumlah informasi.

Mengapa ini masalah untuk AI?

Jendela konteks LLM terbatas. Jika menyampaikan informasi yang sama membutuhkan 3x token, jumlah informasi yang muat di konteks menyusut menjadi sepertiga.

XML verbose agar manusia bisa membacanya dengan mudah. Bahasa penalaran AI tidak boleh punya pemborosan ini. Bagi LLM, tag `<name>` adalah pemborosan.

Dan XML adalah desain awal 2000-an. Ia dibuat di era ketika LLM tidak ada, untuk manusia dan perangkat lunak tradisional. Ia tidak pernah dirancang sebagai bahasa penalaran AI.

---

## Keterbatasan Bersama

Markdown, JSON, XML. Masing-masing dari tiga format punya kekuatannya, tetapi mereka berbagi keterbatasan umum.

**Mereka berbasis teks.** Semuanya diserialisasi menjadi string. Mesin harus mem-parse-nya untuk memprosesnya. Parsing adalah biaya.

Bahasa penalaran ideal adalah binary stream. Urutan kata 16-bit. Tidak perlu parsing. Dapat diinterpretasikan saat dibaca.

**Mereka dirancang sebelum era LLM.** Markdown dari 2004. JSON dari 2001. XML dari 1998. Mereka dirancang di era ketika konsep LLM tidak ada, untuk manusia atau perangkat lunak tradisional.

Bahasa penalaran AI harus dirancang di era LLM, untuk LLM. Prinsip desain "1 kata = 1 token" mengandaikan keberadaan LLM.


Indeks yang selaras secara semantik adalah ID makna yang terpadu secara global. Di mana pun ia digunakan, SIDX yang sama berarti hal yang sama. Tidak perlu konversi. Konsensus sudah built-in.

---

## Ringkasan

| Format | Struktur | Makna | Ramah LLM | Biner | Dukungan Klaim | Modifier Kata Kerja |
|--------|-----------|---------|---------------|--------|---------------|----------------|
| Markdown | Lemah | Tidak | Tinggi | Tidak | Tidak | Tidak |
| JSON | Ya | Tidak | Sedang | Tidak | Tidak | Tidak |
| XML | Ya | Sebagian | Rendah | Tidak | Tidak | Tidak |
| **Bahasa Penalaran Ideal** | **Ya** | **Ya** | **Tinggi** | **Ya** | **Ya** | **Ya** |

Format baru diperlukan bukan karena format yang ada buruk. Tetapi karena format yang ada dibuat di era berbeda, untuk tujuan berbeda.

Markdown dibuat untuk dokumen yang dibaca manusia. JSON dibuat untuk pertukaran data di web API. XML dibuat untuk serialisasi dokumen dan data tujuan umum.

Format untuk mencatat dan mengakumulasi penalaran AI. Itu belum ada.

Ketika tujuan berbeda, alat harus berbeda.

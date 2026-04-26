# 📥 Email Reader (for Obsidian)

Selamat tinggal inbox yang berantakan! `email-reader` adalah asisten AI yang membaca email Anda, membuatkan ringkasan cerdas, dan menyimpannya langsung ke dalam **Obsidian Vault** Anda sebagai catatan Markdown yang cantik.

## ✨ Fitur Utama

- 🧠 **AI Summarization**: Menggunakan Gemini AI untuk membuat ringkasan eksekutif dari isi email.
- 📂 **Obsidian Integration**: Otomatis membuat note baru dengan metadata lengkap (YAML frontmatter).
- 🧹 **Clean Markdown**: Mengonversi email HTML yang ribet menjadi Markdown yang bersih dan mudah dibaca.
- 🚫 **Smart Unsubscribe**: Email promosi otomatis dideteksi dan dikumpulkan ke dalam `Unsubscribe.md` agar Anda bisa berhenti berlangganan dengan satu klik.
- 🔄 **Multi-Account**: Mendukung banyak akun Gmail sekaligus via `gog` CLI.

## 🚀 Persiapan Cepat

### 1. Prasyarat
- [gog CLI](https://github.com/kilip/gog) terinstal dan sudah login (`gog auth login`).
- [uv](https://github.com/astral-sh/uv) untuk menjalankan script Python tanpa ribet install dependency manual.

### 2. Environment Variables
Set variabel berikut di terminal Anda (atau di file `.env`):

```bash
# Lokasi root vault Obsidian Anda
$env:OBSIDIAN_VAULT = "C:\Users\Nama\Documents\MyVault"

# Lokasi folder tujuan untuk menyimpan email (relatif/absolut)
$env:OBSIDIAN_INBOX_PATH = "C:\Users\Nama\Documents\MyVault\00-Inbox\Emails"
```

## 🛠️ Cara Penggunaan

Cukup jalankan perintah ini:

```bash
uv run skills/email-reader/email_reader.py
```

Script akan memproses semua email yang belum dibaca (**unread**) dan mengubahnya menjadi catatan di Obsidian.

## 🎨 Kustomisasi Tampilan

Semua tampilan note dihasilkan melalui templat di folder `tpl/`. Anda bisa bebas mengubahnya sesuai selera:
- `tpl/email.md`: Mengatur struktur note email utama.
- `tpl/unsubscribe_init.md`: Mengatur header file daftar unsubscribe.
- `tpl/unsubscribe.md`: Mengatur format checklist untuk email promo.

---

> 💡 **Tips**: Gunakan plugin **Dataview** di Obsidian untuk menampilkan daftar email terbaru di dashboard Anda!

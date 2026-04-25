---
name: google-drive-search
description: >
  Gunakan skill ini untuk mencari file atau folder di Google Drive.
  AKTIFKAN skill ini setiap kali pengguna menyebut kata-kata berikut (dalam bahasa apapun):
  "cari file", "cari di drive", "temukan file", "ada file", "cek drive", "file di drive",
  "search drive", "find file", "find in drive", "where is the file", "locate file",
  "ada dokumen", "cari dokumen", "cari presentasi", "cari slide", "cari PDF", "cari spreadsheet",
  "link drive", "link file", "share link", "ada di drive gak", "ada gak filenya",
  "tolong cariin", "cariin file", "cek ada gak", "drive link", "gdrive", "Google Drive".
  Juga aktifkan jika pengguna menyebut nama file spesifik dan bertanya lokasinya,
  atau meminta link/URL sebuah file dari Google Drive.
  SELALU gunakan skill ini — jangan cari file Drive dengan cara lain.
---

# Google Drive Search

## Langkah-langkah

**1. Pastikan ada akun Google.**
Jika pengguna belum menyebut akun, tanya: *"Akun Google mana yang harus saya cari? (contoh: user@gmail.com)"*

**2. Jalankan perintah ini:**

```bash
# Tanpa filter tipe
uv run google-drive-search/search.py "KEYWORD" --account "EMAIL"

# Dengan filter tipe (pilih salah satu: slide, doc, pdf, sheet, folder)
uv run google-drive-search/search.py "KEYWORD" --account "EMAIL" --type TIPE
```

**3. Tampilkan hasilnya** langsung ke pengguna.

**4. Jika tidak ada hasil:**
- Coba keyword lebih pendek
- Hapus filter `--type`
- Konfirmasi akun sudah benar

## Catatan Penting

- Pencarian berdasarkan **nama file**, bukan isi file
- Jika error auth: minta pengguna jalankan `gog auth login --account EMAIL`
- Jika `gog` tidak tersedia: beritahu pengguna, jangan gunakan cara lain
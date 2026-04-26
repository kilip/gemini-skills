---
name: email-reader
description: >
  Gunakan skill ini setiap kali pengguna ingin membaca, mengecek, atau memproses email baru.
  AKTIFKAN jika pengguna menyebut kata-kata berikut (bahasa apapun):
  "cek email", "ada email baru", "baca inbox", "email masuk", "email terbaru",
  "check email", "read email", "new email", "any email", "email hari ini",
  "ada pesan masuk", "inbox penuh", "lihat email", "email dari siapa",
  "ada surat masuk", "email belum dibaca", "unread email", "bacain email".
  SELALU gunakan skill ini — jangan proses email dengan cara lain.
---

# 📥 Email Reader

Baca email baru → buat catatan Obsidian → kelola unsubscribe list.

## Persiapan Environment

Skill ini membutuhkan beberapa environment variable agar sinkron dengan Obsidian Vault:

```bash
$env:OBSIDIAN_VAULT = "C:\Path\To\Your\Vault"
$env:OBSIDIAN_INBOX_PATH = "C:\Path\To\Your\Vault\00-Inbox\Emails"
```

## Jalankan Script

```bash
uv run skills/email-reader/email_reader.py
```

Script akan memproses semua akun yang terdaftar di `gog` secara otomatis.

## Apa yang Dilakukan Script

1. **Scan Inbox**: Ambil semua thread **unread** dari semua akun `gog`.
2. **Promo Handling**: Jika email berlabel `PROMOTION` atau `CATEGORY_PROMOTIONS`:
   - Tambahkan ke `Unsubscribe.md` di folder Emails.
   - Gunakan format checklist: `- [ ] [Nama](Link) - Subjek`.
   - Mark as read.
3. **Regular Email**:
   - Fetch isi lengkap dan konversi HTML ke Markdown.
   - **AI Summary**: Gemini membuat ringkasan eksekutif.
   - **Obsidian Note**: Buat file `.md` baru menggunakan templat `tpl/email.md`.
   - Mark as read.

## Struktur Templat

Skill ini menggunakan sistem templat eksternal di folder `tpl/`:
- `email.md`: Struktur note email (metadata YAML, detail, ringkasan, isi lengkap).
- `unsubscribe_init.md`: Header untuk file `Unsubscribe.md`.
- `unsubscribe.md`: Format baris untuk daftar unsubscribe.

## Troubleshooting

| Error | Solusi |
|-------|--------|
| `Failed to list unread emails` | Jalankan: `gog auth login --account EMAIL` |
| `OBSIDIAN_VAULT not set` | Set env var `OBSIDIAN_VAULT` sesuai lokasi vault Anda. |
| `Template not found` | Pastikan folder `tpl/` ada di dalam direktori skill. |
| `inscriptis` or `google-generativeai` missing | Script akan otomatis menginstall via `uv` (inline metadata). |

## Self-Check Sebelum Selesai

- Beritahu pengguna berapa email yang berhasil diproses.
- Sebutkan jika ada email promo yang masuk ke daftar unsubscribe.
- Jika 0 email diproses, katakan "Inbox aman! Nggak ada email baru."
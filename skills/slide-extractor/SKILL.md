---
name: slide-extractor
description: >
  Use this skill EVERY TIME you need to extract or read text content from a PowerPoint (.pptx) file.
  ALWAYS use this skill when: a .pptx file exists in telegram_files/ and needs to be processed,
  when the user says "proses slide", "baca presentasi", "extract slide", or uploads a .pptx file via Telegram.
  This skill handles text extraction including slides that are image-only (Canva, AI-generated, etc.).
  Use this as STEP 1 before doing any analysis, categorization, or inventory creation of a presentation.
---

# Slide Extractor

Extract all text from a `.pptx` file and save the result as a `.md` file in the same folder.

## When to Use

Use this skill FIRST whenever you need to read the content of a `.pptx` file — before writing summaries, categories, tags, or inventory notes.

---

## Step-by-Step Instructions

### Step 1: Identify the input file

The `.pptx` file is in the `telegram_files/` directory.

Example:
```
telegram_files/Mengenal_Generasi_Z.pptx
```

### Step 2: Run the extractor

Run this exact command (replace the filename):

```bash
uv run skills/slide-extractor/extract_pptx.py telegram_files/Mengenal_Generasi_Z.pptx
```

The script will automatically save the output as a `.md` file in the **same folder** with the **same name**:

```
telegram_files/Mengenal_Generasi_Z.md  ← output saved here
```

You do NOT need to specify an output path. The script handles it automatically.

### Step 3: Read the output file

After the script finishes, read the output `.md` file:

```
telegram_files/Mengenal_Generasi_Z.md
```

Use the content of this file for the next steps (executive brief, categorization, inventory, etc.).

---

## Output Format

The `.md` file contains text per slide:

```markdown
---
title: Mengenal_Generasi_Z
filename: Mengenal_Generasi_Z.pptx
slide_count: 32
---

# Slide 1
Judul slide pertama
Subjudul atau teks lainnya

---

# Slide 2
Teks dari slide kedua

---
```

---

## How OCR Works (Simple Version)

The script tries two methods in order:

1. **Direct text extraction** — reads text shapes directly (fast, works for most slides)
2. **OCR fallback** — if a slide contains images instead of text shapes, it runs OCR automatically
   - First tries **Tesseract** (fast)
   - If Tesseract fails, falls back to **EasyOCR** (slower but more accurate)

You do NOT need to choose or configure anything. It happens automatically.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Script runs but output file is empty | The slide may be fully image-based. OCR will run — wait for it to finish. |
| OCR is very slow | Normal for image-heavy files (20MB+). Can take several minutes. |
| `tesseract: command not found` warning | Script will auto-fallback to EasyOCR. No action needed. |

---

## Dependencies

Handled automatically by `uv`. No manual install needed.

- `python-pptx` — reads PowerPoint files
- `pytesseract` — Tesseract OCR wrapper
- `easyocr` — AI-based OCR fallback
- `Pillow`, `numpy`, `opencv-python-headless` — image processing
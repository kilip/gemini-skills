# Gemini Skills 🛠️

This repository is a collection of custom skills for the **Gemini CLI**. These skills are designed to automate various productivity tasks using Python, `uv`, and advanced AI libraries.

## 🚀 Available Skills

| Skill | Description |
| :--- | :--- |
| **[slide-extractor](./skills/slide-extractor)** | Extracts text from PPTX files using **Waterfall OCR** logic (Tesseract & EasyOCR). Perfect for AI-generated slides (NotebookLM, Canva) that consist entirely of images. |
| **[google-drive](./skills/google-drive)** | Wrapper for searching and uploading files/folders in Google Drive using the `gog` CLI. |
| **[email-processor](./skills/email-processor)** | Automated triaging and categorization of emails. |
| **[email-reader](./skills/email-reader)** | AI-powered automated reading and summarization of email content. |
| **[telegram-slide-processor](./skills/telegram-slide-processor)** | Automated workflow for processing presentation files received via Telegram. |
| **[slide-inventory](./skills/slide-inventory)** | Management and inventory system for presentation slide content. |

## 📂 Project Structure

```text
.
├── samples/                # Sample PPTX files for testing
├── skills/                 # Core logic for various skills
│   ├── email-processor/    # Email triaging automation
│   ├── email-reader/       # Email summarization logic
│   ├── google-drive/       # GDrive integration (search/upload)
│   ├── slide-extractor/    # PPTX text & OCR extraction
│   ├── slide-inventory/    # Slide management system
│   └── telegram-slide-processor/ # Telegram file workflow
└── README.md
```

## 🛠️ Requirements

- **Python 3.10+**
- **[uv](https://github.com/astral-sh/uv)**: For running Python scripts portably with automatic dependency management.
- **Tesseract OCR**: (Optional) For faster local OCR performance.
- **gog CLI**: Required for Google Drive integration features.

## 📦 Usage

You can use these skills directly via the Gemini CLI or run them locally:

```powershell
# Example: Run the PPT extractor
uv run skills/slide-extractor/extract_pptx.py <file.pptx>
```

Each skill folder contains a `SKILL.md` file with detailed instructions designed for AI Agents.

---
Created and Maintained by **Anthonius Munthi and Gem**.

## ⚖️ License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

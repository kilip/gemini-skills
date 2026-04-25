# Slide Extractor Skill 🚀

A powerful tool to extract text from PowerPoint (.pptx) files, including image-only slides (AI-generated slides from NotebookLM, Canva, etc.).

## 🛠 Features
- **Waterfall OCR**: Prioritizes Tesseract (fast) and fallbacks to EasyOCR (accurate) if needed.
- **Deep Scan**: Recursively extracts text from grouped shapes and nested elements.
- **Smart Output**: Automatically saves extraction results to a `.md` file in the same directory.
- **Auto-Install**: Fully supports `uv` and `package.json` for seamless installation via `npx skills`.

## 🚀 Usage

Ensure you have `uv` installed, then run:

```bash
uv run extract_pptx.py <path_to_pptx_file>
```

The script will generate a Markdown file with the same name as the input file in the same folder.

### Options
You can force a specific OCR engine:
```bash
uv run extract_pptx.py file.pptx --engine tesseract
uv run extract_pptx.py file.pptx --engine easyocr
```

## 📦 Requirements
- **Tesseract OCR**: (Optional but recommended) Install via `choco install tesseract -y`.
- **EasyOCR**: Automatically downloads AI models on the first run (requires internet connection).

## 📂 File Structure
- `extract_pptx.py`: Main Python script.
- `SKILL.md`: Documentation for AI Agents.
- `package.json`: Configuration for skill installation.
- `requirements.txt`: Python dependency list.

---
Created with ❤️ for **Pak Bos**.

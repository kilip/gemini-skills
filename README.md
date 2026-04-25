# Gemini Skills 🛠️

A library of AI Agent Skills designed to automate productivity workflows using Python, `uv`, and advanced AI. Each skill follows the Agent Skills open standard, for compatibility with coding agents such as Antigravity, Gemini CLI, Claude Code, and Cursor.

## 🚀 Installation & Discovery

Install any skill from this repository using the `skills` CLI. This command will automatically detect your active coding agents and place the skill in the appropriate directory.

```bash
# List all available skills in this repository
npx skills add kilip/gemini-skills --list

# Install a specific skill
npx skills add kilip/gemini-skills --skill slide-extractor --global
```

## 🛠️ Available Skills

### slide-extractor
Extract text from PowerPoint (.pptx) slides using smart OCR waterfall logic (Tesseract & EasyOCR). Perfect for AI-generated slides that consist entirely of images.

```bash
npx skills add kilip/gemini-skills --skill slide-extractor --global
```

### google-drive
Wrapper for searching and uploading files/folders in Google Drive using the `gog` CLI. Provides clean Markdown-formatted results with metadata.

```bash
npx skills add kilip/gemini-skills --skill google-drive --global
```

### email-processor
Workflow for processing email notes in Obsidian (replying, archiving, deleting) and moving them out of the Inbox.

```bash
npx skills add kilip/gemini-skills --skill email-processor --global
```

### email-reader
AI-powered automated reading and summarization of email content, helping you prioritize what's important.

```bash
npx skills add kilip/gemini-skills --skill email-reader --global
```

### telegram-slide-processor
Automated workflow for processing presentation files received via Telegram, including extraction and organization.

```bash
npx skills add kilip/gemini-skills --skill telegram-slide-processor --global
```

### slide-inventory
Management and inventory system for presentation slide content, keeping your knowledge base organized.

```bash
npx skills add kilip/gemini-skills --skill slide-inventory --global
```

## 📂 Repository Structure

Every skill directory within `skills/` follows a standardized structure to ensure the AI agent has everything it needs to perform its tasks.

```text
.
├── LICENSE
├── README.md
├── samples/                # Sample files for testing
└── skills/
    └── [skill-name]/
        ├── SKILL.md        — The "Mission Control" for the agent
        └── scripts/        — Executable scripts (Python, Bash, etc.)
```

## 🛠️ Requirements

- **Python 3.10+**
- **[uv](https://github.com/astral-sh/uv)**: For running Python scripts portably with automatic dependency management.
- **Tesseract OCR**: (Optional) For faster local OCR performance.
- **gog CLI**: Required for Google Drive and Email integration features.

## ⚖️ License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
Created and Maintained by **Anthonius Munthi and Gem** with love ❤️ and coffee ☕

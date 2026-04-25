---
name: google-drive-search
description: Search for files and folders in Google Drive and return a Markdown-formatted list with links and metadata.
---

# Google Drive Search Skill

Use this skill to search for files or folders in Google Drive. It provides a convenient way to find documents, spreadsheets, presentations, and other files using keywords and returns them in a clean Markdown format.

## When to Use
- When the user asks to find a specific file in Google Drive.
- When you need to search for documents related to a specific topic or project.
- When you need the direct link to a Google Drive file.

## Prerequisites
- The `gog` CLI tool must be installed and configured on the system.
- Access to Google Drive must be authenticated via `gog`.

## Usage

Always use `uv run` to execute the search script and specify the target account using the **required** `--account` parameter.

### Search Files
To search for files containing a specific keyword in the name for a given account:

```bash
uv run google-drive-search/search.py "your-keyword" --account "user@gmail.com"
```

### Filter by Type
You can filter results by file type using the `--type` (or `-t`) parameter. Supported types are: `slide`, `doc`, `pdf`, `sheet`, and `folder`.

#### Search for Slides
```bash
uv run google-drive-search/search.py "Presentation" --account "user@gmail.com" --type slide
```

#### Search for PDFs
```bash
uv run google-drive-search/search.py "Invoice" --account "user@gmail.com" --type pdf
```

## Output Format
The skill returns a Markdown list of results, including:
- File-type specific icon (e.g., 📁 for folders, 📝 for docs).
- Clickable filename linking to the file on Google Drive.
- Metadata such as last modified date and file size.

Example output:
- 📝 [Project Proposal](https://docs.google.com/document/d/...) | 🕒 2024-07-20 | 📦 1.2 MB
- 📁 [Assets Folder](https://drive.google.com/drive/folders/...) | 🕒 2024-07-15

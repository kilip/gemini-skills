---
name: google-drive
description: Comprehensive skill for interacting with Google Drive, including searching and uploading files.
---

# Google Drive Hub Skill

This skill provides a unified entry point for interacting with Google Drive. It allows agents to search for files and upload new content using the `gog` CLI.

## Capabilities

- **Search**: Find files and folders using keywords, and get Markdown-formatted results with metadata.
- **Upload**: Upload local files or directories to specific Google Drive accounts.

## Sub-Skills

This skill is organized into specialized modules:
- **Search**: `google-drive/search`
- **Upload**: `google-drive/upload`

## Usage

Agents should navigate to the appropriate subdirectory for specific tasks:
- For searching: `skills/google-drive/search/`
- For uploading: `skills/google-drive/upload/`

Refer to the `SKILL.md` in those directories for detailed instructions.

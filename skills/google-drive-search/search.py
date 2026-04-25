#!/usr/bin/env uv run
# /// script
# dependencies = []
# ///

import subprocess
import json
import sys
import argparse
import os
import io

# Force UTF-8 for stdout to support emojis on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def format_size(size_bytes):
    if not size_bytes:
        return ""
    try:
        size = int(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
    except:
        return ""
    return ""

def get_icon(mime_type):
    if not mime_type:
        return "📄"
    
    # Mapping mimeType to emojis
    mapping = {
        "application/vnd.google-apps.folder": "📁",
        "application/vnd.google-apps.document": "📝",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "📝",
        "application/msword": "📝",
        "application/vnd.google-apps.spreadsheet": "📊",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "📊",
        "application/vnd.ms-excel": "📊",
        "application/vnd.google-apps.presentation": "📽️",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": "📽️",
        "application/vnd.ms-powerpoint": "📽️",
        "application/vnd.google-apps.form": "📋",
        "application/pdf": "📕",
        "application/zip": "📦",
        "application/x-zip-compressed": "📦",
        "application/x-7z-compressed": "📦",
        "application/x-rar-compressed": "📦",
        "text/plain": "📄",
        "text/markdown": "📝",
        "text/html": "🌐",
    }
    
    if mime_type in mapping:
        return mapping[mime_type]
    
    if mime_type.startswith("image/"):
        return "🖼️"
    if mime_type.startswith("video/"):
        return "🎬"
    if mime_type.startswith("audio/"):
        return "🎵"
        
    return "📄"

def search_drive(keyword, account=None, file_type=None):
    # Construct the query
    query_parts = []
    if keyword:
        query_parts.append(f"name contains '{keyword}'")
    
    if file_type:
        type_mapping = {
            "slide": [
                "application/vnd.google-apps.presentation",
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "application/vnd.ms-powerpoint"
            ],
            "doc": [
                "application/vnd.google-apps.document",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/msword"
            ],
            "pdf": ["application/pdf"],
            "sheet": [
                "application/vnd.google-apps.spreadsheet",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/vnd.ms-excel"
            ],
            "folder": ["application/vnd.google-apps.folder"]
        }
        
        if file_type in type_mapping:
            mimes = type_mapping[file_type]
            mime_query = " or ".join([f"mimeType = '{m}'" for m in mimes])
            query_parts.append(f"({mime_query})")

    query = " and ".join(query_parts)
    
    # Base command
    cmd = ["gog", "drive", "search", query, "--json"]
    
    # Handle account if provided or if GOG_ACCOUNT env var exists
    if account:
        cmd.extend(["--account", account])
    elif "GOG_ACCOUNT" in os.environ:
        cmd.extend(["--account", os.environ["GOG_ACCOUNT"]])

    try:
        # Run gog command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}", file=sys.stderr)
            return

        # Parse JSON output
        data = json.loads(result.stdout)
        files = data.get("files", [])
        
        if not files:
            search_desc = f"'{keyword}'"
            if file_type:
                search_desc += f" with type '{file_type}'"
            print(f"No files found containing {search_desc}", file=sys.stderr)
            return

        # Output as Markdown list with icons and metadata
        for file in files:
            name = file.get("name", "Untitled")
            link = file.get("webViewLink", "")
            mime_type = file.get("mimeType", "")
            icon = get_icon(mime_type)
            
            # Metadata
            modified = file.get("modifiedTime", "")
            if modified:
                modified = modified.split("T")[0]
            
            size = format_size(file.get("size"))
            
            if not link:
                link = file.get("alternateLink", "#")
            
            # Construct metadata string
            meta = []
            if modified: meta.append(f"🕒 {modified}")
            if size: meta.append(f"📦 {size}")
            
            meta_str = f" | {' | '.join(meta)}" if meta else ""
            
            print(f"- {icon} [{name}]({link}){meta_str}")
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrapper for gog drive search")
    parser.add_argument("keyword", help="Search keyword for file/folder name")
    parser.add_argument("-a", "--account", help="Google account email", required=True)
    parser.add_argument("-t", "--type", help="Filter by file type", choices=["slide", "doc", "pdf", "sheet", "folder"])
    
    args = parser.parse_args()
    
    if not args.keyword:
        parser.print_help()
        sys.exit(1)
        
    search_drive(args.keyword, args.account, args.type)

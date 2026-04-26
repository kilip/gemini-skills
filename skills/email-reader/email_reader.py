#!/usr/bin/env python3
# /// script
# dependencies = ["inscriptis"]
# ///

import os
import re
import subprocess
import sys
import argparse
import json
import shutil
import time
from datetime import datetime

GEMINI_BIN = shutil.which("gemini") or "gemini"
GEMINI_MODEL = "gemini-2.5-flash-lite"


# ──────────────────────────────────────────
# Config & Templates
# ──────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TPL_DIR = os.path.join(SCRIPT_DIR, "tpl")


def load_template(name):
    """Load a template from the tpl directory."""
    path = os.path.join(TPL_DIR, f"{name}.md")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()



def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def fail(msg):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def run(cmd, input_data=None, check=True):
    """Run shell command. Returns stdout string or None on failure."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            input=input_data, check=check, encoding='utf-8', errors='replace'
        )
        return result.stdout.strip() if result.stdout else ""
    except subprocess.CalledProcessError as e:
        log(f"Command failed: {cmd}")
        log(f"Stderr: {e.stderr.strip() if e.stderr else ''}")
        return None


def ask_gemini(prompt):
    """Send prompt to Gemini CLI, return raw text response."""
    cmd = f'{GEMINI_BIN} -m {GEMINI_MODEL} -p -'
    output = run(cmd, input_data=prompt)
    if not output:
        log("Gemini returned empty response.")
    return output


def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text[:60]


# ──────────────────────────────────────────
# Email fetching
# ──────────────────────────────────────────

def get_all_accounts():
    log("Fetching all accounts from gog...")
    out = run('gog auth list --json')
    if not out:
        log("Raw output from gog auth list is empty.")
        fail("Failed to list accounts. Ensure gog is authenticated.")
    try:
        data = json.loads(out)
        # Support both 'tokens' and 'accounts' keys
        tokens = data.get("tokens") or data.get("accounts") or []
        emails = [t.get("email") for t in tokens if t.get("email")]
        if not emails:
            log(f"No emails found in JSON. Raw output: {out[:500]}")
        return emails
    except json.JSONDecodeError:
        log(f"Invalid JSON from gog auth list. Raw output: {out[:500]}")
        fail(f"Invalid JSON from gog auth list.")


def list_unread(account):
    log("Fetching unread threads...")
    out = run(f'gog gmail list "is:unread" -a {account} --json')
    if not out:
        fail("Failed to list unread emails. Check: gog auth list")
    try:
        data = json.loads(out)
        return data.get("threads", [])
    except json.JSONDecodeError:
        fail(f"Invalid JSON from gog gmail list: {out[:200]}")


def is_promo(thread):
    labels = thread.get("labels", [])
    return "PROMOTION" in labels or "CATEGORY_PROMOTIONS" in labels


def add_to_unsubscribe_list(thread_data, account, unsubscribe_path):
    messages = thread_data.get("messages", [])
    if not messages:
        return

    # Use first message for metadata
    msg = messages[0]
    headers = msg.get("payload", {}).get("headers", [])
    
    sender = next((h.get("value") for h in headers if h.get("name").lower() == "from"), "Unknown")
    subject = next((h.get("value") for h in headers if h.get("name").lower() == "subject"), "No Subject")
    unsub_header = next((h.get("value") for h in headers if h.get("name").lower() == "list-unsubscribe"), "")

    # Clean up sender (remove email)
    sender_name = re.sub(r'<[^>]+>', '', sender).strip()

    # Clean up unsub_header
    links = re.findall(r'<(https?://[^>]+)>', unsub_header)
    clean_unsub = links[0] if links else ""
    
    # If no https link, try any link
    if not clean_unsub:
        all_links = re.findall(r'<([^>]+)>', unsub_header)
        clean_unsub = all_links[0] if all_links else ""

    # Prepare sender display (link or just name)
    if clean_unsub and clean_unsub.startswith("http"):
        sender_display = f"[{sender_name}]({clean_unsub})"
    else:
        sender_display = sender_name

    # Initialize file if not exists
    if not os.path.exists(unsubscribe_path):
        init_tpl = load_template("unsubscribe_init")
        init_content = init_tpl.format(tanggal=datetime.now().strftime("%Y-%m-%d"))
        os.makedirs(os.path.dirname(unsubscribe_path), exist_ok=True)
        with open(unsubscribe_path, "w", encoding="utf-8") as f:
            f.write(init_content)
        log(f"Initialized Unsubscribe List: {unsubscribe_path}")

    unsub_tpl = load_template("unsubscribe")
    entry = unsub_tpl.format(
        sender_display=sender_display,
        subject=subject,
        account=account
    )
    
    if not entry.endswith("\n"):
        entry += "\n"

    try:
        # Append to the file
        with open(unsubscribe_path, "a", encoding="utf-8") as f:
            f.write(entry)
        log(f"Added to Unsubscribe List: {sender_name}")
    except Exception as e:
        log(f"Error updating Unsubscribe List: {e}")


def fetch_thread(thread_id, account):
    log(f"Fetching thread {thread_id}...")
    out = run(f'gog gmail thread get {thread_id} -a {account} --json')
    if not out:
        log(f"Failed to fetch thread {thread_id}. Skipping.")
        return None
    try:
        data = json.loads(out)
        return data.get("thread", data)
    except json.JSONDecodeError:
        log(f"Invalid JSON for thread {thread_id}. Skipping.")
        return None


def mark_read(thread_id, account):
    result = run(f'gog gmail thread modify {thread_id} --remove UNREAD -a {account}', check=False)
    if result is None:
        log(f"Warning: Failed to mark thread {thread_id} as read.")
    else:
        log(f"Marked as read: {thread_id}")


# ──────────────────────────────────────────
# AI summarization
# ──────────────────────────────────────────

def summarize_email(subject, sender, body):
    prompt = f"""Kamu adalah asisten yang membantu merangkum email secara singkat dalam Bahasa Indonesia.

Subjek: {subject}
Dari: {sender}
Isi Email:
{body[:8000]}

Buat ringkasan singkat 2-3 kalimat yang menjelaskan inti email ini.
Hanya tulis ringkasannya saja, tanpa preamble atau label tambahan."""

    summary = ask_gemini(prompt)
    return summary or "Gagal membuat ringkasan."


# ──────────────────────────────────────────
# Obsidian note writer
# ──────────────────────────────────────────

def write_obsidian_note(thread_data, account, inbox_path):
    messages = thread_data.get("messages", [])
    if not messages:
        log("Thread has no messages. Skipping.")
        return None

    first_msg = messages[0]
    headers = {h["name"].lower(): h["value"] for h in first_msg.get("payload", {}).get("headers", [])}

    thread_id = thread_data.get("id", "unknown")
    subject = headers.get("subject", "(Tanpa Subjek)")
    sender_raw = headers.get("from", "")
    date_raw = headers.get("date", "")
    to = headers.get("to", account)

    # Parse sender name & email
    match = re.match(r'^(.*?)\s*<(.+?)>$', sender_raw)
    if match:
        sender_name = match.group(1).strip().strip('"')
        sender_email = match.group(2).strip()
    else:
        sender_name = sender_raw
        sender_email = sender_raw

    # Parse date
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_raw)
        tanggal = dt.strftime("%Y-%m-%d")
        tanggal_display = dt.strftime("%d %B %Y, %H:%M")
    except Exception:
        tanggal = datetime.now().strftime("%Y-%m-%d")
        tanggal_display = datetime.now().strftime("%d %B %Y, %H:%M")

    # Extract plain text body from all messages
    full_body = extract_body(messages)

    # AI summary
    log(f"Summarizing: {subject}")
    ringkasan = summarize_email(subject, sender_raw, full_body)

    # Filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(subject)
    filename = f"{date_str}-{thread_id}-{slug}.md"
    filepath = os.path.join(inbox_path, filename)

    # Build note using template
    date_display = datetime.now().strftime("%d %B %Y")
    lampiran_md = "- [ ] *(tidak ada lampiran)*"
    
    tpl = load_template("email")
    note = tpl.format(
        thread_id=thread_id,
        subject=subject,
        tanggal=tanggal,
        sender_name=sender_name,
        sender_email=sender_email,
        to=to,
        tanggal_display=tanggal_display,
        ringkasan=ringkasan,
        full_body=full_body[:15000],
        lampiran_md=lampiran_md,
        date_display=date_display,
        gemini_model=GEMINI_MODEL
    )

    os.makedirs(inbox_path, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(note)

    log(f"Note created: {filename}")
    return filename, subject, sender_name, sender_email


def extract_body(messages):
    """Extract plain text body from message list."""
    parts_text = []
    for msg in messages:
        payload = msg.get("payload", {})
        text = extract_parts(payload)
        if text:
            parts_text.append(text)
    
    body = "\n\n---\n\n".join(parts_text) if parts_text else "(Isi email kosong)"
    # Strip trailing whitespace from each line
    body = "\n".join(line.rstrip() for line in body.splitlines())
    # Collapse 3 or more newlines into just 2
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body.strip()


def extract_parts(payload):
    """Recursively extract text/plain or text/html, converting HTML to Markdown via inscriptis."""
    mime = payload.get("mimeType", "")
    body_data = payload.get("body", {}).get("data", "")
    import base64

    # 1. Handle HTML parts (Prioritize)
    if mime == "text/html" and body_data:
        try:
            html = base64.urlsafe_b64decode(body_data + "==").decode("utf-8", errors="replace")
            from inscriptis import get_text
            return get_text(html)
        except Exception:
            pass

    # 2. Handle Plain Text parts
    if mime == "text/plain" and body_data:
        try:
            return base64.urlsafe_b64decode(body_data + "==").decode("utf-8", errors="replace")
        except Exception:
            pass

    # 3. Recurse into multipart
    parts = payload.get("parts", [])
    html_res = None
    plain_res = None

    for part in parts:
        res = extract_parts(part)
        if not res: continue
        
        # Heuristic: if it looks like HTML-derived text (has many lines/links), it's likely better
        if part.get("mimeType") == "text/html":
            html_res = res
        elif part.get("mimeType") == "text/plain":
            plain_res = res
        else:
            # Nested parts
            return res

    return html_res or plain_res or ""


# ──────────────────────────────────────────
# Daily journal sync
# ──────────────────────────────────────────







# ──────────────────────────────────────────
# Main
# ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Email reader → Obsidian note generator")
    args = parser.parse_args()

    vault = os.getenv("OBSIDIAN_VAULT")
    emails_path = os.getenv("OBSIDIAN_INBOX_PATH")
    unsubscribe_path = emails_path + "/Unsubscribe.md"
    
    missing_envs = []
    if not vault: missing_envs.append("OBSIDIAN_VAULT")
    if not emails_path: missing_envs.append("OBSIDIAN_INBOX_PATH")
    
    if missing_envs:
        fail(f"Environment variables belum diset: {', '.join(missing_envs)}")

    accounts = get_all_accounts()
    if not accounts:
        log("No accounts found.")
        return

    for account in accounts:
        log(f"=== Processing account: {account} ===")
        # 1. List unread
        threads = list_unread(account)
        if not threads:
            log("No unread emails found.")
            continue

        log(f"Found {len(threads)} unread thread(s).")
        processed = 0

        for thread in threads:
            time.sleep(1)  # Delay to prevent Google API rate limit
            thread_id = thread.get("id")
            if not thread_id:
                continue

            # 2. Check for promos
            if is_promo(thread):
                log(f"Promotional email detected: {thread_id}. Adding to unsubscribe list.")
                thread_data = fetch_thread(thread_id, account)
                if thread_data:
                    add_to_unsubscribe_list(thread_data, account, unsubscribe_path)
                mark_read(thread_id, account)
                continue

            # 3. Fetch full thread for regular emails
            thread_data = fetch_thread(thread_id, account)
            if not thread_data:
                continue

            # 4. Write Obsidian note
            result = write_obsidian_note(thread_data, account, emails_path)
            if not result:
                continue

            filename, subject, sender_name, sender_email = result

            # 5. Done

            # 6. Mark as read
            mark_read(thread_id, account)
            processed += 1

        log(f"Done for {account}. {processed} email(s) processed.")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Checks the Proton Drive CLI download page for a version newer than the one
pinned in flake.nix. If newer, extracts the linux/x64 sha512 checksum and
emits GitHub Actions step outputs: should_update, new_version, sha512.
"""
import os
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from packaging.version import InvalidVersion, Version

PAGE_URL = "https://proton.me/download/drive/cli/index.html"
FLAKE_PATH = Path("flake.nix")


def get_current_version() -> str:
    content = FLAKE_PATH.read_text()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        sys.exit('Could not find `version = "...";` in flake.nix')
    return match.group(1)


def fetch_page() -> str:
    resp = requests.get(PAGE_URL, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_latest_version(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else ""
    match = re.search(r"(\d+\.\d+\.\d+)\s*$", (title or "").strip())
    if not match:
        sys.exit(f"Could not find a version number in <title>: {title!r}")
    return match.group(1)


def parse_linux_x64_sha512(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for row in soup.find_all("tr"):
        cells = row.find_all(["td", "th"])
        if not cells:
            continue
        platform = cells[0].get_text(strip=True).lower()
        if platform == "linux/x64":
            if len(cells) < 3:
                sys.exit(f"Row for linux/x64 has fewer than 3 cells: {row}")
            checksum = cells[2].get_text(strip=True).strip("`").strip()
            if not re.fullmatch(r"[0-9a-fA-F]{128}", checksum):
                sys.exit(f"Unexpected sha512 checksum format: {checksum!r}")
            return checksum.lower()
    sys.exit("Could not find a table row for platform 'linux/x64'")


def write_output(name: str, value: str) -> None:
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if not gh_output:
        print(f"{name}={value}")
        return
    with open(gh_output, "a") as f:
        f.write(f"{name}={value}\n")


def main() -> None:
    current_version = get_current_version()
    html = fetch_page()
    latest_version = parse_latest_version(html)

    try:
        is_newer = Version(latest_version) > Version(current_version)
    except InvalidVersion as exc:
        sys.exit(f"Could not compare versions: {exc}")

    print(f"Current version (flake.nix): {current_version}")
    print(f"Latest version (proton.me):  {latest_version}")

    if not is_newer:
        print("No update needed.")
        write_output("should_update", "false")
        return

    sha512 = parse_linux_x64_sha512(html)
    print(f"New version found: {latest_version}")
    print(f"linux/x64 sha512:  {sha512}")

    write_output("should_update", "true")
    write_output("new_version", latest_version)
    write_output("sha512", sha512)


if __name__ == "__main__":
    main()

import os
import re
from pathlib import Path

def update_version(flake_content: str, new_version: str) -> str:
    content, n = re.subn(
        r'(version\s*=\s*")[^"]+(")',
        rf'\g<1>{new_version}\g<2>',
        flake_content,
        count=1,
    )
    if n != 1:
        raise SystemExit("Failed to update `version` in flake.nix")
    return content

def update_hash(flake_content: str, new_hash: str) -> str:
    content, n = re.subn(
        r'(\s*hash\s*=\s*")[^"]+(")',
        rf'\g<1>{new_hash}\g<2>',
        flake_content,
        count=1,
    )
    if n != 1:
        raise SystemExit("Failed to update x86_64-linux hash in flake.nix")
    return content

def main() -> None:
    new_version = os.environ["NEW_VERSION"]
    new_hash = os.environ["NEW_HASH"]

    path = Path("flake.nix")
    content = path.read_text()

    content = update_version(content, new_version)

    content = update_hash(content, new_hash)

    path.write_text(content)

if __name__ == "__main__":
    main()
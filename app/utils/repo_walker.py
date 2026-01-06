import os
from pathlib import Path
import pathspec
from typing import Dict

def is_binary(file_path: Path) -> bool:
    """
    Check if a file is binary by sniffing the first 1024 bytes for null characters.
    """
    try:
        if not file_path.is_file():
            return True
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except Exception:
        return True

def gather_repository_content(root_path: str = ".", max_size_mb: int = 10) -> Dict[str, str]:
    """
    Safely gathers content of all non-binary, non-ignored files in the repository.
    """
    root = Path(root_path).resolve()
    content_map = {}
    total_size = 0
    max_size_bytes = max_size_mb * 1024 * 1024

    # Load .gitignore
    gitignore_path = root / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
    else:
        spec = pathspec.PathSpec.from_lines('gitwildmatch', [])

    # We also want to explicitly ignore .git directory and common build artifacts
    # if they aren't in .gitignore for some reason.
    manual_ignore = [".git", "__pycache__", ".pytest_cache", "venv", ".venv", "node_modules", "v12_log.txt"]

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative_path = path.relative_to(root)
        
        # Check manual ignores first (faster)
        if any(ignored in relative_path.parts for ignored in manual_ignore):
            continue

        # Check gitignore
        if spec.match_file(str(relative_path)):
            continue

        # Check binary
        if is_binary(path):
            continue

        # Check size before reading
        file_size = path.stat().st_size
        if total_size + file_size > max_size_bytes:
            # Skip this file to avoid exceeding total limit
            continue

        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                content_map[str(relative_path)] = content
                total_size += len(content.encode('utf-8'))
        except Exception:
            # Skip files that can't be read
            continue

    return content_map

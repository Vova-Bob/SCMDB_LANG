#!/usr/bin/env python3
"""
auto_update_translation.py — Automation script for Ukrainian SCMDB translation

This script automates the process of updating the Ukrainian translation for SCMDB:
1. Updates the SCMDB_LANG repository (gets new templates)
2. Fixes encoding issues in your global.ini file
3. Builds the translation JSON file
4. Optionally commits changes to git

Usage:
    # Basic usage (builds translation from LIVE global.ini)
    python auto_update_translation.py

    # Use PTU version
    python auto_update_translation.py --ptu

    # Custom paths
    python auto_update_translation.py --global-ini path/to/global.ini --output-dir path/to/output

    # With git commit (commits to current branch)
    python auto_update_translation.py --commit

Requirements:
    - Python 3.10+
    - Git (for --commit option)
    - Your Star Citizen installation with Ukrainian global.ini
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent.absolute()
DEFAULT_SC_INI_LIVE = Path("F:/Games/StarCitizen/LIVE/Data/Localization/korean_(south_korea)/global.ini")
DEFAULT_SC_INI_PTU = Path("F:/Games/StarCitizen/PTU/Data/Localization/korean_(south_korea)/global.ini")
FIXED_INI_NAME = "global_ua_fixed.ini"


# Character fixes for Ukrainian encoding
CHAR_FIXES = {
    'í': 'і', 'ì': 'і', 'î': 'і',  # Latin i variants -> Ukrainian i
    'ý': 'и', 'ÿ': 'и',              # Latin y variants -> Ukrainian y
    'ε': 'є',                        # Greek epsilon -> Ukrainian je
    'ı': 'і', 'ĭ': 'і',              # Other i variants
    '\u2019': "'",  # Right single quotation mark
    '\u2018': "'",  # Left single quotation mark
    '\u02bc': "'",  # Modifier letter apostrophe
    '\u201d': '"',  # Right double quotation mark
    '\u201c': '"',  # Left double quotation mark
    '\u201e': '"',  # Double low-9 quotation mark
    '\u2013': '-',  # En dash
}


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_step(step: int, text: str) -> None:
    """Print a step indicator."""
    print(f"\n[Step {step}] {text}")
    print("-" * 70)


def fix_encoding_line(line: str) -> str:
    """Fix encoding issues in a single line."""
    for wrong, right in CHAR_FIXES.items():
        line = line.replace(wrong, right)
    line = line.replace('В.I.П.', 'ВІП')
    line = line.replace('В.І.П.', 'ВІП')
    return line


def fix_encoding_file(input_path: Path, output_path: Path) -> tuple[int, int]:
    """Fix encoding issues in the entire file. Returns (lines_total, lines_fixed)."""
    line_num = 0
    fixes_count = 0

    with open(input_path, 'r', encoding='utf-8-sig') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:

        for line in infile:
            line_num += 1
            original = line
            fixed = fix_encoding_line(line)

            if original != fixed:
                fixes_count += 1

            outfile.write(fixed)

    return line_num, fixes_count


def update_repository(repo_path: Path) -> bool:
    """Update git repository. Returns True if successful."""
    if not repo_path.exists():
        print(f"  [!] Repository not found: {repo_path}")
        return False

    try:
        result = subprocess.run(
            ['git', 'pull'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print("  [OK] Repository updated successfully")
            return True
        else:
            print(f"  [ERROR] Git pull failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("  [ERROR] Git pull timed out")
        return False
    except FileNotFoundError:
        print("  [ERROR] Git not found in PATH")
        return False
    except Exception as e:
        print(f"  [ERROR] Error updating repository: {e}")
        return False


def build_translation(template_path: Path, global_ini_path: Path, output_dir: Path) -> bool:
    """Run build_lang_template.py script."""
    try:
        cmd = [
            sys.executable,
            SCRIPT_DIR / "build_lang_template.py",
            "--translate",
            str(global_ini_path)
        ]

        result = subprocess.run(
            cmd,
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print("  [OK] Translation built successfully")

            # Move the generated file to output directory
            json_files = list(SCRIPT_DIR.glob("lang-*.json"))
            if json_files:
                latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
                dest = output_dir / latest_file.name

                # Try to copy, if fails, try to remove destination first
                try:
                    shutil.copy2(latest_file, dest)
                except PermissionError:
                    try:
                        dest.unlink()
                        shutil.copy2(latest_file, dest)
                    except:
                        pass

                print(f"  [OK] File saved to: {dest}")
                return True

        print(f"  [ERROR] Build failed: {result.stderr}")
        return False

    except subprocess.TimeoutExpired:
        print("  [ERROR] Build timed out")
        return False
    except Exception as e:
        print(f"  [ERROR] Error building translation: {e}")
        return False


def git_commit_changes(repo_path: Path, message: str) -> bool:
    """Commit changes to git repository."""
    try:
        # Add changes
        subprocess.run(
            ['git', 'add', '.'],
            cwd=repo_path,
            capture_output=True,
            check=True
        )

        # Commit
        result = subprocess.run(
            ['git', 'commit', '-m', message],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("  [OK] Changes committed to git")
            return True
        else:
            if "nothing to commit" in result.stdout.lower():
                print("  [INFO] No changes to commit")
                return True
            print(f"  [ERROR] Git commit failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"  [ERROR] Error committing changes: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Automate Ukrainian SCMDB translation updates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_update_translation.py
  python auto_update_translation.py --ptu
  python auto_update_translation.py --commit --push
  python auto_update_translation.py --global-ini /path/to/global.ini
        """
    )

    parser.add_argument(
        '--ptu',
        action='store_true',
        help='Use PTU version instead of LIVE'
    )

    parser.add_argument(
        '--global-ini',
        type=Path,
        help='Path to your global.ini file (auto-detected if not specified)'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=SCRIPT_DIR,
        help='Output directory for translation files (default: script directory)'
    )

    parser.add_argument(
        '--no-update',
        action='store_true',
        help='Skip updating SCMDB_LANG repository'
    )

    parser.add_argument(
        '--commit',
        action='store_true',
        help='Commit changes to git (in current directory)'
    )

    parser.add_argument(
        '--push',
        action='store_true',
        help='Push commits to remote after committing'
    )

    args = parser.parse_args()

    print_header("SCMDB Ukrainian Translation Auto-Updater")

    # Determine paths
    sc_ini_path = args.global_ini or (DEFAULT_SC_INI_PTU if args.ptu else DEFAULT_SC_INI_LIVE)
    version_name = "PTU" if args.ptu else "LIVE"

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Update repository
    print_step(1, f"Updating SCMDB_LANG repository")
    if args.no_update:
        print("  [INFO] Skipping repository update (--no-update flag)")
    else:
        update_repository(SCRIPT_DIR)

    # Step 2: Fix encoding
    print_step(2, f"Fixing encoding in {version_name} global.ini")

    if not sc_ini_path.exists():
        print(f"  [ERROR] File not found: {sc_ini_path}")
        print(f"  [INFO] Use --global-ini to specify the correct path")
        return 1

    fixed_ini_path = args.output_dir / FIXED_INI_NAME
    lines_total, lines_fixed = fix_encoding_file(sc_ini_path, fixed_ini_path)

    print(f"  [OK] Processed {lines_total:,} lines")
    print(f"  [OK] Fixed {lines_fixed:,} lines with encoding issues")
    print(f"  [OK] Saved to: {fixed_ini_path}")

    # Step 3: Build translation
    print_step(3, "Building SCMDB translation")

    success = build_translation(None, fixed_ini_path, args.output_dir)

    if not success:
        return 1

    # Step 4: Git operations
    if args.commit:
        print_step(4, "Committing changes to git")

        version_tag = datetime.now().strftime("%Y.%m.%d")
        commit_message = f"Update Ukrainian translation {version_tag} ({version_name})"

        if git_commit_changes(args.output_dir, commit_message):
            if args.push:
                try:
                    subprocess.run(
                        ['git', 'push'],
                        cwd=args.output_dir,
                        capture_output=True,
                        check=True
                    )
                    print("  [OK] Changes pushed to remote")
                except Exception as e:
                    print(f"  [ERROR] Push failed: {e}")

    # Summary
    print_header("Update Complete!")

    print(f"Version: {version_name}")
    print(f"Source: {sc_ini_path}")
    print(f"Output: {args.output_dir}")
    print(f"\nFiles created:")
    print(f"  - {fixed_ini_path.name}")
    print(f"  - lang-*.json")

    print(f"\nNext steps:")
    print(f"  - Upload the JSON file to a public URL (GitHub/Gist)")
    print(f"  - Use in SCMDB: scmdb.dev?lang=<YOUR_JSON_URL>")

    return 0


if __name__ == '__main__':
    sys.exit(main())

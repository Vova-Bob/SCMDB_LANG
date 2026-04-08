#!/usr/bin/env python3
"""
fix_encoding.py - Fixes common encoding issues in Ukrainian localization files.

Problems fixed:
1. Latin characters with diacritics (í, ý, ε, etc.) replaced with Ukrainian equivalents (і, и, є, etc.)
2. Different apostrophe types normalized to standard apostrophe
3. Multiple quote types normalized
"""

import sys
import re

# Mapping of incorrect characters to correct Ukrainian ones
CHAR_FIXES = {
    # Latin i with acute -> Ukrainian i
    'í': 'і',
    'ì': 'і',
    'î': 'і',
    # Latin y with acute -> Ukrainian и (sometimes used as i)
    'ý': 'и',
    'ÿ': 'и',
    # Greek epsilon -> Ukrainian є
    'ε': 'є',
    # Other problematic characters
    'ı': 'і',
    'ĭ': 'і',
    # Quotes and apostrophes (using Unicode values)
    '\u2019': "'",  # Right single quotation mark
    '\u2018': "'",  # Left single quotation mark
    '\u02bc': "'",  # Modifier letter apostrophe
    '\u201d': '"',  # Right double quotation mark
    '\u201c': '"',  # Left double quotation mark
    '\u201e': '"',  # Double low-9 quotation mark
    '\u2014': '—',   # Em dash (keep as is)
    '\u2013': '-',   # En dash
}

def fix_line(line: str) -> str:
    """Fix encoding issues in a single line."""
    # Apply character replacements
    for wrong, right in CHAR_FIXES.items():
        line = line.replace(wrong, right)

    # Fix specific common patterns
    line = line.replace('В.I.П.', 'ВІП')  # VIP abbreviation
    line = line.replace('В.І.П.', 'ВІП')

    return line

def fix_file(input_path: str, output_path: str) -> None:
    """Fix encoding issues in the entire file."""
    line_num = 0
    fixes_count = 0

    print(f"Reading from: {input_path}")
    print(f"Writing to: {output_path}")
    print()

    with open(input_path, 'r', encoding='utf-8-sig') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:

        for line in infile:
            line_num += 1
            original = line
            fixed = fix_line(line)

            if original != fixed:
                fixes_count += 1
                if fixes_count <= 10:  # Show first 10 fixes
                    try:
                        print(f"Line {line_num}: Fixed")
                    except:
                        pass  # Skip output if encoding error

            outfile.write(fixed)

    print(f"Processed {line_num:,} lines")
    print(f"Fixed {fixes_count:,} lines with encoding issues", file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python fix_encoding.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    fix_file(input_file, output_file)
    print("\nDone!")

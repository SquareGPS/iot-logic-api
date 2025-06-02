#!/usr/bin/env python3
"""
Simple markdown to PDF converter.

Features:
- Converts markdown to PDF using system browser (Chrome/Edge)
- No complex dependencies or system libraries required
- Professional styling optimized for documentation
- Automatic fallback to printable HTML if PDF conversion fails
- Works reliably on Windows systems

Usage: python dead_simple_converter.py [--input FILE] [--output FILE]
Dependencies: markdown

No fancy templates, no complex processing - just works.
"""

import argparse
from pathlib import Path
import markdown
import subprocess
import os
import sys

def create_simple_html(markdown_content: str) -> str:
    """Convert markdown to simple HTML with inline CSS."""

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['codehilite', 'tables', 'fenced_code'])
    html_body = md.convert(markdown_content)

    # Simple HTML template
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Navixy IoT Logic API Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
        h3 {{ color: #34495e; }}
        pre {{ background: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        code {{ background: #f1f3f4; padding: 2px 4px; border-radius: 3px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        blockquote {{ border-left: 4px solid #3498db; margin: 0; padding-left: 20px; background: #f8f9fa; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""

    return html

def find_chrome():
    """Find Chrome executable on Windows."""
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def find_edge():
    """Find Edge executable on Windows."""
    possible_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def main():
    parser = argparse.ArgumentParser(description='Simple MD to PDF converter')
    parser.add_argument('--input', '-i', default='API_documentation_full.md', help='Input markdown file')
    parser.add_argument('--output', '-o', help='Output PDF file')

    args = parser.parse_args()

    input_file = Path(args.input)
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = input_file.with_suffix('.pdf')

    print(f"🚀 Converting {input_file} to {output_file}")

    # Check input file exists
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)

    # Read markdown
    print("📖 Reading markdown...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    print(f"📊 Content size: {len(markdown_content):,} characters")

    # Convert to HTML
    print("🔄 Converting to HTML...")
    try:
        html_content = create_simple_html(markdown_content)
    except Exception as e:
        print(f"❌ Error converting to HTML: {e}")
        sys.exit(1)

    # Save HTML file
    html_file = output_file.with_suffix('.html')
    print(f"💾 Saving HTML: {html_file}")
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except Exception as e:
        print(f"❌ Error saving HTML: {e}")
        sys.exit(1)

    # Try to convert to PDF using browser
    print("🌐 Converting to PDF using browser...")

    # Find browser
    browser_path = find_chrome()
    browser_name = "Chrome"

    if not browser_path:
        browser_path = find_edge()
        browser_name = "Edge"

    if browser_path:
        print(f"✅ Found {browser_name}: {browser_path}")

        # Convert using headless browser
        cmd = [
            browser_path,
            '--headless',
            '--disable-gpu',
            '--print-to-pdf=' + str(output_file.resolve()),
            '--no-pdf-header-footer',
            'file:///' + str(html_file.resolve()).replace('\\', '/')
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if output_file.exists():
                size = output_file.stat().st_size
                print(f"✅ PDF created successfully!")
                print(f"📊 Size: {size:,} bytes ({size/1024/1024:.1f} MB)")

                # Clean up HTML file
                try:
                    html_file.unlink()
                except:
                    pass

                return
            else:
                print(f"⚠️  Browser command failed")

        except subprocess.TimeoutExpired:
            print("⚠️  Browser conversion timed out")
        except Exception as e:
            print(f"⚠️  Browser conversion error: {e}")

    # If we reach here, automatic conversion failed
    print("⚠️  Automatic PDF conversion failed, but HTML file was created!")
    print(f"📄 HTML file: {html_file}")
    print("\n💡 Manual conversion steps:")
    print(f"   1. Double-click to open: {html_file}")
    print("   2. Press Ctrl+P to print")
    print("   3. Select 'Save as PDF' or 'Microsoft Print to PDF'")
    print("   4. Choose your filename and save")
    print("\nThe HTML file is styled for perfect PDF printing! 🎯")

if __name__ == "__main__":
    main()
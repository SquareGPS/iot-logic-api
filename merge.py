#!/usr/bin/env python3
"""
Documentation merge script with content grooming and TOC generation.

Features:
- Analyzes markdown files in /docs directory
- Parses toc.json structure and matches files
- Removes stoplight-id frontmatter blocks
- Filters out orphaned sections (GitHub links, placeholder content)
- Generates optional table of contents
- Merges clean content into single markdown file

Usage: python working_groomed_merge.py [--toc] [--toc-depth N]
Output: API_documentation_full.md
"""

import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import re

@dataclass
class FileInfo:
    """Information about a markdown file."""
    path: Path
    relative_path: str
    filename_no_ext: str
    size: int

@dataclass
class TOCItem:
    """Parsed TOC item with metadata."""
    type: str
    title: str
    uri: Optional[str] = None
    slug: Optional[str] = None
    items: Optional[List['TOCItem']] = None
    matched_file: Optional[FileInfo] = None
    level: int = 1

class ContentGroomer:
    """Handles content cleaning and grooming operations."""

    @staticmethod
    def clean_content(content: str) -> str:
        """Clean and groom markdown content."""
        if not content:
            return content

        print(f"🧹 Grooming content ({len(content)} chars)...")

        # Remove stoplight-id frontmatter blocks
        content = ContentGroomer._remove_stoplight_ids(content)

        # Remove orphaned sections
        content = ContentGroomer._remove_orphaned_sections(content)

        # Clean up whitespace
        content = ContentGroomer._normalize_whitespace(content)

        print(f"🧹 After grooming: {len(content)} chars")

        return content

    @staticmethod
    def _remove_stoplight_ids(content: str) -> str:
        """Remove stoplight-id frontmatter blocks."""
        original_len = len(content)

        # Remove frontmatter blocks with stoplight-id (various patterns)
        patterns = [
            r'^---\s*\nstoplight-id:\s*[a-zA-Z0-9]+\s*\n---\s*\n?',  # Simple frontmatter
            r'^---\s*\nstoplight-id:\s*[a-zA-Z0-9]+\s*\ntags:\s*\[[^\]]*\]\s*\n---\s*\n?',  # With tags
            r'^---\s*\ntags:\s*\[[^\]]*\]\s*\nstoplight-id:\s*[a-zA-Z0-9]+\s*\n---\s*\n?',  # Tags first
        ]

        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)

        removed = original_len - len(content)
        if removed > 0:
            print(f"  🗑️  Removed {removed} chars of stoplight-id content")

        return content

    @staticmethod
    def _remove_orphaned_sections(content: str) -> str:
        """Remove orphaned section headers."""
        original_len = len(content)

        # Remove specific orphaned headers
        orphaned_patterns = [
            r'^# Navixy IoT Logic API\s*\n?',
            r'^# GitHub repository\s*\n?',
            r'^# User documentation\s*\n?',
            r'^# Back to Navixy website\s*\n?',
            r'^# Contact us\s*\n?',
            r'^# Resources\s*\n?',
        ]

        for pattern in orphaned_patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)

        # Remove placeholder content sections
        content = re.sub(
            r'^# [^\n]*\n\nThe beginning of an awesome article\.\.\.\s*\n?',
            '',
            content,
            flags=re.MULTILINE
        )

        removed = original_len - len(content)
        if removed > 0:
            print(f"  🗑️  Removed {removed} chars of orphaned sections")

        return content

    @staticmethod
    def _normalize_whitespace(content: str) -> str:
        """Normalize whitespace."""
        # Remove excessive newlines (more than 2 consecutive)
        content = re.sub(r'\n{3,}', '\n\n', content)

        # Remove trailing whitespace from lines
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

        # Ensure content ends with single newline
        content = content.rstrip() + '\n' if content.strip() else ''

        return content

class DocumentationMerger:
    def __init__(self, repo_root: Path, generate_toc: bool = False, toc_depth: int = 3):
        self.repo_root = repo_root
        self.docs_dir = repo_root / 'docs'
        self.toc_path = repo_root / 'toc.json'
        self.output_path = repo_root / 'API_documentation_full.md'
        self.generate_toc = generate_toc
        self.toc_depth = toc_depth

        self.file_map: Dict[str, FileInfo] = {}
        self.toc_items: List[TOCItem] = []
        self.matched_files: Set[str] = set()
        self.content_toc: List[tuple] = []

        # External patterns to filter out
        self.external_patterns = [
            r'https?://',
            r'github\.com',
            r'navixy\.com',
            r'Back to.*website',
            r'GitHub repository',
            r'User documentation',
            r'Contact us',
            r'Resources',
        ]

    def stage1_analyze_file_tree(self) -> bool:
        """Stage 1: Analyze file structure."""
        print("🔍 Stage 1: Analyzing file tree")
        print("=" * 50)

        if not self.docs_dir.exists():
            print(f"❌ Docs directory not found: {self.docs_dir}")
            return False

        md_files = list(self.docs_dir.rglob("*.md"))
        print(f"📄 Found {len(md_files)} markdown files")

        for md_file in md_files:
            relative_path = md_file.relative_to(self.docs_dir)
            relative_str = str(relative_path).replace('\\', '/')
            filename_no_ext = relative_str.replace('.md', '')

            file_info = FileInfo(
                path=md_file,
                relative_path=relative_str,
                filename_no_ext=filename_no_ext,
                size=md_file.stat().st_size
            )

            # Create lookup keys
            lookup_keys = [
                filename_no_ext,
                filename_no_ext.lower(),
                Path(filename_no_ext).name,
                Path(filename_no_ext).name.lower(),
            ]

            for key in lookup_keys:
                if key not in self.file_map:
                    self.file_map[key] = file_info

            print(f"   📄 {relative_str} ({file_info.size} bytes)")

        print(f"✅ Created file mapping with {len(md_files)} files")
        return True

    def stage2_parse_toc_structure(self) -> bool:
        """Stage 2: Parse TOC structure."""
        print(f"\n🔍 Stage 2: Parsing TOC structure")
        print("=" * 50)

        if not self.toc_path.exists():
            print(f"❌ TOC file not found: {self.toc_path}")
            return False

        try:
            with open(self.toc_path, 'r', encoding='utf-8') as f:
                toc_data = json.load(f)
            print(f"✅ Loaded toc.json successfully")
        except Exception as e:
            print(f"❌ Error loading toc.json: {e}")
            return False

        if isinstance(toc_data, dict) and 'items' in toc_data:
            # Filter out external items
            filtered_items = self._filter_external_items(toc_data['items'])
            self.toc_items = self._parse_toc_items(filtered_items)
            print(f"📄 Parsed {self._count_toc_items(self.toc_items)} TOC items")
            return True
        else:
            print(f"❌ Unexpected toc.json structure")
            return False

    def _filter_external_items(self, items: List[dict]) -> List[dict]:
        """Filter out external links."""
        filtered = []

        for item in items:
            if not isinstance(item, dict):
                continue

            title = item.get('title', '')
            uri = item.get('uri', '')

            # Check if external
            if self._is_external_item(title, uri):
                print(f"🧹 Filtering out: '{title}'")
                continue

            # Handle nested items
            if item.get('type') == 'group' and 'items' in item:
                filtered_nested = self._filter_external_items(item['items'])
                if filtered_nested:
                    new_item = item.copy()
                    new_item['items'] = filtered_nested
                    filtered.append(new_item)
            else:
                filtered.append(item)

        return filtered

    def _is_external_item(self, title: str, uri: str) -> bool:
        """Check if item is external."""
        text = f"{title} {uri}".lower()
        return any(re.search(pattern.lower(), text) for pattern in self.external_patterns)

    def _parse_toc_items(self, items: List[dict], level: int = 1) -> List[TOCItem]:
        """Parse TOC items."""
        parsed = []

        for item in items:
            if not isinstance(item, dict):
                continue

            toc_item = TOCItem(
                type=item.get('type', ''),
                title=item.get('title', ''),
                uri=item.get('uri'),
                slug=item.get('slug'),
                level=level
            )

            if 'items' in item:
                toc_item.items = self._parse_toc_items(item['items'], level + 1)

            parsed.append(toc_item)

        return parsed

    def _count_toc_items(self, items: List[TOCItem]) -> int:
        """Count TOC items."""
        count = len(items)
        for item in items:
            if item.items:
                count += self._count_toc_items(item.items)
        return count

    def stage3_match_toc_to_files(self) -> bool:
        """Stage 3: Match TOC to files."""
        print(f"\n🔍 Stage 3: Matching TOC to files")
        print("=" * 50)

        self._match_items_recursive(self.toc_items)

        total_items = self._count_content_items(self.toc_items)
        matched_items = self._count_matched_items(self.toc_items)

        print(f"\n📊 Matched {matched_items}/{total_items} content items")
        return matched_items > 0

    def _match_items_recursive(self, items: List[TOCItem]):
        """Match TOC items to files."""
        for item in items:
            if item.type == 'item':
                matched_file = self._find_matching_file(item)
                if matched_file:
                    item.matched_file = matched_file
                    self.matched_files.add(matched_file.filename_no_ext)
                    print(f"✅ '{item.title}' → {matched_file.relative_path}")
                else:
                    print(f"❌ '{item.title}' → No file found")

            if item.items:
                self._match_items_recursive(item.items)

    def _find_matching_file(self, toc_item: TOCItem) -> Optional[FileInfo]:
        """Find matching file."""
        search_keys = self._generate_search_keys(toc_item)

        for key in search_keys:
            if key in self.file_map:
                return self.file_map[key]

        return None

    def _generate_search_keys(self, toc_item: TOCItem) -> List[str]:
        """Generate search keys."""
        keys = []

        # From URI
        if toc_item.uri:
            uri_key = self._extract_filename_from_uri(toc_item.uri)
            if uri_key:
                keys.extend([uri_key, uri_key.lower()])

        # From slug
        if toc_item.slug:
            keys.extend([toc_item.slug, toc_item.slug.lower()])

        # From title
        if toc_item.title:
            title_variants = [
                toc_item.title.replace(' ', '-'),
                toc_item.title.replace(' ', '-').lower(),
                toc_item.title.replace(' ', '_'),
                toc_item.title.replace(' ', '_').lower(),
            ]
            keys.extend(title_variants)

        return list(dict.fromkeys(keys))  # Remove duplicates

    def _extract_filename_from_uri(self, uri: str) -> Optional[str]:
        """Extract filename from URI."""
        if not uri:
            return None

        clean_uri = uri.lstrip('/')
        if clean_uri.endswith('.md'):
            clean_uri = clean_uri[:-3]
        if clean_uri.startswith('docs/'):
            clean_uri = clean_uri[5:]

        return clean_uri if clean_uri else None

    def _count_content_items(self, items: List[TOCItem]) -> int:
        """Count content items."""
        count = 0
        for item in items:
            if item.type == 'item':
                count += 1
            if item.items:
                count += self._count_content_items(item.items)
        return count

    def _count_matched_items(self, items: List[TOCItem]) -> int:
        """Count matched items."""
        count = 0
        for item in items:
            if item.type == 'item' and item.matched_file:
                count += 1
            if item.items:
                count += self._count_matched_items(item.items)
        return count

    def stage4_merge_content(self) -> bool:
        """Stage 4: Merge content."""
        print(f"\n🔍 Stage 4: Merging content with grooming")
        print("=" * 50)

        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write("# Navixy IoT Logic API Documentation\n\n")
                f.write("*Generated from https://developers.navixy.com/docs/iot-logic-api/overview*\n\n")
            print(f"✅ Created output file: {self.output_path}")
        except Exception as e:
            print(f"❌ Error creating output: {e}")
            return False

        # Generate TOC if requested
        if self.generate_toc:
            self._generate_toc()

        # Merge content
        content_written = self._merge_items_recursive(self.toc_items)

        # Insert TOC if generated
        if self.generate_toc and self.content_toc:
            self._insert_toc()

        # Final stats
        try:
            final_size = self.output_path.stat().st_size
            print(f"\n✅ Merge complete: {final_size:,} bytes")
            if self.generate_toc:
                print(f"📑 TOC entries: {len(self.content_toc)}")
        except Exception as e:
            print(f"❌ Error checking output: {e}")
            return False

        return True

    def _generate_toc(self):
        """Generate table of contents."""
        self._collect_toc_entries(self.toc_items)

    def _collect_toc_entries(self, items: List[TOCItem]):
        """Collect TOC entries."""
        for item in items:
            if item.type in ['group', 'item'] and item.title and item.level <= self.toc_depth:
                anchor = self._create_anchor(item.title)
                self.content_toc.append((item.level, item.title, anchor))

            if item.items:
                self._collect_toc_entries(item.items)

    def _create_anchor(self, title: str) -> str:
        """Create anchor from title."""
        anchor = title.lower().replace(' ', '-')
        anchor = re.sub(r'[^a-z0-9\-]', '', anchor)
        anchor = re.sub(r'-+', '-', anchor).strip('-')
        return anchor

    def _insert_toc(self):
        """Insert table of contents."""
        try:
            with open(self.output_path, 'r', encoding='utf-8') as f:
                content = f.read()

            toc_lines = ["## Table of Contents\n"]
            for level, title, anchor in self.content_toc:
                indent = "  " * (level - 1)
                toc_lines.append(f"{indent}- [{title}](#{anchor})")

            toc_section = "\n".join(toc_lines) + "\n\n---\n\n"

            lines = content.split('\n')
            lines.insert(3, toc_section)

            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

        except Exception as e:
            print(f"⚠️  Could not insert TOC: {e}")

    def _merge_items_recursive(self, items: List[TOCItem], level: int = 1) -> bool:
        """Merge TOC items recursively."""
        content_written = False

        for item in items:
            if item.type == 'group':
                if item.title:
                    header = f"\n{'#' * level} {item.title}\n\n"
                    print(f"📝 Section: {'#' * level} {item.title}")

                    with open(self.output_path, 'a', encoding='utf-8') as f:
                        f.write(header)
                    content_written = True

                if item.items:
                    if self._merge_items_recursive(item.items, level + 1):
                        content_written = True

            elif item.type == 'item':
                if item.matched_file:
                    # Read and groom content
                    groomed_content = self._get_groomed_content(item.matched_file)

                    if groomed_content.strip():
                        # Write section header
                        if item.title:
                            header = f"\n{'#' * level} {item.title}\n\n"
                            print(f"📝 Content: {'#' * level} {item.title}")

                            with open(self.output_path, 'a', encoding='utf-8') as f:
                                f.write(header)
                                f.write(groomed_content)
                                f.write("\n\n")
                            content_written = True
                    else:
                        print(f"⚠️  Skipped '{item.title}' - no content after grooming")
                else:
                    print(f"⚠️  No file for '{item.title}'")

            elif item.type == 'divider':
                with open(self.output_path, 'a', encoding='utf-8') as f:
                    f.write("\n---\n\n")
                content_written = True

        return content_written

    def _get_groomed_content(self, file_info: FileInfo) -> str:
        """Get groomed content from file."""
        try:
            with open(file_info.path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Apply grooming
            groomed = ContentGroomer.clean_content(content)

            return groomed

        except Exception as e:
            print(f"❌ Error reading {file_info.path}: {e}")
            return ""

    def run_all_stages(self) -> bool:
        """Run all stages."""
        print("🚀 STARTING CLEAN DOCUMENTATION MERGE")
        print("=" * 60)

        if self.generate_toc:
            print(f"📑 TOC will be generated (depth: {self.toc_depth})")

        stages = [
            self.stage1_analyze_file_tree,
            self.stage2_parse_toc_structure,
            self.stage3_match_toc_to_files,
            self.stage4_merge_content
        ]

        for stage in stages:
            if not stage():
                return False

        print(f"\n🎉 MERGE COMPLETED SUCCESSFULLY!")
        print(f"🧹 Content has been groomed and cleaned")
        return True

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Clean Documentation Merger')
    parser.add_argument('--toc', action='store_true', help='Generate table of contents')
    parser.add_argument('--toc-depth', type=int, default=3, help='TOC depth (default: 3)')

    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    merger = DocumentationMerger(repo_root, generate_toc=args.toc, toc_depth=args.toc_depth)

    success = merger.run_all_stages()

    if success:
        print(f"\n✅ Clean merge completed!")
        print(f"📄 Output: {merger.output_path}")
        if args.toc:
            print(f"📑 TOC included (depth {args.toc_depth})")
    else:
        print(f"\n❌ Merge failed")

if __name__ == "__main__":
    main()
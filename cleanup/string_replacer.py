#!/usr/bin/env python3
"""
String replacer script that replaces all occurrences of a string in:
- File contents (for text files)
- File names
- Directory names
"""

import os
import sys
import argparse
from pathlib import Path
import mimetypes
import traceback


def is_text_file(file_path):
    """Check if a file is likely a text file based on its mimetype."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        return mime_type.startswith('text/') or mime_type in [
            'application/json',
            'application/xml',
            'application/javascript',
            'application/x-yaml',
            'application/x-sh',
            'application/x-python-code'
        ]
    
    # Try to read a small portion to detect if it's text
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(512)
            # Check for null bytes (binary indicator)
            if b'\x00' in chunk:
                return False
            # Try to decode as UTF-8
            try:
                chunk.decode('utf-8')
                return True
            except UnicodeDecodeError:
                return False
    except:
        return False


def replace_in_file_content(file_path, search_str, replace_str):
    """Replace string in file content if it's a text file."""
    if not is_text_file(file_path):
        return False
    
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if replacement is needed
        if search_str in content:
            new_content = content.replace(search_str, replace_str)
            
            # Write back the modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  Modified content in: {file_path}")
            return True
    except Exception as e:
        print(f"  Error processing file {file_path}: {e}")
    
    return False


def get_new_name(old_name, search_str, replace_str):
    """Get the new name after string replacement."""
    if search_str in old_name:
        return old_name.replace(search_str, replace_str)
    return None


def process_directory(root_path, search_str, replace_str):
    """Process all files and directories recursively."""
    root_path = Path(root_path).resolve()
    
    if not root_path.exists():
        print(f"Error: Path '{root_path}' does not exist.")
        return
    
    # Collect all paths first to avoid issues with renaming during traversal
    all_paths = []
    
    # If root_path is a file, just process it
    if root_path.is_file():
        all_paths.append(root_path)
    else:
        # Collect all files and directories
        for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
            dirpath = Path(dirpath)
            
            # Add files
            for filename in filenames:
                all_paths.append(dirpath / filename)
            
            # Add directories (excluding root)
            if dirpath != root_path:
                all_paths.append(dirpath)
    
    # Statistics
    files_content_modified = 0
    files_renamed = 0
    dirs_renamed = 0
    
    # Process all collected paths
    for path in all_paths:
        if path.is_file():
            # Replace in file content
            if replace_in_file_content(path, search_str, replace_str):
                files_content_modified += 1
            
            # Check if file needs renaming
            new_name = get_new_name(path.name, search_str, replace_str)
            if new_name and new_name != path.name:
                new_path = path.parent / new_name
                try:
                    path.rename(new_path)
                    print(f"  Renamed file: {path} -> {new_path}")
                    files_renamed += 1
                except Exception as e:
                    print(f"  Error renaming file {path}: {e}")
        
        elif path.is_dir():
            # Check if directory needs renaming
            new_name = get_new_name(path.name, search_str, replace_str)
            if new_name and new_name != path.name:
                new_path = path.parent / new_name
                try:
                    path.rename(new_path)
                    print(f"  Renamed directory: {path} -> {new_path}")
                    dirs_renamed += 1
                except Exception as e:
                    print(f"  Error renaming directory {path}: {e}")
    
    # Check if root directory itself needs renaming (only if it's a directory)
    if root_path.is_dir():
        new_name = get_new_name(root_path.name, search_str, replace_str)
        if new_name and new_name != root_path.name:
            new_path = root_path.parent / new_name
            try:
                root_path.rename(new_path)
                print(f"  Renamed root directory: {root_path} -> {new_path}")
                dirs_renamed += 1
            except Exception as e:
                print(f"  Error renaming root directory {root_path}: {e}")
    
    # Print summary
    print("\nSummary:")
    print(f"  Files with content modified: {files_content_modified}")
    print(f"  Files renamed: {files_renamed}")
    print(f"  Directories renamed: {dirs_renamed}")


def main():
    parser = argparse.ArgumentParser(
        description="Replace all occurrences of a string in file contents, file names, and directory names."
    )
    parser.add_argument("path", help="Path to file or directory to process")
    parser.add_argument("search_string", help="String to search for")
    parser.add_argument("replace_string", help="String to replace with")
    parser.add_argument("-y", "--yes", action="store_true", 
                       help="Skip confirmation prompt")
    
    args = parser.parse_args()
    
    # Show what will be done
    print(f"String Replacer")
    print(f"===============")
    print(f"Path: {args.path}")
    print(f"Search for: '{args.search_string}'")
    print(f"Replace with: '{args.replace_string}'")
    print()
    
    # Confirmation
    if not args.yes:
        response = input("This will modify files and rename files/directories. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
    
    print("\nProcessing...")
    try:
        process_directory(args.path, args.search_string, args.replace_string)
        print("\nOperation completed successfully!")
    except Exception as e:
        print(f"\nError during processing: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

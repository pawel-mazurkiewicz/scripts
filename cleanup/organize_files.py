#!/usr/bin/env python3
"""
File Organizer Script
Organizes files in a specified folder into subfolders based on file types.

Usage: python organize_files.py <folder_path>
Example: python organize_files.py /Users/username/Downloads
"""

import os
import sys
import shutil
from pathlib import Path
from collections import defaultdict

# File type mappings - define which extensions go to which folders
FILE_TYPE_MAPPINGS = {
    'Images': {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', 
        '.webp', '.svg', '.ico', '.heic', '.heif', '.raw', '.cr2', 
        '.nef', '.orf', '.sr2', '.dng'
    },
    'Documents': {
        '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages', 
        '.tex', '.md', '.html', '.htm', '.xml', '.epub', '.mobi'
    },
    'Spreadsheets': {
        '.xls', '.xlsx', '.csv', '.ods', '.numbers', '.tsv'
    },
    'Presentations': {
        '.ppt', '.pptx', '.odp', '.key'
    },
    'Videos': {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
        '.m4v', '.3gp', '.ogv', '.mpg', '.mpeg', '.m2v'
    },
    'Audio': {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', 
        '.opus', '.mid', '.midi', '.xm', '.mod', '.s3m', '.it',
        '.vitalbank', '.ableton', '.logic'
    },
    'Archives': {
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tar.gz', 
        '.tar.bz2', '.tar.xz', '.dmg', '.iso', '.img', '.sit', '.sitx',
        '.exe', '.msi', '.deb', '.rpm', '.appimage', '.pkg', '.torrent',
        '.xpi'
    },
    'Games': {
        '.gba', '.gb', '.gbc', '.nes', '.snes', '.sfc', '.n64', '.z64',
        '.md', '.smd', '.gg', '.sms', '.pce', '.ngp', '.ws', '.wsc',
        '.rom', '.iso', '.cue', '.bin', '.img', '.nds', '.3ds', '.cia',
        '.srm', '.sav', '.ips', '.ups', '.bps', '.psu', '.mcr', '.vmc'
    },
    'Code': {
        '.py', '.js', '.html', '.css', '.json', '.xml', '.yaml', '.yml',
        '.sh', '.bat', '.ps1', '.php', '.rb', '.go', '.rust', '.c', '.cpp',
        '.h', '.hpp', '.java', '.kt', '.swift', '.r', '.sql', '.cfg', '.conf',
        '.ini', '.toml', '.env', '.dockerfile', '.makefile', '.cmake',
        '.gitignore', '.gitattributes', '.editorconfig', '.eslintrc',
        '.prettierrc', '.babelrc', '.vscode', '.idea', '.lic', '.license',
        '.rdp', '.ovpn', '.pem', '.key', '.crt', '.p12', '.pfx', '.jks',
        '.tfstate', '.tf', '.hcl', '.ics'
    },
    'Fonts': {
        '.ttf', '.otf', '.woff', '.woff2', '.eot'
    }
}

# System files and directories to skip
SKIP_FILES = {
    '.ds_store', '.localized', 'desktop.ini', 'thumbs.db', '.directory',
    '$recycle.bin', 'system volume information', '.spotlight-v100',
    '.trashes', '.fseventsd', '.temporaryitems'
}

def get_file_category(file_path):
    """Determine which category a file belongs to based on its extension."""
    extension = file_path.suffix.lower()
    
    # Handle special cases like .tar.gz
    if file_path.name.lower().endswith(('.tar.gz', '.tar.bz2', '.tar.xz')):
        return 'Archives'
    
    for category, extensions in FILE_TYPE_MAPPINGS.items():
        if extension in extensions:
            return category
    
    return None

def should_skip_file(file_path):
    """Check if a file should be skipped (system files, etc.)."""
    file_name = file_path.name.lower()
    return (
        file_name in SKIP_FILES or
        file_name.startswith('.') and len(file_name) > 1 or
        file_path.is_dir()
    )

def create_category_folders(base_path, categories):
    """Create category folders if they don't exist."""
    created_folders = []
    for category in categories:
        folder_path = base_path / category
        if not folder_path.exists():
            try:
                folder_path.mkdir(exist_ok=True)
                created_folders.append(category)
                print(f"✅ Created folder: {category}")
            except OSError as e:
                print(f"❌ Error creating folder {category}: {e}")
                return False
    return True

def move_file_safely(source, destination):
    """Move a file safely, handling naming conflicts."""
    if destination.exists():
        # If destination exists, add a number suffix
        counter = 1
        name_without_ext = destination.stem
        extension = destination.suffix
        
        while destination.exists():
            new_name = f"{name_without_ext}_{counter}{extension}"
            destination = destination.parent / new_name
            counter += 1
    
    try:
        shutil.move(str(source), str(destination))
        return True, destination
    except (OSError, shutil.Error) as e:
        print(f"❌ Error moving {source.name}: {e}")
        return False, None

def organize_folder(folder_path):
    """Main function to organize files in the specified folder."""
    folder_path = Path(folder_path).resolve()
    
    if not folder_path.exists():
        print(f"❌ Error: Folder '{folder_path}' does not exist.")
        return False
    
    if not folder_path.is_dir():
        print(f"❌ Error: '{folder_path}' is not a directory.")
        return False
    
    print(f"🔍 Scanning folder: {folder_path}")
    
    # Collect files to organize
    files_to_organize = defaultdict(list)
    skipped_files = []
    
    for item in folder_path.iterdir():
        if item.is_file():
            if should_skip_file(item):
                skipped_files.append(item.name)
                continue
            
            category = get_file_category(item)
            if category:
                files_to_organize[category].append(item)
            else:
                print(f"⚠️  Unknown file type: {item.name}")
    
    if not files_to_organize:
        print("ℹ️  No files found to organize.")
        return True
    
    # Display summary
    print(f"\n📊 Found {sum(len(files) for files in files_to_organize.values())} files to organize:")
    for category, files in files_to_organize.items():
        print(f"   📁 {category}: {len(files)} files")
    
    if skipped_files:
        print(f"⏭️  Skipped {len(skipped_files)} system/hidden files")
    
    # Ask for confirmation
    response = input("\n❓ Proceed with organization? (y/N): ").strip().lower()
    if response != 'y':
        print("🚫 Organization cancelled.")
        return False
    
    # Create category folders
    categories_needed = set(files_to_organize.keys())
    if not create_category_folders(folder_path, categories_needed):
        return False
    
    # Move files
    moved_count = 0
    failed_count = 0
    
    print("\n🔄 Moving files...")
    for category, files in files_to_organize.items():
        category_folder = folder_path / category
        
        for file_path in files:
            destination = category_folder / file_path.name
            success, final_destination = move_file_safely(file_path, destination)
            
            if success:
                moved_count += 1
                print(f"   ✅ {file_path.name} → {category}/")
            else:
                failed_count += 1
    
    # Summary
    print(f"\n🎉 Organization complete!")
    print(f"   ✅ Successfully moved: {moved_count} files")
    if failed_count > 0:
        print(f"   ❌ Failed to move: {failed_count} files")
    
    return True

def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python organize_files.py <folder_path>")
        print("Example: python organize_files.py /Users/username/Downloads")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    print("📂 File Organizer")
    print("=" * 50)
    
    success = organize_folder(folder_path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

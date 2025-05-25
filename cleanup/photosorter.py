#!/usr/bin/env python3
"""
Photo Organizer Script
Sorts photos into YEAR/MONTH/DAY folder structure based on EXIF date or file modification date.
Supports RAF and JPG formats.
"""

import os
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import exifread

def get_exif_date(file_path):
    """
    Extract date from EXIF data. Tries multiple methods for robustness.
    Returns datetime object or None if no date found.
    """
    try:
        # Method 1: Using PIL (works well for JPG)
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "DateTimeOriginal":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    elif tag == "DateTime":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    
    try:
        # Method 2: Using exifread (better for RAF and other formats)
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, stop_tag='DateTimeOriginal')
            
            # Try DateTimeOriginal first (when photo was taken)
            if 'EXIF DateTimeOriginal' in tags:
                date_str = str(tags['EXIF DateTimeOriginal'])
                return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            
            # Fallback to DateTime
            elif 'Image DateTime' in tags:
                date_str = str(tags['Image DateTime'])
                return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    
    return None

def get_file_date(file_path):
    """
    Get date from file system (modification date).
    Returns datetime object.
    """
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)

def get_photo_date(file_path):
    """
    Get the best available date for a photo file.
    Tries EXIF first, falls back to modification date.
    """
    # Try EXIF data first
    exif_date = get_exif_date(file_path)
    if exif_date:
        return exif_date, "EXIF"
    
    # Fallback to file modification date
    file_date = get_file_date(file_path)
    return file_date, "File Modified"

def create_date_path(base_dir, date_obj):
    """
    Create directory path in YEAR/MONTH/DAY format.
    """
    year = date_obj.strftime("%Y")
    month = date_obj.strftime("%m")
    day = date_obj.strftime("%d")
    
    date_path = Path(base_dir) / year / month / day
    date_path.mkdir(parents=True, exist_ok=True)
    
    return date_path

def is_supported_format(file_path):
    """
    Check if file is a supported image format (RAF or JPG).
    """
    supported_extensions = {'.jpg', '.jpeg', '.raf', '.JPG', '.JPEG', '.RAF'}
    return Path(file_path).suffix in supported_extensions

def organize_photos(source_dir, destination_dir, copy_files=False, dry_run=False):
    """
    Organize photos from source directory into destination directory.
    
    Args:
        source_dir: Directory containing photos to organize
        destination_dir: Directory where organized photos will be placed
        copy_files: If True, copy files instead of moving them
        dry_run: If True, show what would be done without actually doing it
    """
    source_path = Path(source_dir)
    dest_path = Path(destination_dir)
    
    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return
    
    # Create destination directory if it doesn't exist
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Statistics
    stats = {
        'total_files': 0,
        'processed': 0,
        'skipped': 0,
        'exif_used': 0,
        'file_date_used': 0,
        'errors': 0
    }
    
    print(f"{'DRY RUN: ' if dry_run else ''}Organizing photos...")
    print(f"Source: {source_dir}")
    print(f"Destination: {destination_dir}")
    print(f"Operation: {'Copy' if copy_files else 'Move'}")
    print("-" * 50)
    
    # Process all files in source directory (including subdirectories)
    for file_path in source_path.rglob('*'):
        if file_path.is_file():
            stats['total_files'] += 1
            
            # Check if it's a supported image format
            if not is_supported_format(file_path):
                continue
            
            try:
                # Get the photo date
                photo_date, date_source = get_photo_date(file_path)
                
                # Update statistics
                if date_source == "EXIF":
                    stats['exif_used'] += 1
                else:
                    stats['file_date_used'] += 1
                
                # Create destination path
                date_folder = create_date_path(dest_path, photo_date)
                dest_file_path = date_folder / file_path.name
                
                # Handle file name conflicts
                counter = 1
                original_name = file_path.stem
                extension = file_path.suffix
                while dest_file_path.exists():
                    new_name = f"{original_name}_{counter}{extension}"
                    dest_file_path = date_folder / new_name
                    counter += 1
                
                # Show what we're doing
                operation = "COPY" if copy_files else "MOVE"
                print(f"[{operation}] {file_path.name} -> {date_folder.relative_to(dest_path)} ({date_source})")
                
                # Perform the operation (unless dry run)
                if not dry_run:
                    if copy_files:
                        shutil.copy2(file_path, dest_file_path)
                    else:
                        shutil.move(str(file_path), str(dest_file_path))
                
                stats['processed'] += 1
                
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")
                stats['errors'] += 1
    
    # Print statistics
    print("-" * 50)
    print("SUMMARY:")
    print(f"Total files found: {stats['total_files']}")
    print(f"Photos processed: {stats['processed']}")
    print(f"Files skipped (unsupported): {stats['total_files'] - stats['processed'] - stats['errors']}")
    print(f"Errors: {stats['errors']}")
    print(f"Used EXIF date: {stats['exif_used']}")
    print(f"Used file modified date: {stats['file_date_used']}")

def main():
    parser = argparse.ArgumentParser(description="Organize photos into YEAR/MONTH/DAY folder structure")
    parser.add_argument("source", help="Source directory containing photos")
    parser.add_argument("destination", help="Destination directory for organized photos")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of moving them")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without actually doing it")
    
    args = parser.parse_args()
    
    organize_photos(args.source, args.destination, args.copy, args.dry_run)

if __name__ == "__main__":
    main()

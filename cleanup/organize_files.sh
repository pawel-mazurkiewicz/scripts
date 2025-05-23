#!/bin/bash

# File Organizer Script (Bash Version)
# Organizes files in a specified folder into subfolders based on file types.
# 
# Usage: ./organize_files.sh <folder_path>
# Example: ./organize_files.sh /Users/username/Downloads

set -euo pipefail

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# File type associations (extension:folder)
declare -A FILE_TYPES=(
    # Images
    ["jpg"]="Images" ["jpeg"]="Images" ["png"]="Images" ["gif"]="Images"
    ["bmp"]="Images" ["tiff"]="Images" ["tif"]="Images" ["webp"]="Images"
    ["svg"]="Images" ["ico"]="Images" ["heic"]="Images" ["heif"]="Images"
    
    # Documents
    ["pdf"]="Documents" ["doc"]="Documents" ["docx"]="Documents" ["txt"]="Documents"
    ["rtf"]="Documents" ["odt"]="Documents" ["pages"]="Documents" ["tex"]="Documents"
    ["md"]="Documents" ["html"]="Documents" ["htm"]="Documents" ["xml"]="Documents"
    ["epub"]="Documents" ["mobi"]="Documents"
    
    # Spreadsheets
    ["xls"]="Spreadsheets" ["xlsx"]="Spreadsheets" ["csv"]="Spreadsheets"
    ["ods"]="Spreadsheets" ["numbers"]="Spreadsheets" ["tsv"]="Spreadsheets"
    
    # Presentations
    ["ppt"]="Presentations" ["pptx"]="Presentations" ["odp"]="Presentations"
    ["key"]="Presentations"
    
    # Videos
    ["mp4"]="Videos" ["avi"]="Videos" ["mkv"]="Videos" ["mov"]="Videos"
    ["wmv"]="Videos" ["flv"]="Videos" ["webm"]="Videos" ["m4v"]="Videos"
    ["3gp"]="Videos" ["ogv"]="Videos" ["mpg"]="Videos" ["mpeg"]="Videos"
    
    # Audio
    ["mp3"]="Audio" ["wav"]="Audio" ["flac"]="Audio" ["aac"]="Audio"
    ["ogg"]="Audio" ["wma"]="Audio" ["m4a"]="Audio" ["opus"]="Audio"
    ["mid"]="Audio" ["midi"]="Audio" ["xm"]="Audio" ["mod"]="Audio"
    ["vitalbank"]="Audio"
    
    # Archives
    ["zip"]="Archives" ["rar"]="Archives" ["7z"]="Archives" ["tar"]="Archives"
    ["gz"]="Archives" ["bz2"]="Archives" ["xz"]="Archives" ["dmg"]="Archives"
    ["iso"]="Archives" ["img"]="Archives" ["sit"]="Archives" ["sitx"]="Archives"
    ["exe"]="Archives" ["msi"]="Archives" ["deb"]="Archives" ["rpm"]="Archives"
    ["appimage"]="Archives" ["pkg"]="Archives" ["torrent"]="Archives" ["xpi"]="Archives"
    
    # Games
    ["gba"]="Games" ["gb"]="Games" ["gbc"]="Games" ["nes"]="Games"
    ["snes"]="Games" ["sfc"]="Games" ["n64"]="Games" ["z64"]="Games"
    ["md"]="Games" ["smd"]="Games" ["gg"]="Games" ["sms"]="Games"
    ["rom"]="Games" ["srm"]="Games" ["sav"]="Games" ["ips"]="Games"
    ["ups"]="Games" ["bps"]="Games" ["psu"]="Games"
    
    # Code
    ["py"]="Code" ["js"]="Code" ["css"]="Code" ["json"]="Code"
    ["yaml"]="Code" ["yml"]="Code" ["sh"]="Code" ["bat"]="Code"
    ["ps1"]="Code" ["php"]="Code" ["rb"]="Code" ["go"]="Code"
    ["c"]="Code" ["cpp"]="Code" ["h"]="Code" ["hpp"]="Code"
    ["java"]="Code" ["kt"]="Code" ["swift"]="Code" ["sql"]="Code"
    ["cfg"]="Code" ["conf"]="Code" ["ini"]="Code" ["toml"]="Code"
    ["env"]="Code" ["lic"]="Code" ["license"]="Code" ["rdp"]="Code"
    ["ovpn"]="Code" ["pem"]="Code" ["key"]="Code" ["crt"]="Code"
    ["pfx"]="Code" ["jks"]="Code" ["tfstate"]="Code" ["tf"]="Code"
    ["ics"]="Code"
    
    # Fonts
    ["ttf"]="Fonts" ["otf"]="Fonts" ["woff"]="Fonts" ["woff2"]="Fonts"
)

# Files to skip (system files, hidden files, etc.)
SKIP_FILES=(".ds_store" ".localized" "desktop.ini" "thumbs.db" ".directory")

# Function to check if a file should be skipped
should_skip_file() {
    local filename=$(basename "$1" | tr '[:upper:]' '[:lower:]')
    
    # Skip hidden files (starting with .)
    if [[ "$filename" == .* ]]; then
        return 0
    fi
    
    # Skip specific system files
    for skip_file in "${SKIP_FILES[@]}"; do
        if [[ "$filename" == "$skip_file" ]]; then
            return 0
        fi
    done
    
    return 1
}

# Function to get file extension
get_extension() {
    local filename=$(basename "$1")
    local extension="${filename##*.}"
    echo "${extension,,}" # Convert to lowercase
}

# Function to get category for a file
get_category() {
    local file="$1"
    local extension=$(get_extension "$file")
    
    # Handle special cases like .tar.gz
    if [[ "$file" == *.tar.gz ]] || [[ "$file" == *.tar.bz2 ]] || [[ "$file" == *.tar.xz ]]; then
        echo "Archives"
        return
    fi
    
    echo "${FILE_TYPES[$extension]:-}"
}

# Function to create directories safely
create_directory() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        if mkdir -p "$dir" 2>/dev/null; then
            print_message "$GREEN" "✅ Created folder: $(basename "$dir")"
            return 0
        else
            print_message "$RED" "❌ Error creating folder: $(basename "$dir")"
            return 1
        fi
    fi
    return 0
}

# Function to move file safely (handle naming conflicts)
move_file_safely() {
    local source="$1"
    local destination="$2"
    local filename=$(basename "$source")
    local counter=1
    
    # If destination exists, add number suffix
    while [[ -e "$destination" ]]; do
        local name_without_ext="${filename%.*}"
        local extension="${filename##*.}"
        if [[ "$name_without_ext" == "$extension" ]]; then
            # No extension
            destination="$(dirname "$destination")/${filename}_${counter}"
        else
            destination="$(dirname "$destination")/${name_without_ext}_${counter}.${extension}"
        fi
        ((counter++))
    done
    
    if mv "$source" "$destination" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Main organization function
organize_folder() {
    local folder_path="$1"
    
    # Validate folder path
    if [[ ! -d "$folder_path" ]]; then
        print_message "$RED" "❌ Error: Folder '$folder_path' does not exist or is not a directory."
        return 1
    fi
    
    print_message "$BLUE" "🔍 Scanning folder: $folder_path"
    
    # Arrays to store files by category
    declare -A files_by_category
    declare -a unknown_files
    declare -a skipped_files
    
    # Scan files
    while IFS= read -r -d '' file; do
        if [[ -f "$file" ]]; then
            if should_skip_file "$file"; then
                skipped_files+=("$(basename "$file")")
                continue
            fi
            
            local category=$(get_category "$file")
            if [[ -n "$category" ]]; then
                files_by_category["$category"]+="$file"$'\n'
            else
                unknown_files+=("$(basename "$file")")
            fi
        fi
    done < <(find "$folder_path" -maxdepth 1 -type f -print0)
    
    # Count files
    local total_files=0
    for category in "${!files_by_category[@]}"; do
        local count=$(echo -n "${files_by_category[$category]}" | grep -c '^' 2>/dev/null || echo 0)
        ((total_files += count))
        print_message "$BLUE" "   📁 $category: $count files"
    done
    
    if [[ $total_files -eq 0 ]]; then
        print_message "$YELLOW" "ℹ️  No files found to organize."
        return 0
    fi
    
    if [[ ${#unknown_files[@]} -gt 0 ]]; then
        print_message "$YELLOW" "⚠️  Unknown file types:"
        for file in "${unknown_files[@]}"; do
            print_message "$YELLOW" "   - $file"
        done
    fi
    
    if [[ ${#skipped_files[@]} -gt 0 ]]; then
        print_message "$YELLOW" "⏭️  Skipped ${#skipped_files[@]} system/hidden files"
    fi
    
    # Ask for confirmation
    echo
    read -p "❓ Proceed with organization? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_message "$YELLOW" "🚫 Organization cancelled."
        return 0
    fi
    
    # Create category folders
    for category in "${!files_by_category[@]}"; do
        if ! create_directory "$folder_path/$category"; then
            return 1
        fi
    done
    
    # Move files
    local moved_count=0
    local failed_count=0
    
    print_message "$BLUE" "🔄 Moving files..."
    
    for category in "${!files_by_category[@]}"; do
        while IFS= read -r file; do
            [[ -z "$file" ]] && continue
            
            local destination="$folder_path/$category/$(basename "$file")"
            
            if move_file_safely "$file" "$destination"; then
                ((moved_count++))
                print_message "$GREEN" "   ✅ $(basename "$file") → $category/"
            else
                ((failed_count++))
                print_message "$RED" "   ❌ Failed to move $(basename "$file")"
            fi
        done <<< "${files_by_category[$category]}"
    done
    
    # Summary
    echo
    print_message "$GREEN" "🎉 Organization complete!"
    print_message "$GREEN" "   ✅ Successfully moved: $moved_count files"
    if [[ $failed_count -gt 0 ]]; then
        print_message "$RED" "   ❌ Failed to move: $failed_count files"
    fi
    
    return 0
}

# Main script
main() {
    if [[ $# -ne 1 ]]; then
        echo "Usage: $0 <folder_path>"
        echo "Example: $0 /Users/username/Downloads"
        exit 1
    fi
    
    local folder_path="$1"
    
    print_message "$BLUE" "📂 File Organizer (Bash Version)"
    print_message "$BLUE" "$(printf '=%.0s' {1..50})"
    
    if organize_folder "$folder_path"; then
        exit 0
    else
        exit 1
    fi
}

# Run main function with all arguments
main "$@"

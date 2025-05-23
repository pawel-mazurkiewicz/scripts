# File Organizer Scripts

Two scripts to automatically organize files in any folder by sorting them into subfolders based on file types.

## 📁 What Gets Organized

Files are sorted into these categories:

- **📸 Images**: JPG, PNG, GIF, HEIC, SVG, etc.
- **📄 Documents**: PDF, DOC, TXT, HTML, MD, etc.
- **📊 Spreadsheets**: XLS, XLSX, CSV, etc.
- **🎬 Videos**: MP4, AVI, MKV, MOV, etc.
- **🎵 Audio**: MP3, WAV, FLAC, MIDI, etc.
- **📦 Archives**: ZIP, RAR, DMG, EXE, etc.
- **🎮 Games**: ROM files, save files, patches
- **💻 Code**: Programming files, configs, certificates
- **🔤 Fonts**: TTF, OTF, WOFF, etc.

## 🐍 Python Version (`organize_files.py`)

### Features:
- Cross-platform (Windows, macOS, Linux)
- Robust error handling
- Handles file naming conflicts automatically
- Detailed progress reporting
- Confirmation before organizing

### Usage:
```bash
python organize_files.py <folder_path>
```

### Examples:
```bash
# Organize Downloads folder
python organize_files.py /Users/username/Downloads

# Organize a project folder
python organize_files.py /path/to/messy/folder

# On Windows
python organize_files.py "C:\Users\username\Downloads"
```

### Requirements:
- Python 3.6+
- No additional packages needed (uses only standard library)

## 🐚 Bash Version (`organize_files.sh`)

### Features:
- Fast and lightweight
- Colored output for better readability
- Works on macOS and Linux
- No dependencies except bash

### Usage:
```bash
# Make executable (first time only)
chmod +x organize_files.sh

# Run the script
./organize_files.sh <folder_path>
```

### Examples:
```bash
# Organize Downloads folder
./organize_files.sh /Users/username/Downloads

# Organize any folder
./organize_files.sh /path/to/messy/folder
```

### Requirements:
- Bash 4.0+
- macOS or Linux

## 🛡️ Safety Features

Both scripts include these safety features:

1. **Confirmation Required**: Scripts ask for confirmation before moving files
2. **Naming Conflicts**: Automatically handle duplicate filenames by adding numbers
3. **System Files Protected**: Skip system files like `.DS_Store`, `desktop.ini`
4. **Existing Folders**: Don't disturb existing directories
5. **Error Handling**: Graceful error handling with informative messages

## 📋 Example Output

```
📂 File Organizer
==================================================
🔍 Scanning folder: /Users/username/Downloads

📊 Found 45 files to organize:
   📁 Images: 12 files
   📁 Documents: 8 files
   📁 Archives: 15 files
   📁 Videos: 3 files
   📁 Audio: 7 files

⏭️  Skipped 3 system/hidden files

❓ Proceed with organization? (y/N): y

✅ Created folder: Images
✅ Created folder: Documents
✅ Created folder: Archives

🔄 Moving files...
   ✅ photo1.jpg → Images/
   ✅ document.pdf → Documents/
   ✅ archive.zip → Archives/
   ...

🎉 Organization complete!
   ✅ Successfully moved: 45 files
```

## 🔧 Customization

To add new file types or modify categories:

### Python Version:
Edit the `FILE_TYPE_MAPPINGS` dictionary in `organize_files.py`

### Bash Version:
Edit the `FILE_TYPES` associative array in `organize_files.sh`

## ⚠️ Important Notes

- **Backup First**: Always backup important data before running
- **Test Run**: Try on a test folder first to see how it works
- **Hidden Files**: System files and hidden files are automatically skipped
- **Permissions**: Ensure you have write permissions for the target folder

## 🚀 Quick Start

1. **Download** either script to your system
2. **Navigate** to the folder containing the script
3. **Run** with your target folder path:
   ```bash
   python organize_files.py /path/to/folder
   # or
   ./organize_files.sh /path/to/folder
   ```
4. **Confirm** when prompted
5. **Enjoy** your organized folder! 🎉



# Utility Scripts Collection

This repository contains a collection of utility scripts for various tasks, including file organization and image conversion.

## File Cleanup Utilities (`cleanup/`)

This section includes scripts designed to help organize and manage files.

- **`organize_files.py`**: A Python script that sorts files into subfolders based on their type (e.g., images, documents, videos).
- **`organize_files.sh`**: A Bash script providing similar file organization capabilities for macOS and Linux systems.

For more detailed information on these scripts, please see the [cleanup/README.md](cleanup/README.md).

## Image and Data Conversion Utilities (`imageconvert/`)

This section provides scripts for various image and data format conversions.

- **`csv-to-ics.py`**: Converts event data from a CSV file to an ICS calendar file.
  - *Usage*: `python imageconvert/csv-to-ics.py <input.csv>`
- **`icns-to-pngs.py`**: Extracts all image sizes from a macOS `.icns` icon file and saves them as individual PNG files.
  - *Usage*: `python imageconvert/icns-to-pngs.py <icon_file.icns>`
- **`svg-to-png.py`**: Converts an SVG (Scalable Vector Graphics) image file to a PNG (Portable Network Graphics) file.
  - *Usage*: `python imageconvert/svg-to-png.py <input.svg> <output.png> [width] [height]`
    - `width` and `height` are optional arguments to specify the dimensions of the output PNG.

## Usage

### Python Scripts

To run the Python scripts (`.py`), you generally need Python 3 installed. You can execute them using the following command structure:

```bash
python <path_to_script>.py [arguments...]
```

For example:
```bash
python imageconvert/svg-to-png.py assets/my_icon.svg output/my_icon.png 128 128
```

Make sure to replace `<path_to_script>.py` with the actual path to the script and `[arguments...]` with any required arguments for the specific script.

### Bash Scripts

To run the Bash scripts (`.sh`), you'll typically use a terminal on a macOS or Linux system.

1.  **Make the script executable** (you only need to do this once):
    ```bash
    chmod +x <path_to_script>.sh
    ```
2.  **Run the script**:
    ```bash
    ./<path_to_script>.sh [arguments...]
    ```

For example:
```bash
chmod +x cleanup/organize_files.sh
./cleanup/organize_files.sh /Users/yourname/Downloads
```

Replace `<path_to_script>.sh` with the actual path to the script and `[arguments...]` with any required arguments.

## Contributing

Contributions to this collection of utility scripts are welcome! If you have an idea for a new script, an improvement to an existing one, or have found a bug, please feel free to:

1.  **Report an Issue**: Open an issue in the repository to discuss the problem or suggestion.
2.  **Submit a Pull Request**: Fork the repository, make your changes, and submit a pull request with a clear description of your modifications.

Please ensure that any new scripts are well-documented and, if applicable, include usage examples.


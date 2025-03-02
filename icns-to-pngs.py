#!/usr/bin/env python3
from PIL import Image
import sys

def export_icns_to_png(icns_file):
    try:
        im = Image.open(icns_file)
    except Exception as e:
        print(f"Error opening {icns_file}: {e}")
        return

    if im.format.lower() != "icns":
        print("Warning: The file does not appear to be in ICNS format.")

    sizes = im.info.get("sizes")
    if sizes:
        print("Found icon sizes:", sizes)
    else:
        print("No size info found in the ICNS file.")

    # Save largest size
    output_filename = "icon_largest.png"
    im.save(output_filename, format="PNG")
    print(f"Exported largest icon: {output_filename}")

    for size in sizes or []:
        # Make sure size contains only length and width
        target_size = size if len(size) == 2 else size[:2]
        if im.size == target_size:
            continue
        scaled_img = im.resize(target_size, Image.LANCZOS)
        output_filename = f"icon_{target_size[0]}x{target_size[1]}.png"
        scaled_img.save(output_filename, format="PNG")
        print(f"Exported resized icon: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_icns.py <icon_file.icns>")
        sys.exit(1)
    
    icns_path = sys.argv[1]
    export_icns_to_png(icns_path)
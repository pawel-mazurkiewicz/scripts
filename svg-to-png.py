#!/usr/bin/env python3
import sys
import cairosvg

def convert_svg_to_png(input_file: str, output_file: str, width: int = None, height: int = None) -> None:
    """
    Converts an SVG file to a PNG file.
    
    Parameters:
    - input_file: Path to the input SVG file.
    - output_file: Path where the output PNG file will be saved.
    - width: Optional; desired width in pixels for the output PNG.
    - height: Optional; desired height in pixels for the output PNG.
    """
    try:
        with open(input_file, "rb") as svg_file:
            cairosvg.svg2png(file_obj=svg_file, write_to=output_file,
                              output_width=width, output_height=height)
        print(f"Conversion successful! PNG saved to {output_file}")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    # Command-line usage:
    # python svg-to-png.py <input.svg> <output.png> [<width> <height>]
    if len(sys.argv) not in [3, 5]:
        print("Usage: python svg-to-png.py <input.svg> <output.png> [<width> <height>]")
    else:
        input_svg = sys.argv[1]
        output_png = sys.argv[2]
        if len(sys.argv) == 5:
            try:
                width = int(sys.argv[3])
                height = int(sys.argv[4])
            except ValueError:
                print("Width and height must be integers.")
                sys.exit(1)
            convert_svg_to_png(input_svg, output_png, width, height)
        else:
            convert_svg_to_png(input_svg, output_png)
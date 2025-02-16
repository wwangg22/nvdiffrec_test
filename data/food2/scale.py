#!/usr/bin/env python3

import os
import sys
from PIL import Image

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    # Desired resolution: 540×960
    target_width  = 960
    target_height = 540

    # Create output folder if necessary
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        # Construct full path to the file
        input_path = os.path.join(input_folder, filename)

        # Check if it's actually a file (not a subfolder) and skip if not an image
        if not os.path.isfile(input_path):
            continue

        # Attempt to open as an image
        try:
            with Image.open(input_path) as img:
                # Optionally check size or skip if the image isn't 1920×1080
                # if img.size != (1920, 1080):
                #     print(f"Skipping '{filename}', not exactly 1920x1080.")
                #     continue

                # Resize using a high-quality downsampling filter
                img_resized = img.resize((target_width, target_height), Image.LANCZOS)

                # Construct output path
                output_path = os.path.join(output_folder, filename)

                # Save with the same filename
                img_resized.save(output_path)
                print(f"Scaled '{filename}' -> [{target_height}×{target_width}], saved to '{output_path}'")
        except Exception as e:
            print(f"Skipping file '{filename}', not a valid image or error reading file ({e}).")

if __name__ == "__main__":
    main()

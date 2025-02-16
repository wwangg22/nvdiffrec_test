#!/usr/bin/env python3

import os
from PIL import Image

def resize_images(input_folder='./lego/test', output_folder='./lego/test_resized', size=(512, 512)):
    """
    Resizes all PNG images in the input folder to the specified size
    and saves them into the output folder.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is a PNG (by extension)
        if filename.lower().endswith('.png'):
            # Construct full file path
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # Open the image using Pillow
            with Image.open(input_path) as img:
                print(f"Resizing {filename} to {size[0]}x{size[1]}...")
                # Resize the image
                resized_img = img.resize(size, Image.Resampling.LANCZOS)
                 # Save the resized image in the output folder
                resized_img.save(output_path)

    print(f"\nAll images have been resized to {size[0]}x{size[1]} "
          f"and saved in the '{output_folder}' folder.")

if __name__ == '__main__':
    # By default, it looks for PNG files in the current directory
    # and saves them into the 'resized' directory as 512x512.
    resize_images()

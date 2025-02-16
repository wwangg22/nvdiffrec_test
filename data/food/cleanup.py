#!/usr/bin/env python3

import os
import json
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Remove frames from the JSON if their corresponding image file no longer exists."
    )
    parser.add_argument("--input_json",  type=str, required=True, help="Path to the original JSON file.")
    parser.add_argument("--output_json", type=str, required=True, help="Where to write the cleaned JSON.")
    parser.add_argument("--folder",      type=str, required=True, help="Folder where images reside.")

    args = parser.parse_args()

    # 1) Load the JSON data
    with open(args.input_json, "r") as f:
        data = json.load(f)

    frames = data.get("frames", [])
    print(f"Original frames count: {len(frames)}")

    # 2) Collect only frames that still exist on disk
    cleaned_frames = []
    for frame in frames:
        # Example: frame["file_path"] = "./train/0007" (no extension or maybe .png)
        file_path = frame.get("file_path", "")
        folder_part, filename = os.path.split(file_path)  # e.g. "./train", "0007" or "0007.png"

        name, ext = os.path.splitext(filename)
        if not ext:  # If the JSON path has no extension, assume .png
            ext = ".png"
        full_path = os.path.join(args.folder, folder_part, name + ext)

        # Normalize the path (remove any "./" duplication, etc.)
        full_path = os.path.normpath(full_path)

        if os.path.exists(full_path):
            cleaned_frames.append(frame)
        else:
            print(f"Frame removed - missing file: '{full_path}'")

    data["frames"] = cleaned_frames
    print(f"Cleaned frames count: {len(cleaned_frames)}")

    # 3) Save out the updated JSON
    with open(args.output_json, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved cleaned JSON to '{args.output_json}'.")

if __name__ == "__main__":
    main()

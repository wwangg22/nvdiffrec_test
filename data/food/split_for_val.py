#!/usr/bin/env python3

import os
import json
import shutil
import random
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Split a subset of frames from transforms.json into a validation set, "
                    "move images, write transforms_val.json, and update the original transforms."
    )
    parser.add_argument("--input_json",     type=str, required=True,
                        help="Path to the original transforms JSON (WILL be overwritten).")
    parser.add_argument("--output_json",    type=str, required=True,
                        help="Where to write the new validation JSON (transforms_val.json).")
    parser.add_argument("--val_folder",     type=str, default="./val",
                        help="Folder to move validation images into (must exist or be creatable).")
    parser.add_argument("--num_val_frames", type=int, default=10,
                        help="How many images to move to validation set.")
    parser.add_argument("--seed",           type=int, default=0,
                        help="Random seed for reproducibility.")

    args = parser.parse_args()

    # 1) Read original transforms
    with open(args.input_json, "r") as f:
        data = json.load(f)

    all_frames = data.get("frames", [])
    total_frames = len(all_frames)
    if total_frames == 0:
        print("No frames found in the input JSON. Exiting.")
        return

    # 2) Pick random frames for validation
    random.seed(args.seed)
    if args.num_val_frames > total_frames:
        print(f"Requested {args.num_val_frames} val frames, but only {total_frames} exist.")
        return
    val_indices = set(random.sample(range(total_frames), args.num_val_frames))

    # 3) Partition frames into 'val_frames' and 'train_frames'
    val_frames = []
    train_frames = []
    for i, frame in enumerate(all_frames):
        if i in val_indices:
            val_frames.append(frame)
        else:
            train_frames.append(frame)

    os.makedirs(args.val_folder, exist_ok=True)

    # 4) Move each chosen val file into val folder, adjusting the file_path
    for frame in val_frames:
        old_path = frame["file_path"]  # e.g. "./train/0002" or "./train/0002.png"

        # We'll guess there's a .png extension on disk if no extension is present
        folder_part, filename = os.path.split(old_path)
        name, ext = os.path.splitext(filename)
        if ext == "":
            ext = ".png"  # assume .png if missing

        # The file on disk
        full_old_path = os.path.join(folder_part, name + ext)

        # Build new disk path and new JSON path (force forward slash)
        new_disk_path = os.path.join(args.val_folder, name + ext)           # For the actual file move
        new_json_path = f"./val/{name}"  # or f"./val/{name}{ext}" if you want the .png in the JSON

        # Physically move the file
        if not os.path.exists(full_old_path):
            print(f"Warning: image file '{full_old_path}' does not exist!")
        else:
            shutil.move(full_old_path, new_disk_path)
            print(f"Moved '{full_old_path}' -> '{new_disk_path}'")

        # Update the frame path in the val set
        frame["file_path"] = new_json_path

    # 5) Create new JSON data for val
    val_data = {}
    for k, v in data.items():
        if k != "frames":
            val_data[k] = v
    val_data["frames"] = val_frames

    # 6) Overwrite the original JSON with only the remaining train frames
    data["frames"] = train_frames
    with open(args.input_json, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Overwrote '{args.input_json}' to keep {len(train_frames)} train frames.")

    # 7) Write out transforms_val.json
    with open(args.output_json, "w") as f:
        json.dump(val_data, f, indent=2)
    print(f"Wrote '{args.output_json}' with {len(val_frames)} validation frames.")


if __name__ == "__main__":
    main()

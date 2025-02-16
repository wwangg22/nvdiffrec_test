#!/usr/bin/env python3

import os
import json
import shutil
import random
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Split a subset of frames from transforms.json into a test set, "
                    "move images, write transforms_test.json, and update the original transforms."
    )
    parser.add_argument("--input_json",     type=str, required=True,
                        help="Path to the original transforms JSON (WILL be overwritten).")
    parser.add_argument("--output_json",    type=str, required=True,
                        help="Where to write the new test JSON (transforms_test.json).")
    parser.add_argument("--test_folder",    type=str, default="./test",
                        help="Folder to move test images into (must exist or be creatable).")
    parser.add_argument("--num_test_frames", type=int, default=10,
                        help="How many images to move to test set.")
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

    # 2) Pick random frames for testing
    random.seed(args.seed)
    if args.num_test_frames > total_frames:
        print(f"Requested {args.num_test_frames} test frames, but only {total_frames} exist.")
        return
    test_indices = set(random.sample(range(total_frames), args.num_test_frames))

    # 3) Partition frames into 'test_frames' and 'remaining_frames'
    test_frames = []
    remaining_frames = []
    for i, frame in enumerate(all_frames):
        if i in test_indices:
            test_frames.append(frame)
        else:
            remaining_frames.append(frame)

    os.makedirs(args.test_folder, exist_ok=True)

    # 4) Move each chosen test file into the test folder, adjusting the file_path
    for frame in test_frames:
        old_path = frame["file_path"]  # e.g. "./train/0002", or "./train/0002.png"

        # We'll guess there's a .png extension if none is present in the JSON
        folder_part, filename = os.path.split(old_path)
        name, ext = os.path.splitext(filename)
        if ext == "":
            ext = ".png"  # assume .png if missing

        # The file on disk
        full_old_path = os.path.join(folder_part, name + ext)

        # Build new disk path and new JSON path (force forward slash)
        new_disk_path = os.path.join(args.test_folder, name + ext)  
        # If you want the JSON to have no extension: e.g. "./test/0002"
        # new_json_path = f"./test/{name}"
        # If you want the JSON to keep ".png": 
        new_json_path = f"./test/{name}"

        # Physically move the file
        if not os.path.exists(full_old_path):
            print(f"Warning: image file '{full_old_path}' does not exist!")
        else:
            shutil.move(full_old_path, new_disk_path)
            print(f"Moved '{full_old_path}' -> '{new_disk_path}'")

        # Update the frame path in the test set
        frame["file_path"] = new_json_path

    # 5) Create new JSON data for test
    test_data = {}
    for k, v in data.items():
        if k != "frames":
            test_data[k] = v
    test_data["frames"] = test_frames

    # 6) Overwrite the original JSON with only the remaining frames
    data["frames"] = remaining_frames
    with open(args.input_json, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Overwrote '{args.input_json}' to keep {len(remaining_frames)} frames (train/val).")

    # 7) Write out transforms_test.json
    with open(args.output_json, "w") as f:
        json.dump(test_data, f, indent=2)
    print(f"Wrote '{args.output_json}' with {len(test_frames)} test frames.")


if __name__ == "__main__":
    main()

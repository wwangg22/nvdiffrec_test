#!/usr/bin/env python3

import json
import sys
import os

def main(input_json_path, output_json_path):
    # Read the JSON data from file
    with open(input_json_path, 'r') as f:
        data = json.load(f)
    
    # Loop over every frame and remove .png from file_path if present
    for frame in data.get("frames", []):
        old_path = frame.get("file_path", "")
        
        # Use os.path.splitext to split extension; remove only if it's ".png"
        root, ext = os.path.splitext(old_path)
        if ext.lower() == ".png":
            frame["file_path"] = root
        else:
            frame["file_path"] = old_path

    # Write out the updated JSON data
    with open(output_json_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input_json> <output_json>")
        sys.exit(1)

    input_json = sys.argv[1]
    output_json = sys.argv[2]
    main(input_json, output_json)

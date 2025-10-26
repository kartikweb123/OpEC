# Function for pre-processing input files

import re
import os
from pathlib import Path


def clean_lib_file(input_file, output_dir):
    # Removes non-synthesizable elements from libarary verilog file.
    
    if not os.path.exists(input_file):
        print("ERROR: File not found with", input_file)
        return
    if not os.path.exists(output_dir):
        print("ERROR: Invalid output directpry", output_dir)
        return
    
    # Creating output file path
    output_filename = "lib.v"
    output_path = Path(output_dir) / output_filename
    
    try:
        with open(input_file, 'r') as f:
            verilog_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    cleaned_content = re.sub(r'^\s*`.*$', '', verilog_content, flags=re.MULTILINE)
    print("  - Removed all lines starting with '`'.")

    cleaned_content = re.sub(r'specify.*?endspecify', '', cleaned_content, flags=re.DOTALL | re.IGNORECASE)
    print("  - Removed all 'specify...endspecify' blocks.")

    # cleaned_content = re.sub(r'//.*', '', cleaned_content)
    # print("  - Removed single-line comments (//).")

    cleaned_content = re.sub(r'^\s*$', '', cleaned_content, flags=re.MULTILINE)
    print("  - Removed resulting empty lines.")
    
    try:
        with open(output_path, 'w') as f:
            f.write(cleaned_content)
        print("Successfully cleaned file written to", output_path)
    except Exception as e:
        print(f"Error writing file: {e}")


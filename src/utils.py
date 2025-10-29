# Function for handling arguments

import os
import sys
import re


def check_file(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            print("Looks OK!")
        else:
            print("ERROR: Path is not a file.")    
            sys.exit(1)
    else:
        print("ERROR: Path does not exist.")
        sys.exit(1)
        
        
def check_dir(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            print("Looks OK!")
        else:
            print("ERROR: Path is not a directory.")
            sys.exit(1)
    else:
        print("ERROR: Path does not exist.")
        sys.exit(1)
        
def collect_verilog_modules(path):
    module_pattern = re.compile(r'^\s*module\s+([A-Za-z_]\w*)')
    if os.path.isdir(path):
        module_names = []
        for root, _, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    for line in f:
                        match = module_pattern.match(line)
                        if match:
                            module_names.append(match.group(1))
        
    if os.path.isfile(path):
        with open(path, 'r') as f:
            for line in f:
                match = module_pattern.match(line)
                if match:
                    module_names = match.group(1)

    return module_names

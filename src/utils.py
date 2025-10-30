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


def get_verilog_modules(path):
    module_pattern = re.compile(r'^\s*module\s+([A-Za-z_]\w*)')
    module = {} # returns a dict as "module": "corrsponding/verilog/file/path"
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    for line in f:
                        match = module_pattern.match(line)
                        if match:
                            module[match.group(1)] = filepath
        
    if os.path.isfile(path):
        with open(path, 'r') as f:
            for line in f:
                match = module_pattern.match(line)
                if match:
                    module[match.group(1)] = path

    return module


def get_module_snippet(module, path):
    snippet = []
    inside_module = False

    # regex: match 'module <top>' with optional spaces/params after
    module_pattern = re.compile(rf'^\s*module\s+{re.escape(module)}(\s*#\s*\(|\s|\().*', re.IGNORECASE)
    endmodule_pattern = re.compile(r'^\s*endmodule\b', re.IGNORECASE)

    with open(path, 'r') as f:
        for line in f:
            if not inside_module and re.match(module_pattern, line):
                inside_module = True

            if inside_module:
                cleaned_line = line.replace('\t', '')
                snippet.append(cleaned_line.rstrip('\n'))
                if re.match(endmodule_pattern, line):
                    break

        if not snippet:
            print("ERROR:no such module found in rtl file.")
            sys.exit(1)
        else:
            return snippet

"""
Enhancement needed: 
1)  Return a dict instead of list where key is reg name and value is its width.
2)  Make it recursive so that the code can jump to instantiated modules inside top module and retain width size from instantiation.
    OR
    Find a way to combine all rtl modules into 1 flat top module.
"""
def get_regs(module_snippet: list):
    regs = []
    assign_pattern = re.compile(r'([\w\[\]:]+)\s*<=')  # matches LHS before <=
    
    for line in module_snippet:
        match = assign_pattern.search(line)
        if match:
            regs.append(match.group(1))
    
    return sorted(set(regs))






















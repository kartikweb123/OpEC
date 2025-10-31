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
1)  Return a dict instead of list where key is reg name and value is its width. (done)
2)  Make it recursive so that the code can jump to instantiated modules inside top module and retain width size from instantiation.
    OR
    Find a way to combine all rtl modules into 1 flat top module.
3) Add support for localparam. example: localparam MAX_VALUE = (1 << DATA_WIDTH) - 1;
"""
def get_regs(module_snippet: list):
    regs = {}
    params = {}
    width_def = {}
    
    assign_pattern = re.compile(r'([\w\[\]:]+)\s*<=') # matches LHS before <=
    param_pattern = re.compile(r'parameter\s+(\w+)\s*=\s*([\w\'\+\-\*/]+)', re.IGNORECASE) # matches all parameter definitions
    signal_pattern = re.compile(r'\b(?:input|output|inout)?\s*(?:reg|logic)\s*(\[[^\]]+\])?\s*(\w+)', re.IGNORECASE) # matches all "reg" and "logic"
    
    for line in module_snippet:
        param_match = param_pattern.search(line)
        assign_match = assign_pattern.search(line)
        signal_match = signal_pattern.search(line)
        
        # capture all parameter with default values
        if param_match:
            name, value = param_match.groups()
            try:
                params[name] = int(eval(value))  # safe arithmetic only
            except Exception:
                params[name] = value  # keep unresolved for now
        
        # capture reg definitions with sizes
        width = 1
        if signal_match:
            width_expr, reg_name = signal_match.groups()
            if width_expr:
                width_expr = width_expr.strip('[]')
                if ':' in width_expr:
                    msb, lsb = [x.strip() for x in width_expr.split(':')]
                    try:
                        for k, v in params.items():
                            msb = msb.replace(k, str(v))
                            lsb = lsb.replace(k, str(v))
                        width = abs(eval(msb) - eval(lsb)) + 1
                    except Exception:
                        width = f"[(width_expr)]"
                else:
                    width = 1
            width_def[reg_name] = width
        
        # capture all sequential regs
        if assign_match:
            regs[assign_match.group(1)] = width_def[assign_match.group(1)]
            
    # print("parameters:", params)
    # print("width definition:",width_def)
    return regs

"""
Enhancement needed:
1) unable to parse port definitions: input wire [] a, b;
2) unable to parse port definitions: input a;
                                     wire [] a;
"""
def get_ports(module_snippet: list):
    inputs = {}
    outputs = {}
    params = {}

    # Combine snippet into one text
    snippet_text = "\n".join(module_snippet)

    # --- remove single-line comments ---
    snippet_text = re.sub(r'//.*', '', snippet_text)

    # --- capture parameters ---
    param_pattern = re.compile(r'parameter\s+(\w+)\s*=\s*([\w\'\+\-\*/]+)', re.IGNORECASE)
    for match in param_pattern.finditer(snippet_text):
        name, value = match.groups()
        try:
            params[name] = int(eval(value))
        except Exception:
            params[name] = value

    # --- capture typed input/output declarations (wire/reg only) ---
    port_pattern = re.compile(r'\b(input|output)\b\s*(?:wire|reg)?\s*(\[[^\]]+\])?\s*([^;,\n]+)', re.IGNORECASE)

    for match in port_pattern.finditer(snippet_text):
        direction, width_expr, port_name = match.groups()
        port_name = port_name.strip()

        # calculate width
        width = 1
        if width_expr:
            width_expr = width_expr.strip('[]')
            if ':' in width_expr:
                msb, lsb = [x.strip() for x in width_expr.split(':')]
                try:
                    for p, v in params.items():
                        msb = msb.replace(p, str(v))
                        lsb = lsb.replace(p, str(v))
                    width = abs(eval(msb) - eval(lsb)) + 1
                except Exception:
                    width = f"[{width_expr}]"
            else:
                width = 1

        # store in dict
        if direction.lower() == 'input':
            inputs[port_name] = width
        else:
            outputs[port_name] = width

    return inputs, outputs




















# Source code with main function as entry-point

from arg_parser import *
from utils import *
from cleaner import clean_lib_file
import sys


if __name__ == '__main__':
    args = argument_parser()
    config = load_config(args.config)
    
    print("\nAnalyzing config file...")
    print("Loaded:", args.config)
    
    print("RTL directory:", config['general']['rtl_dir'])
    check_dir(config['general']['rtl_dir'])
    MODULES = collect_verilog_modules(config['general']['rtl_dir'])
    print("Modules found in RTL directory:", MODULES)
    
    print("Top module:", config['general']['top_module'])
    if config['general']['top_module'] not in MODULES:
        print("ERROR: Module name not found")
        sys.exit(1)
    else:
        print("Looks OK!")
    
    print("Netlist file:", config['general']['netlist_file'])
    check_file(config['general']['netlist_file'])
    NETLIST_MODULE = collect_verilog_modules(config['general']['netlist_file'])
    if config['general']['top_module'] != NETLIST_MODULE:
        print("ERROR: Module name mismatch between RTL and netlist")
        sys.exit(1)
    
    print("Library verilog file:", config['general']['lib_verilog_file'])
    check_file(config['general']['lib_verilog_file'])
    
    print("Library liberty file:", config['general']['lib_file'])
    check_file(config['general']['lib_file'])
    
    print("Output directory:", config['general']['output_dir'])
    check_dir(config['general']['output_dir'])
    
    
    
    
    
    print("\nAnalyzing library verilog file...")
    clean_lib_file(config['general']['lib_verilog_file'], config['general']['output_dir'])
    

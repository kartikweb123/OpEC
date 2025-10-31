# Source code with main function as entry-point

from arg_parser import *
from utils import *
from cleaner import *
import sys


if __name__ == '__main__':
    args = argument_parser()
    config = load_config(args.config)

    TOP_MODULE = config['general']['top_module']
    RTL_DIR = config['general']['rtl_dir']
    OUTPUT_DIR = config['general']['output_dir']
    NETLIST_PATH = config['general']['netlist_file']
    LIB_VERILOG = config['general']['lib_verilog_file']
    LIB_LIBERTY = config['general']['lib_liberty_file']
    
    print("\nAnalyzing config file...")
    print("Loaded:", args.config)
    
    print("RTL directory:", RTL_DIR)
    check_dir(RTL_DIR)
    RTL_MODULES = get_verilog_modules(RTL_DIR)
    print("Modules found in RTL directory:", list(RTL_MODULES.keys()))
    
    print("Top module:", TOP_MODULE)
    if TOP_MODULE not in RTL_MODULES:
        print("ERROR: Module name not found")
        sys.exit(1)
    else:
        print("Looks OK!")
    
    print("Netlist file:", NETLIST_PATH)
    check_file(NETLIST_PATH)
    NETLIST_MODULES = get_verilog_modules(NETLIST_PATH)
    print("Modules found in netlist file:", list(NETLIST_MODULES.keys()))
    if TOP_MODULE not in list(NETLIST_MODULES.keys()):
        print("ERROR: Module name mismatch between RTL and netlist")
        sys.exit(1)
    
    print("Library verilog file:", LIB_VERILOG)
    check_file(LIB_VERILOG)
    
    print("Library liberty file:", LIB_LIBERTY)
    check_file(LIB_LIBERTY)
    
    print("Output directory:", OUTPUT_DIR)
    check_dir(OUTPUT_DIR)

    dff_module_snippet = get_module_snippet("dff", RTL_MODULES["dff"])
    print("\nlist of regs found in dff rtl:", get_regs(dff_module_snippet))
    top_module_snippet = get_module_snippet(TOP_MODULE, RTL_MODULES[TOP_MODULE])
    print("list of regs found in top rtl:", get_regs(top_module_snippet))
    
    dff_input_ports, dff_output_ports = get_ports(dff_module_snippet)
    print("list of input ports in dff module:", dff_input_ports)
    print("list of output ports in dff module:", dff_output_ports)
    top_input_ports, top_output_ports = get_ports(top_module_snippet)
    print("list of input ports in top module:", top_input_ports)
    print("list of output ports in top module:", top_output_ports)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    print("\nAnalyzing library verilog file...")
    clean_lib_file(LIB_VERILOG, OUTPUT_DIR)
    

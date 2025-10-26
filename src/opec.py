# Source code with main function as an entry-point
from arg_parser import create_arg_parser
from cleaner import clean_lib_file


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()
    
    print("\nTop level module name is:", args.module)
    print("Technology verilog file:", args.lib)
    print("RTL dirctory:", args.rtl_dir)
    print("Netlist:", args.netlist)
    print("Output directory:", args.output_dir)
    
    clean_lib_file(args.lib, args.output_dir)

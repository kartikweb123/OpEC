# Source code with main function as entry-point

from arg_parser import create_arg_parser
from arg_parser import check_file
from arg_parser import check_dir
from cleaner import clean_lib_file


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()
    
    print ("\nValidating collaterals...")
    print("  - Technology verilog file:", args.lib)
    check_file(args.lib)
    print("  - RTL dirctory:", args.rtl_dir)
    check_dir(args.rtl_dir)
    print("  - Netlist:", args.netlist)
    check_file(args.netlist)
    print("  - Output directory:", args.output_dir)
    check_dir(args.output_dir)
    print("  - Top level module name is:", args.module)
    
    print("\nAnalyzing library verilog file...")
    clean_lib_file(args.lib, args.output_dir)

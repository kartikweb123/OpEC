import argparse as ap

def create_arg_parser():
    parser = ap.ArgumentParser(
        description='Thanks for using OpEC. Please send any feedbacks to kartikweb@gmail.com',
        epilog='Example: python3 opec.py'
    )

    parser.add_argument(
        '--rtl_dir',
        type=str,
        help='Your RTL .v files directory'
    )

    parser.add_argument(
        '--netlist',
        type=str,
        help='Your flat netlist .v file'
    )

    parser.add_argument(
        '--module',
        type=str,
        help='Name of your top level design.'
    )

    parser.add_argument(
        '--lib',
        type=str,
        help='Technology liberty (.lib) file'
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        help='Your desired output directory. This will contain all logs and reports.'
    )
    
    return parser

if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()
    # print(args)

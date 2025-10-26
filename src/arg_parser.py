# Function for handling arguments

import argparse


def create_arg_parser():
    parser = argparse.ArgumentParser(
        description='Thanks for using OpEC. Please send any feedbacks to kartikweb@gmail.com',
        epilog='Example: python3 opec.py'
    )

    parser.add_argument(
        '--rtl_dir',
        type=str,
        required=True,
        help='Your RTL .v files directory'
    )

    parser.add_argument(
        '--netlist',
        type=str,
        # required=True,
        help='Your flat netlist .v file'
    )

    parser.add_argument(
        '--module',
        type=str,
        required=True,
        help='Name of your top level design'
    )

    parser.add_argument(
        '--lib',
        type=str,
        required=True,
        help='Technology .v file containing all stdcells'
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        required=True,
        help='Your desired output directory. This will contain all logs and reports'
    )
    
    return parser


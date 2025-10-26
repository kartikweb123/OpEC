# Function for handling arguments

import os
import sys
import argparse


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rtl_dir', type=str, required=True, help='Your RTL .v files directory')
    parser.add_argument('--netlist', type=str, required=True, help='Your flat netlist .v file')
    parser.add_argument('--module', type=str, required=True, help='Name of your top level design')
    parser.add_argument('--lib', type=str, required=True, help='Technology .v file containing all stdcells')
    parser.add_argument('--output_dir', type=str, required=True, help='Your desired output directory. This will contain all logs and reports')
    return parser


def check_file(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            print("  Looks OK!")
        else:
            print("  ERROR: Path is not a file.")    
            sys.exit(1)
    else:
        print("  ERROR: Path does not exist.")
        sys.exit(1)
        
        
def check_dir(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            print("  Looks OK!")
        else:
            print("  ERROR: Path is not a directory.")
            sys.exit(1)
    else:
        print("  ERROR: Path does not exist.")
        sys.exit(1)
        

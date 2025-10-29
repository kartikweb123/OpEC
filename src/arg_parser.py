import argparse
import tomllib


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', type=str, required='true', help="Configuration file needed to run equivalence checker. Sample config file is in github repo.")
    return parser.parse_args()

def load_config(path):
    with open(path, 'rb') as toml_config_file:
        return tomllib.load(toml_config_file)


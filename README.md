# OpEC — Open-source Equivalence Checker

OpEC is a Python-based tool designed to perform **logic equivalence checking** between RTL designs and their corresponding synthesized netlists.
It helps digital designers verify that transformations, optimizations, or synthesis steps do not change functional behavior.

## Features

- Parse Verilog/SystemVerilog RTL files and extract module definitions
- Identify sequential signals (flip-flops) automatically
- Compare RTL with synthesized netlists for functional equivalence
- Configurable via a TOML file for easy integration with different projects
- Command-line interface (CLI) with options for configuration and template generation

## Limitations
- Still work in progress (10% done)
- Only works with YOSYS synthesized netlist
- Targeting 45nm free pdk

## Installation

Clone the repository and ensure you have Python 3.8+ installed:

```bash
git clone https://github.com/kartikweb123/OpEC.git
cd OpEC
pip install -r requirements.txt


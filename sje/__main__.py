#!/usr/bin/env python
import argparse
import json
import os
import sys

import yaml

from .extractor import *

MODE_TO_FILE = "file"
MODE_TO_CONSOLE = "console"
FORMAT_TO_JSON = "json"
FORMAT_TO_SQL = "sql"


def main(argv=None):
    options = _parse_arguments()

    with open(options.input) as input_file:
        if options.input.endswith(".json"):
            data = json.load(input_file)
        elif options.input.endswith(".yaml") or options.input.endswith(".yml"):
            data = yaml.load(input_file, Loader=yaml.SafeLoader)
        input_file.close()

    if options.format == FORMAT_TO_JSON:
        parsed = flatten_all(data)
        results = json.dumps(parsed, indent=4)
    elif options.format == FORMAT_TO_SQL:
        results = flatten_all_as_sql(data, options.trailer_clause)

    if options.mode == MODE_TO_CONSOLE:
        print(results)
    elif options.mode == MODE_TO_FILE:
        with open(options.output, "w+") as output_file:
            output_file.write(results)
            output_file.close()
        print(f"File has been written to {os.path.abspath(output_file.name)}")


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--format",
        default=FORMAT_TO_JSON,
        help=f"Output format: {FORMAT_TO_JSON}, {FORMAT_TO_SQL}.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        default=MODE_TO_CONSOLE,
        help=f"Output mode: {MODE_TO_FILE}, {MODE_TO_CONSOLE}.",
    )
    parser.add_argument("-i", "--input", help="Data schema file as input.")
    parser.add_argument(
        "-o",
        "--output",
        help=f"Flatten schema file as output. Required only if mode is set to {MODE_TO_FILE}",
    )
    parser.add_argument(
        "-t",
        "--trailer_clause",
        help=f"The SQL trailer clause after the select statement. Would only be used if mode is set to {FORMAT_TO_SQL}",
    )

    options = parser.parse_args()

    if options.mode:
        options.format = options.format.lower()
        options.mode = options.mode.lower()
        if options.format not in [FORMAT_TO_JSON, FORMAT_TO_SQL]:
            print(
                f"Please provide one of the following output formats: {FORMAT_TO_JSON}, {FORMAT_TO_SQL}"
            )
            sys.exit(1)
        if options.mode not in [MODE_TO_FILE, MODE_TO_CONSOLE]:
            print(
                f"Please provide one of the following output modes: {MODE_TO_FILE}, {MODE_TO_CONSOLE}"
            )
            sys.exit(1)
        elif not options.input:
            print("Please provide input file")
            sys.exit(1)
        elif options.mode == MODE_TO_FILE and not options.output:
            print("Please provide output file")
            sys.exit(1)

    return options


if __name__ == "__main__":
    main()

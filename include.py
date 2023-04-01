#!/usr/bin/env python3

import argparse
import fileinput
import os
import re

# This regular expression is looking for:
# - A line that starts with #include
# - Has quotes with 1+ characters inside (the include path)
# - Has 0+ whitespace characters before the line ends
regex = re.compile(r"^#include \"(.+)\"\s*$")


def parse_arguments() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "file",
        default="-",
    )
    return p.parse_args()


def raw_print(line: object):
    print(line, end="")


def main():
    args = parse_arguments()

    with fileinput.input(files=args.file) as f:
        for line in f:
            match = regex.match(line)
            if not match:
                raw_print(line)
                continue

            current_file = fileinput.filename()
            base_dir = os.path.dirname(current_file)
            included_path = match.group(1)
            to_include = os.path.join(base_dir, included_path)

            with open(to_include, "r") as included:
                raw_print(included.read())


if __name__ == "__main__":
    main()

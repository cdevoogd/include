#!/usr/bin/env python3

import argparse
from fileinput import FileInput
import os
import re

# Global script arguments. This will only be populated after the arguments are
# parsed.
args: argparse.Namespace

# This regular expression is looking for:
# - A line that starts with #include
# - Has quotes with 1+ characters inside (the include path)
# - Has 0+ whitespace characters before the line ends
regex = re.compile(r"^#include \"(.+)\"\s*$")

# included stores all files that have already been included. This allows the
# script to strictly enforce a behavior similar to C's #pragma once directive
# that ensures that a file is only included once in a file even if requested
# multiple times.
included = set()


def parse_arguments():
    p = argparse.ArgumentParser()
    p.add_argument(
        "file",
        default="-",
        help="The file to process includes in (default: stdin)",
    )
    p.add_argument(
        "--max-depth",
        type=int,
        default=10,
        metavar="int",
        help="The maximum allowed include depth before an error is thrown",
    )

    global args
    args = p.parse_args()


def process_line(line: str):
    print(line, end="")


# Even though the fileinput module is meant to handle multiple input sources,
# it is only being used here for it's easy management of stdin. This method
# should only ever accept a single file as an argument.
def process_file(path: str, depth=1):
    if depth > args.max_depth:
        raise Exception("Depth limit reached!")

    if path in included:
        return

    included.add(path)
    with FileInput(files=path) as input:
        parent_dir = os.path.dirname(path)
        for line in input:
            match = regex.match(line)
            if not match:
                process_line(line)
                continue

            requested_include = match.group(1)
            include_path = os.path.normpath(os.path.join(parent_dir, requested_include))
            process_file(include_path, depth=depth + 1)


def main():
    parse_arguments()
    process_file(args.file)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
from enum import Enum
from fileinput import FileInput
import os
import sys
import re


class FileType(Enum):
    UNKNOWN = 0
    SHELL = 1


# Global script arguments. This will only be populated after the arguments are
# parsed.
args: argparse.Namespace
filetype: FileType = FileType.UNKNOWN

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

    global filetype
    if args.file.endswith(".sh"):
        filetype = FileType.SHELL


def process_line(line: str, *, current_depth: int):
    # If we are adding text to a shell script, don't add additional shebangs
    if current_depth > 1 and filetype == FileType.SHELL and line.startswith("#!"):
        return

    print(line, end="")


# Even though the fileinput module is meant to handle multiple input sources,
# it is only being used here for it's easy management of stdin. This method
# should only ever accept a single file as an argument.
def process_file(path: str, depth=1):
    if depth > args.max_depth:
        print(
            f"FATAL: Maximum allowed depth of {args.max_depth} reached!",
            file=sys.stderr,
        )
        sys.exit(1)

    if path in included:
        return

    included.add(path)
    with FileInput(files=path) as input:
        parent_dir = os.path.dirname(path)
        for line in input:
            match = regex.match(line)
            if not match:
                process_line(line, current_depth=depth)
                continue

            requested_include = match.group(1)
            include_path = os.path.normpath(os.path.join(parent_dir, requested_include))
            process_file(include_path, depth=depth + 1)


def main():
    parse_arguments()
    process_file(args.file)


if __name__ == "__main__":
    main()

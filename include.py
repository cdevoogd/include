#!/usr/bin/env python3

import argparse
from fileinput import FileInput
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


def print_raw(line: object):
    print(line, end="")


# Even though the fileinput module is meant to handle multiple input sources,
# it is only being used here for it's easy management of stdin. This method
# should only ever accept a single file as an argument.
def process_file(path: str, depth=1):
    if depth > 10:
        raise Exception("Depth limit reached!")

    with FileInput(files=path) as input:
        parent_dir = os.path.dirname(path)
        for line in input:
            match = regex.match(line)
            if not match:
                print_raw(line)
                continue

            include_path = match.group(1)
            to_include = os.path.join(parent_dir, include_path)
            # FIXME: This needs to protect against recursive includes.
            process_file(to_include, depth=depth + 1)


def main():
    args = parse_arguments()
    process_file(args.file)


if __name__ == "__main__":
    main()

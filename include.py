#!/usr/bin/env python3

import argparse
import fileinput
import re

# This regular expression is looking for:
# - A line that starts with #include
# - Has quotes with 1+ characters inside (the include path)
# - Has 0+ whitespace characters before the line ends
regex = re.compile(r"^#include \"(.+)\"\s*$")


def parse_arguments() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "files",
        nargs="?",
        default="-",
    )
    return p.parse_args()


def main():
    args = parse_arguments()

    with fileinput.input(files=args.files) as f:
        for line in f:
            match = regex.match(line)
            if not match:
                continue

            print(f"Match Found! {fileinput.filename()} @ L{fileinput.lineno()}")
            print(f"    Included File: {match.group(1)}")


if __name__ == "__main__":
    main()

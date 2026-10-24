#!/usr/bin/env python
import argparse
import sys

from process_rep import *

def main():
    ap = argparse.ArgumentParser(description="Clean a raw `top` capture into a readable report.")
    ap.add_argument("input", nargs="?", help="raw top capture file")
    ap.add_argument("-o", "--output", help="output file (default: stdout)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--first", action="store_true", help="only the first snapshot")
    g.add_argument("--last", action="store_true", help="only the last snapshot")
    g.add_argument("--frame", type=int, help="only snapshot N (1-based)")
    ap.add_argument("--no-fill", action="store_true", help="don't restore unchanged lines from prior frame")
    ap.add_argument("--delete", metavar="FILE", help="permanently delete FILE after cleaning the file onto the output")
    ap.add_argument("-y", "--yes", action="store_true", help="delete without confirmation") #subject to change
    args = ap.parse_args()

    if not args.input and not args.delete:
        ap.error("provide an input file to clean, --delete FILE, or both")

    if args.input:
        with open(args.input, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()
 
        frames = build_frames(raw, fill=not args.no_fill)
        if not frames:
            sys.exit("No top frames found in input.")
 
        if args.first:
            selected = [frames[0]]
        elif args.last:
            selected = [frames[-1]]
        elif args.frame:
            if not 1 <= args.frame <= len(frames):
                sys.exit(f"--frame must be between 1 and {len(frames)}")
            selected = [frames[args.frame - 1]]
        else:
            selected = frames
 
        report = format_report(selected)
 
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Wrote {len(selected)} snapshot(s) to {args.output}")
        else:
            print(report)

    if args.delete:
        remove_file(args.delete, confirm=not args.yes)
 
 
if __name__ == "__main__":
    main()
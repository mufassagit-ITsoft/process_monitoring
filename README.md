"""
clean_top.py - Convert a raw capture of the Linux `top` command (with ANSI
escape codes) into a clean, readable text report.
 
top redraws only changed lines, so blank lines in a later frame mean
"unchanged". This script restores those lines from the previous frame so
every snapshot is a complete top report.
 
Usage:
    python3 clean_top.py process_moitoring.txt                 # all snapshots
    python3 clean_top.py process_moitoring.txt -o report.txt   # write to file
    python3 clean_top.py process_moitoring.txt --last          # final snapshot only
    python3 clean_top.py process_moitoring.txt --first
    python3 clean_top.py process_moitoring.txt --frame 5       # snapshot #5
    python3 clean_top.py process_moitoring.txt --no-fill       # don't restore blank lines
"""
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

# Process Report Cleaner

Converts a raw capture of the Linux `top` command (full of ANSI escape codes) into a clean, readable text report.

## Files

| File | Purpose |
|------|---------|
| `main.py` | Command-line entry point |
| `process_rep.py` | Module that strips ANSI codes, splits the capture into snapshots, and formats the report |
| `process_moitoring.txt` | Example raw `top` capture |

Keep `main.py` and `process_rep.py` in the same folder.

## Requirements

- Python 3.6+
- No third-party packages

## Creating a capture

Record `top` output to a file (for example, with `script` or by redirecting a batch run):

```
top -b -n 10 > process_moitoring.txt
```

## Usage

```
python3 main.py <input_file> [options]
```

| Option | Description |
|--------|-------------|
| `-o FILE`, `--output FILE` | Write the report to `FILE` instead of the screen |
| `--first` | Output only the first snapshot |
| `--last` | Output only the last snapshot |
| `--frame N` | Output only snapshot `N` (1-based) |
| `--no-fill` | Do not restore unchanged lines from the previous snapshot |

`--first`, `--last`, and `--frame` cannot be combined.

### Examples

```
python3 main.py process_moitoring.txt                  # all snapshots, printed
python3 main.py process_moitoring.txt -o report.txt    # save to a file
python3 main.py process_moitoring.txt --last           # final snapshot only
python3 main.py process_moitoring.txt --frame 5        # snapshot 5
```

## How it works

1. **Split**: the capture is divided into snapshots at each cursor-home escape sequence (`ESC[H`), which `top` emits at every refresh. Text before the first one (such as `current report:`) is dropped.
2. **Clean**: ANSI escape codes are stripped and trailing whitespace is removed, keeping the column alignment.
3. **Fill**: `top` redraws only the lines that changed, so unchanged lines (such as the `Tasks:` line or the column header) appear blank in later snapshots. These are restored from the previous snapshot so each one is a complete report. Use `--no-fill` to disable this.
4. **Format**: snapshots are joined into one report, each labeled `===== Snapshot N of M =====` when there is more than one.

## Sample output

```
top - 09:23:14 up 3 days, 22:31,  1 user,  load average: 1.35, 1.09, 0.73
Tasks: 455 total,   2 running, 453 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.7 us,  1.1 sy,  0.0 ni, 96.2 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :  31760.5 total,  12056.1 free,   7765.7 used,  13571.8 buff/cache
MiB Swap:   8192.0 total,   8192.0 free,      0.0 used.  23994.8 avail Mem

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   3576 mufassa   20   0  990336 162448 102564 S  15.6   0.5  27:41.86 Xorg
   3784 mufassa   20   0 4772268 392268 147336 S  15.0   1.2  31:49.38 gnome-s+
```

## Notes

- If no snapshots are found, the program exits with `No top frames found in input.`
- `--frame N` exits with an error if `N` is outside the range of available snapshots.
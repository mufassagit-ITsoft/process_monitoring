__author__: "Mustafa Prodhan"
import re

from pathlib import Path

# cleaning up the ANSI characters that are cluttering the top command report
ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b[()][A-Za-z0-9]|\x1b[=>]")
HOME_RE = re.compile(r"\x1b\[H") # start of a new top report
CLEAR_RE = re.compile(r"\x1b\[2J")

def split_frames(raw):
    #splits lines, to create a list of each line objects
    try:
        raw = CLEAR_RE.sub("", raw)
        parts = HOME_RE.split(raw)
    except:
        raise TypeError("split_frames expects text (str), not " + type(raw).__name__)
    return parts[1:] if len(parts) > 1 else parts

def clean_lines(frame):
    try:
        text = ANSI_RE.sub("", frame).replace("\r", "")
    except:
        raise TypeError("clean_lines expects text (str), not " + type(frame).__name__)
    return [ln for ln in text.split("\n")]

# builds the report after splitting the ANSI file and then cleaning the ANSI lines
def build_frames(raw, fill=True):
    try:
        frames, prev = [], []
        for part in split_frames(raw):
            lines = clean_lines(part)
            while lines and not lines[-1]: #drop any trailing lines or end of frame padding
                lines.pop()
            if fill and prev:
                for i, ln in enumerate(lines):
                    if not ln and i < len(prev):
                        lines[i] = prev[i]
            if lines:
                frames.append(lines)
                prev = lines
    except:
        raise TypeError(f"build_frames needs the capture as text (str): {err}") from err
    return frames

# formats the report into a coherent file
def format_report(frames):
    try:
        proc_report = []
        for i, lines in enumerate(frames, 1):
            if len(frames) > 1:
                proc_report.append(f"===== Snapshot {i} of {len(frames)} =====")
            proc_report.extend(lines)
            proc_report.append("")
    except:
        raise TypeError(f"format_report needs a list of snapshots, each a list of text lines: {err}") from err
    return "\n".join(proc_report)

def remove_file(path, confirm=True):
    try:
        file_del = Path(input("Which file needs to be removed: ").strip())

        if not file_del.is_file():
            print(f"File not found: {file_del}")
            return False

        if confirm and input(f"Permanently delete {file_del}? (y/n): ").strip().lower() !="y":
            print("Deletion cancelled.")
            return False
        file_del.unlink()
    except PermissionError:
        print(f"Permission denied: cannot delete {file_del}")
        return False
    except OSError as err:
        print(f"Could not delete {file_del}: {err}")
        return False
    else:
        print("File deleted successfully")
        return True
    finally:
        print("finished deletion")
    
    
import re

# cleaning up the ANSI characters that are cluttering the top command report
ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b[()][A-Za-z0-9]|\x1b[=>]")
HOME_RE = re.compile(r"\x1b\[H") # start of a new top report
CLEAR_RE = re.compile(r"\x1b\[2J")

def split_frames(raw):
    #splits lines, to create a list of each line objects
    raw = CLEAR_RE.sub("", raw)
    parts = HOME_RE.split(raw)
    return parts[1:] if len(parts) > 1 else parts

def clean_lines(frame):
    text = ANSI_RE.sub("", frame).replace("\r", "")
    return [ln for ln in text.split("\n")]

# builds the report after splitting the ANSI file and then cleaning the ANSI lines
def build_frames(raw, fill=True):
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
    return frames

# formats the report into a coherent file
def format_report(frames):
    proc_report = []
    for i, lines in enumerate(frames, 1):
        if len(frames) > 1:
            proc_report.append(f"===== Snapshot {i} of {len(frames)} =====")
        proc_report.extend(lines)
        proc_report.append("")
    return "\n".join(proc_report)
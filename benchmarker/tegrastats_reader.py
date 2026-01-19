import subprocess
import re


def start_monitor(interval: int, path: str):
    """
    Run tegrastats monitoring

    Args:
      - interval (int): Sampling interval in miliseconds
      - path (str): Where to store tegrastats output

    Returns:
      - subp (subprocess.Popen): The Popen object representing the running tegrastats monitor
    """

    log_file = open(path, "w")

    subp = subprocess.Popen(
        ["tegrastats", "--interval", str(interval)],
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True
    )

    return subp


def process(log_file):
    core_pattern = re.compile(
        r"RAM\s+(\d+)/\d+MB.*?"
        r"SWAP\s+(\d+)/\d+MB.*?"
        r"CPU\s*\[([^\]]+)\].*?"
        r"GR3D_FREQ\s+(\d+%)",
        re.DOTALL
    )

    rail_pattern = re.compile(
        r"\b(VDD_[A-Z0-9_]+|VIN_[A-Z0-9_]+)\s+(\d+)(?:mW)?",
        re.IGNORECASE)

    for line in open(log_file, "r"):
        m = core_pattern.search(line)
        if not m:
            continue

        ram, swap, cpu_raw, gr3d = m.groups()
        cpu_vals = [float(x) for x in re.findall(r"(\d+)(?=%@)", cpu_raw)]

        rails = {
            name.upper(): float(val) for name, val in rail_pattern.findall(line)
        }

        rails_sum = sum(rails.values())

        return {
            "RAM": float(ram),
            "SWAP": float(swap),
            "CPU": cpu_vals,
            "GR3D_FREQ": float(gr3d.rstrip('%')),
            "RAILS": rails,
            "VDD_TOTAL": rails_sum
        }

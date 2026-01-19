from time import sleep

def read_meminfo():
    wanted = {
        "MemTotal:",
        "MemFree:",
        "MemAvailable:",
        "SwapTotal:",
        "SwapFree:",
    }
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            key = parts[0]
            if key in wanted:
                # parts[1] is always the numeric value (in kB)
                val = float(parts[1])
                info[key] = val
    return info

while True:
    m = read_meminfo()

    mem_total = m["MemTotal:"]
    mem_avail = m["MemAvailable:"]

    mem_used_percent = 100.0 * (1.0 - mem_avail / mem_total)

    swap_total = m["SwapTotal:"]
    swap_free  = m["SwapFree:"]
    swap_used_percent = 0.0
    if swap_total > 0:
        swap_used_percent = 100.0 * (1.0 - swap_free / swap_total)

    print(f"RAM: {mem_used_percent:5.1f}%   SWAP: {swap_used_percent:5.1f}%")
    sleep(1)

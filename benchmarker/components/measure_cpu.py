from __future__ import print_function
from time import sleep


last_idle = last_total = 0
while True:
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    utilisation = 100.0 * (1.0 - idle_delta / total_delta)
    print(f"{utilisation:.2f}")
    sleep(1)

# from __future__ import print_function

# import signal
# import time

# INTERVAL = 1.0  # seconds
# running = True


# def _handle_sigterm(signum, frame):
#     global running
#     running = False


# def main():
#     global running

#     last_idle = 0.0
#     last_total = 0.0

#     while running:
#         with open("/proc/stat") as f:
#             fields = [float(x) for x in f.readline().split()[1:]]

#         idle = fields[3]
#         total = sum(fields)

#         idle_delta = idle - last_idle
#         total_delta = total - last_total

#         if total_delta > 0:
#             utilisation = 100.0 * (1.0 - idle_delta / total_delta)
#             print(f"{utilisation:5.1f}", flush=True)

#         last_idle = idle
#         last_total = total

#         time.sleep(INTERVAL)


# if __name__ == "__main__":
#     signal.signal(signal.SIGTERM, _handle_sigterm)
#     signal.signal(signal.SIGINT, _handle_sigterm)

#     main()

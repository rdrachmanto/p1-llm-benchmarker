import time
from pynvml import *

try:
    nvmlInit()
    device_count = nvmlDeviceGetCount()

    while(True):
        time.sleep(1)
        for i in range(device_count):
            handle = nvmlDeviceGetHandleByIndex(i)
            mem = nvmlDeviceGetMemoryInfo(handle)
            used_vram_mb = mem.used // (1024 * 1024)
            print(f"Used VRAM: {used_vram_mb} MB")

            usage = nvmlDeviceGetUtilizationRates(handle)
            gpu_util = usage.gpu
            print(f"GPU utilization: {gpu_util}%")

finally:
    nvmlShutdown()

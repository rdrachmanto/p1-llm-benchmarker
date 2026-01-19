def _process_cpu_log():
    pass


def _process_ram_log():
    pass


def _process_nvml_log():
    pass


def process(cpu_log_f, ram_log_f, nvml_log_f):
    cpu_metrics = _process_cpu_log()
    ram_metrics = _process_ram_log()
    nvml_metrics = _process_nvml_log()

    return {

    }

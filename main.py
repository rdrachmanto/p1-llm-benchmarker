import argparse
from pathlib import Path
import subprocess
import time
import utils
import shlex


def _set_metrics_recorder(platform, out):
    procs: dict[str, subprocess.Popen] = {}
    logs: dict[str, object] = {}

    match platform:
        case "jetson":
            p, f = utils.spawn_cmd(
                ["tegrastats", "--interval", "1000"],
                log_path=out / "tegrastats.log"
            )
            procs["tegra"] = p
            logs["tegra"] = f
        case "server":
            monitors = {
                "cpu": "benchmarker.components.measure_cpu",
                "ram": "benchmarker.components.measure_ram",
                "gpu": "benchmarker.components.measure_nvml",
            }

            for name, module in monitors.items():
                p, f = utils.spawn_module(module, interval=3, log_path=out / f"{name}.log")
                procs[name] = p
                logs[name] = f

    return procs, logs


def main(args):
    out = Path("some_path")

    procs: dict[str, subprocess.Popen] = {}
    logs: dict[str, object] = {}

    try:
        procs, logs = _set_metrics_recorder(args.platform, out)

        time.sleep(0.2)  # Some time to sleep to let the metric recorders get set up

        to_benchmark = subprocess.Popen(
            shlex.split(args.exec_string),
            stdout=open(out / "main.stdout.log", "w"),
            stderr=open(out / "main.stderr.log", "w"),
            text=True
        )

        start = time.perf_counter()
        rc = to_benchmark.wait()
        time_to_finish = time.perf_counter() - start

        for p in procs.values():
            utils.stop_process(p)

        for f in logs.values():
            f.close()  # pyright: ignore

        # TODO: processing
        metrics = {}
        # Compile and return results
        results = {
            "returncode": rc,
            "time_to_finish_s": time_to_finish,
            "metrics": metrics,
        }

        return results
    finally:
        for p in procs.values():
            try:
                utils.stop_process(p)
            except Exception:
                pass
        for f in logs.values():
            try:
                f.close()  # pyright: ignore
            except Exception:
                pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--py-executable", "-pyex")
    # parser.add_argument("--to-benchmark", "-tb")
    parser.add_argument("--exec-string", "-exs")
    parser.add_argument("--platform", "-p")

    args = parser.parse_args()
    print(args)

    main(args)

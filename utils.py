import subprocess
from pathlib import Path
import sys
from typing_extensions import Sequence, TextIO


def spawn_module(module: str, *, interval: int, log_path: Path) -> tuple[subprocess.Popen, object]:
    log_f = open(log_path, "w")
    p = subprocess.Popen(
        [sys.executable, "-u", "-m", module],
        stdout=log_f,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    return p, log_f


def spawn_cmd(argv: Sequence[str], *, log_path: Path) -> tuple[subprocess.Popen, TextIO]:
    log_f = open(log_path, "w")
    p = subprocess.Popen(
        list(argv),
        stdout=log_f,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    return p, log_f


def stop_process(p: subprocess.Popen, *, timeout: float = 3.0) -> None:
    if p.poll() is not None:
        return
    p.terminate()
    try:
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill()
        p.wait()

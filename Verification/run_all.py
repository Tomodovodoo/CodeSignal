from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    scripts = sorted(p for p in here.glob("verify_*.py") if p.is_file())
    if not scripts:
        raise SystemExit("No verify_*.py scripts found.")

    for script in scripts:
        print(f"==> {script.name}")
        proc = subprocess.run([sys.executable, str(script)], text=True)
        if proc.returncode != 0:
            raise SystemExit(proc.returncode)

    print("ALL VERIFICATIONS PASSED")


if __name__ == "__main__":
    main()


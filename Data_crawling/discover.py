"""Run this file directly, from any working directory."""

from pathlib import Path

from url_discovery.cli import main

if __name__ == "__main__":
    raise SystemExit(main(workspace=Path(__file__).resolve().parent))

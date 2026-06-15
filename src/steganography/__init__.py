"""Image steganography: hide text inside PNG images and serve it over HTTP.

I keep the carrier images and the sample text files outside the package so the
project root stays the single place to look for data. These paths are resolved
relative to this file so the tools work no matter where I launch them from.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CARRIERS_DIR = PROJECT_ROOT / "assets" / "carriers"
SAMPLES_DIR = PROJECT_ROOT / "samples"

__all__ = ["PROJECT_ROOT", "CARRIERS_DIR", "SAMPLES_DIR"]

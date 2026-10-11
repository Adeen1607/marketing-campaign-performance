"""Download and extract the UCI Bank Marketing data."""

from __future__ import annotations

import argparse
import io
import shutil
import zipfile
from pathlib import Path

import requests


URL = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"
MEMBER = "bank-full.csv"


def download(destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = destination / "bank_marketing.zip"
    output_path = destination / "bank-full.csv"

    with requests.get(URL, stream=True, timeout=120) as response:
        response.raise_for_status()
        with archive_path.open("wb") as target:
            shutil.copyfileobj(response.raw, target)

    if not zipfile.is_zipfile(archive_path):
        raise ValueError("Downloaded file is not a valid ZIP archive.")

    with zipfile.ZipFile(archive_path) as archive:
        # UCI distributes bank-full.csv inside bank.zip, itself in the outer ZIP.
        if "bank.zip" not in archive.namelist():
            raise ValueError("Expected bank.zip in the UCI source archive.")
        with zipfile.ZipFile(io.BytesIO(archive.read("bank.zip"))) as bank:
            if MEMBER not in bank.namelist():
                raise ValueError(f"Expected {MEMBER!r} in bank.zip.")
            with bank.open(MEMBER) as source, output_path.open("wb") as target:
                shutil.copyfileobj(source, target)

    archive_path.unlink()
    print(f"Downloaded dataset to {output_path}")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Bank Marketing data.")
    parser.add_argument("--destination", type=Path, default=Path("data/raw"))
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    download(arguments.destination)

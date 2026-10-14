import json
import subprocess
import sys

from pathlib import Path

import awaiting_result

# OUTPUT_DIR = Path(__file__).parent / "output"
DATA_DIR = Path(__file__).parent / "data"
# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def test_cli_invalid_file():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            "data/124.jsonl",
            "--format",
            "jsonll",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2


def test_cli_valid_file():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(DATA_DIR / "input.jsonl"),
            str(DATA_DIR / "input2.jsonl"),
            "--format",
            "jsonl",
            "--skip-invalid",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0


def test_cli_valid_file_no_skip_invalid():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(DATA_DIR / "input.jsonl"),
            str(DATA_DIR / "input2.jsonl"),
            "--format",
            "jsonl",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2


def test_cli_output_jsonl(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(DATA_DIR / "input.jsonl"),
            str(DATA_DIR / "input2.jsonl"),
            "--format",
            "jsonl",
            "--output",
            str(tmp_path / "REPORT.json"),
            "--skip-invalid",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert (tmp_path / "REPORT.json").exists()

    data = json.loads((tmp_path / "REPORT.json").read_text(encoding="utf-8"))
    assert data == awaiting_result.REPORT_JSONL


def test_cli_output_csv(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(DATA_DIR / "input.csv"),
            "--format",
            "csv",
            "--output",
            str(tmp_path / "REPORT.json"),
            "--skip-invalid",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert (tmp_path / "REPORT.json").exists()

    data = json.loads((tmp_path / "REPORT.json").read_text(encoding="utf-8"))
    assert data == awaiting_result.REPORT_CSV
